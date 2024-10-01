import contextlib
import os
from abc import ABC, abstractmethod
from datetime import date
from functools import cmp_to_key
from logging import getLogger
from pathlib import Path
from typing import List, Union

import classifications as cls
import country_converter as coco
import pandas as pd
import semantic_version

from dataio._classifications_helper import (
    combine_duplicates,
    convert_location_to_iso3,
    filter_classifications,
    generate_classification_mapping,
    increment_version,
)
from dataio.set_logger import set_logger
from dataio.load import load
from dataio.save import save
from dataio.schemas.bonsai_api import *
from dataio.schemas.bonsai_api import DataResource
from dataio.validate import validate_table

logger = getLogger("root")


class ResourceRepository(ABC):
    @abstractmethod
    def add_or_update_resource_list(self, resource: DataResource):
        raise NotImplementedError

    @abstractmethod
    def add_to_resource_list(self, resource: DataResource):
        raise NotImplementedError

    @abstractmethod
    def update_resource_list(self, resource: DataResource):
        raise NotImplementedError

    @abstractmethod
    def get_resource_info(self, **filters) -> DataResource | List[DataResource]:
        raise NotImplementedError

    @abstractmethod
    def resource_exists(self, resource: DataResource) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_dataframe_for_task(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def write_dataframe_for_resource(
        self, data: pd.DataFrame, resource: DataResource, overwrite=True
    ):
        raise NotImplementedError

    @abstractmethod
    def list_available_resources(self) -> list[DataResource]:
        raise NotImplementedError

    @abstractmethod
    def load_with_classification(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def load_with_bonsai_classification(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def harmonize_with_resource(self, dataframe, **kwargs):
        raise NotImplementedError


class CSVResourceRepository(ResourceRepository):
    """
    Repository for managing data resources within a CSV file storage system.

    Attributes
    ----------
    db_path : Path
        Path to the directory containing the resource CSV file.
    table_name : str
        Name of the table (used for naming the CSV file).
    resources_list_path : Path
        Full path to the CSV file that stores resource information.
    schema : DataResource
        Schema used for resource data validation and storage.

    Methods
    -------
    add_or_update_resource_list(resource: DataResource, **kwargs)
        Adds a new resource or updates an existing one in the repository.
    add_to_resource_list(resource: DataResource)
        Adds a new resource to the repository.
    update_resource_list(resource: DataResource)
        Updates an existing resource in the repository.
    get_resource_info(**filters)
        Retrieves resource information based on specified filters.
    add_from_dataframe(data, loc, task_name, task_relation, last_update, **kwargs)
        Adds resource information from a DataFrame.
    get_dataframe_for_task(name, **kwargs)
        Retrieves a DataFrame for a specific task.
    write_dataframe_for_task(data, resource_name, **kwargs)
        Writes a DataFrame to the storage based on resource information.
    write_dataframe_for_resource(data, resource, overwrite)
        Validates and writes a DataFrame to the resource location.
    list_available_resources()
        Lists all available resources in the repository.
    comment_resource(resource, comment)
        Adds a comment to a resource and updates the repository.
    """

    def __init__(self, db_path: str, table_name="resources") -> None:
        """
        Initializes the ResourceRepository with the path to the database and table name.

        Parameters
        ----------
        db_path : str
            The file system path where the CSV database is located.
        table_name : str, optional
            The name of the table, default is 'resources'.
        """
        self.db_path = Path(db_path)
        self.table_name = table_name

        if self.db_path.is_dir():
            self.resources_list_path = self.db_path / (self.table_name + ".csv")
        else:
            self.resources_list_path = self.db_path
        self.schema = DataResource

        csv_resource = DataResource(
            table_name, DataResource.__name__, location=str(self.resources_list_path)
        )
        self.resources_list_path = Path(csv_resource.location)
        self.root_dir = self.resources_list_path.parent.absolute()
        # Initialize CSV file if it does not exist
        if not self.resources_list_path.exists():
            if not self.resources_list_path.parent.exists():
                self.resources_list_path.parent.mkdir(parents=True)
            self.schema.get_empty_dataframe().to_csv(
                self.resources_list_path, index=False
            )

        self.available_resources = load(
            self.resources_list_path, {self.table_name: self.schema}
        )
        # self.df["loc"] = self.df["loc"].apply(lambda x: Path(x))

    def add_or_update_resource_list(self, resource: DataResource, **kwargs) -> None:
        """
        Adds a new resource to the repository or updates it if it already exists.

        Parameters
        ----------
        resource : DataResource
            The resource data to add or update.
        kwargs : dict
            Additional keyword arguments used for extended functionality.
        """

        if self.resource_exists(resource):
            self.update_resource_list(resource)
        else:
            self.add_to_resource_list(resource)

    def add_to_resource_list(self, resource: DataResource) -> None:
        """
        Appends a new resource to the repository.

        Parameters
        ----------
        resource : DataResource
            The resource data to add.
        """
        # Append new record
        new_record = resource.to_pandas()
        self.available_resources = pd.concat(
            [self.available_resources, new_record], ignore_index=True
        )
        self.available_resources.to_csv(self.resources_list_path, index=False)

    def update_resource_list(self, resource: DataResource) -> None:
        """
        Updates an existing resource in the repository.

        Parameters
        ----------
        resource : DataResource
            The resource data to update.
        """
        # Update existing record
        resource_as_dict = resource.to_pandas().squeeze().to_dict()
        cleared_dict = self._clear_resource_dict(resource_as_dict)
        mask = pd.Series([True] * len(self.available_resources))
        for key, value in cleared_dict.items():
            if not value:
                # None values will match with any available resource
                continue
            mask &= self.available_resources[key] == value

        row_index = self.available_resources[mask].index[0]

        for key, value in resource_as_dict.items():
            self.available_resources.at[row_index, key] = value

        self.available_resources.to_csv(self.resources_list_path, index=False)

    def _clear_resource_dict(self, resource_dict: dict):
        resource_dict = resource_dict.copy()
        # drop unnecessary fields
        if "comment" in resource_dict:
            del resource_dict["comment"]
        if "created_by" in resource_dict:
            del resource_dict["created_by"]
        if "license" in resource_dict:
            del resource_dict["license"]
        if "last_update" in resource_dict:
            del resource_dict["last_update"]
        if "license_url" in resource_dict:
            del resource_dict["license_url"]
        if "dag_run_id" in resource_dict:
            del resource_dict["dag_run_id"]

        return resource_dict

    def resource_exists(self, resource: DataResource) -> bool:
        try:
            model_dict = resource.to_pandas().squeeze().to_dict()
            model_dict = self._clear_resource_dict(model_dict)
            self.get_resource_info(**model_dict)
            return True
        except ValueError:
            return False

    def get_latest_version(self, **filters: dict):
        resources = self.get_resource_info(**filters)

        if not isinstance(resources, list):
            return resources

        if len(resources) > 1:

            def compare_version_strings(
                resource1: DataResource, resource2: DataResource
            ):
                try:
                    version1 = semantic_version.Version.coerce(resource1.data_version)
                    version2 = semantic_version.Version.coerce(resource2.data_version)
                    return (version1 > version2) - (version1 < version2)
                except ValueError:
                    # Fallback to regular string comparison if semantic_version fails
                    return (resource1.data_version > resource2.data_version) - (
                        resource1.data_version < resource2.data_version
                    )

            resources = sorted(
                resources, key=cmp_to_key(compare_version_strings), reverse=True
            )

        return resources[0]

    def get_resource_info(self, **filters: dict) -> DataResource | List[DataResource]:
        """
        Retrieves resource information based on specified filters.

        Parameters
        ----------
        filters : dict
            Key-value pairs of attributes to filter the resources by.

        Returns
        -------
        DataResource
            The matched resource data.
        List[DataResource]
            If more than one resource match the filters, a list with all of them is returned

        Raises
        ------
        ValueError
            If no resource is found or if multiple resources are found.
        """
        mask = pd.Series(True, index=self.available_resources.index)

        for k, v in filters.items():
            if not v:
                # None values will match with any available resource
                continue
            # Update the mask to narrow down the rows
            mask = mask & (self.available_resources[k] == v)
        result = self.available_resources[mask]

        if result.empty:
            raise ValueError(f"No resource found with the provided filters: {filters}")

        if len(result.index) > 1:
            results = []
            for _, row in result.iterrows():
                results.append(self._row_to_data_resource(row))
            return results
        else:
            return self._row_to_data_resource(result.iloc[0])

    def add_from_dataframe(
        self,
        data: pd.DataFrame,
        loc: Union[Path, str],
        task_name: str | None = None,
        task_relation: str = "output",
        last_update: date = date.today(),
        **kwargs,
    ) -> DataResource:
        res = DataResource.from_dataframe(
            data,
            loc,
            task_name,
            task_relation=task_relation,
            last_update=last_update,
            **kwargs,
        )
        self.add_or_update_to_list(res)
        return res

    def get_dataframe_for_task(
        self,
        name: str,
        **kwargs,
    ) -> pd.DataFrame:
        res = self.get_resource_info(
            name=name,
            **kwargs,
        )
        assert not isinstance(
            res, list
        ), "Provided information points to more than one resource. Please add more information."
        return load(
            Path(res.location), {Path(res.location).stem: globals()[res.schema_name]}
        )

    def write_dataframe_for_task(
        self,
        data: pd.DataFrame,
        resource_name: str,
        data_version: str,
        overwrite=True,
        **kwargs,
    ):
        try:
            # make sure only relevant fields are used when getting already existing resource
            cleaned_kwargs = self._clear_resource_dict(kwargs)
            resource = self.get_resource_info(name=resource_name, **cleaned_kwargs)

            if isinstance(resource, list):
                raise IndexError(
                    "Resource information is ambiguous. Multiple resources match the given description. Please provide more parameters."
                )
            # update resource based on kwargs
            for key, value in kwargs.items():
                if key == "location":
                    resource.__setattr__("_location", value)
                else:
                    resource.__setattr__(key, value)
        except ValueError:
            resource = DataResource(
                name=resource_name,
                data_version=data_version,
                root_location=self.root_dir,
                **kwargs,
            )

        resource.data_version = data_version
        self.write_dataframe_for_resource(data, resource, overwrite=overwrite)

    def write_dataframe_for_resource(
        self, data: pd.DataFrame, resource: DataResource, overwrite=True
    ):
        schema = globals()[resource.schema_name]

        if self.resource_exists(resource) and not overwrite:
            raise FileExistsError

        save(data, resource.name, Path(resource.location), schema, overwrite)
        self.add_or_update_resource_list(resource)

    def list_available_resources(self) -> list[DataResource]:
        resources = [
            self._row_to_data_resource(row)
            for _, row in self.available_resources.iterrows()
        ]
        return resources

    def comment_resource(self, resource: DataResource, comment: str) -> DataResource:
        resource.append_comment(comment)
        self.add_or_update_resource_list(resource)
        return resource

    def _row_to_data_resource(self, row):
        args = {"root_location": self.root_dir, **row}
        return DataResource(**args)

    def load_with_classification(self, classifications: dict, **kwargs) -> pd.DataFrame:
        set_logger()  # Initialize the logger

        # Retrieve resource information and dataframe for task
        resource_info = self.get_resource_info(**kwargs)
        df_classified = self.get_dataframe_for_task(**kwargs)

        total_deleted_lines = 0  # Initialize the counter for total deleted lines

        for column, classification in classifications.items():
            if column not in df_classified.columns:
                continue  # Skip if the column doesn't exist in the dataframe

            # Handle specific case for 'location' column
            if column == "location" and isinstance(classification, str):
                df_classified[column] = coco.convert(
                    names=df_classified[column], to=classification
                )
            else:
                filtered_classifications, deleted_classifications = (
                    filter_classifications(classification)
                )

                # Log the number of deleted classifications
                logger.info(
                    f"Number of classifications deleted in {column}: {len(deleted_classifications)}"
                )

                if not filtered_classifications.empty:
                    for deleted_classification in deleted_classifications.itertuples(
                        index=False, name="DeletedClassification"
                    ):
                        classification_list = (
                            [deleted_classification[1]]
                            if isinstance(deleted_classification[1], str)
                            else deleted_classification[1]
                        )

                        # Record the number of rows before and after deletion
                        before_delete = len(df_classified)
                        df_classified = df_classified[
                            ~df_classified[column].isin(classification_list)
                        ]
                        after_delete = len(df_classified)

                        deleted_lines = before_delete - after_delete
                        total_deleted_lines += deleted_lines

                        # Log the deletion details
                        logger.info(
                            f"Deleted {deleted_lines} lines for bonsai classification "
                            f"{deleted_classification[0]} with source classification "
                            f"{deleted_classification[1]} in column {column}"
                        )

                    # Generate and apply classification mapping
                    classification_mapping = generate_classification_mapping(
                        filtered_classifications, column, resource_info
                    )

                    # Find and log unmapped classifications
                    original_values = df_classified[column].unique()
                    mapped_values = set(classification_mapping.keys())
                    unmapped_values = set(original_values) - mapped_values

                    if unmapped_values:
                        logger.info(
                            f"Unmapped classifications in column {column}: {unmapped_values}"
                        )

                    df_classified[column] = df_classified[column].map(
                        classification_mapping
                    )

                    # Drop rows with NaN values
                    before_delete = len(df_classified)
                    df_classified = df_classified.dropna(subset=[column])
                    after_delete = len(df_classified)

                    deleted_lines = before_delete - after_delete
                    total_deleted_lines += deleted_lines

                    logger.info(
                        f"Dropped {deleted_lines} rows due to missing classifications"
                    )

        logger.info(f"Total deleted lines: {total_deleted_lines}")
        df_classified = combine_duplicates(df_classified)
        return df_classified

    def load_with_bonsai_classification(self, **kwargs) -> pd.DataFrame:
        resource_info = self.get_resource_info(**kwargs)

        if resource_info.schema_name == "PRODCOMProductionVolume":
            classified = self.load_with_classification(
                {
                    "location": cls.location.datapackage.conc_prodcom_iso_3166_1,
                    "product": cls.flowobject.datapackage.conc_bonsai_prodcom_total_2_0,
                },
                **kwargs,
            )
            classified = convert_location_to_iso3(classified, "ISO3")
        elif resource_info.schema_name == "UNdataEnergyBalance":
            classified = self.load_with_classification(
                {
                    "location": cls.location.datapackage.conc_undata_energy_iso_3166_1,
                    "product": cls.flowobject.datapackage.conc_bonsai_undata_energy_stats,
                },
                **kwargs,
            )
            classified = convert_location_to_iso3(classified, "ISO3")

        return classified

    def harmonize_with_resource(self, dataframe, **kwargs):
        # Load the base DataFrame
        base_df = self.get_dataframe_for_task(**kwargs)

        # Define the columns to check for overlaps
        overlap_columns = ["time", "location", "product", "unit"]

        # Ensure the overlap columns exist in both DataFrames
        for column in overlap_columns:
            if column not in base_df.columns or column not in dataframe.columns:
                raise ValueError(
                    f"Column '{column}' is missing in one of the DataFrames"
                )

        # Concatenate the DataFrames
        combined_df = pd.concat([base_df, dataframe], ignore_index=True)

        # Identify duplicate rows based on overlap columns
        duplicates = combined_df[
            combined_df.duplicated(subset=overlap_columns, keep=False)
        ]
        # TODO handle dublicates somehow. Based on source and uncertainty

        # Find and display duplicate pairs
        duplicate_pairs = (
            combined_df.groupby(overlap_columns).size().reset_index(name="Count")
        )
        duplicate_pairs = duplicate_pairs[duplicate_pairs["Count"] > 1]

        # # Display all duplicate pairs
        # if not duplicate_pairs.empty:
        #     print("Duplicate Pairs:")
        #     print(duplicate_pairs)
        # else:
        #     print("No duplicate pairs found.")

        duplicates_df = duplicates
        unique_df = combined_df.drop_duplicates(subset=overlap_columns, keep=False)
        # TODO check if there is any changes if not then no need to create a new resource

        resource = self.get_latest_version(**kwargs)
        resource.data_version = increment_version(resource.data_version)
        self.write_dataframe_for_resource(unique_df, resource)
