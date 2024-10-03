"""Functions for loading data for GlyTrait.

This module provides functions for loading data for GlyTrait.

Classes:
    GlyTraitInputData: Encapsulates all the input data for GlyTrait.

Functions:
    load_input_data: Load all the input data for GlyTrait, including
        abundance table, glycans, and groups.
        Returns a `GlyTraitInputData` object.
"""

from __future__ import annotations

from collections.abc import Iterable, Callable
from typing import Optional, Literal

import pandas as pd
from attrs import define, field
from numpy import dtype

from glytrait.data_type import AbundanceTable, GroupSeries, MetaPropertyTable
from glytrait.exception import DataInputError
from glytrait.glycan import parse_structures, parse_compositions, Structure, Composition

__all__ = [
    "load_abundance",
    "load_groups",
    "load_glycans",
    "load_meta_property",
    "check_all_glycans_have_mp",
    "check_all_glycans_have_struct_or_comp",
    "check_same_samples_in_abund_and_groups",
]


GlycanDict = dict[str, Structure] | dict[str, Composition]


@define
class DFValidator:
    """Validator for pandas DataFrame.

    Attributes:
        must_have: List of column names that must be in the DataFrame.
        unique: List of column names that must be unique in the DataFrame.
        types: Dictionary of column names and their expected types.
        default_type: Default type for columns not in `types`.
    """

    must_have: list[str] = field(kw_only=True, factory=list)
    unique: list[str] = field(kw_only=True, factory=list)
    types: dict[str, str] = field(kw_only=True, factory=dict)
    default_type: dtype | str = field(kw_only=True, default=None)

    def __call__(self, df: pd.DataFrame) -> None:
        """Validate the DataFrame.

        Raises:
            DataInputError: If one of the following conditions is met:
            - The DataFrame does not have all the columns specified in `must_have`.
        """
        self._test_must_have_columns(df)
        self._test_unique_columns(df)
        self._test_type_check(df)
        self._test_default_type(df)

    def _test_must_have_columns(self, df: pd.DataFrame):
        if missing := {col for col in self.must_have if col not in df.columns}:
            msg = f"The following columns are missing: {', '.join(missing)}."
            raise DataInputError(msg)

    def _test_unique_columns(self, df: pd.DataFrame):
        if non_unique := [
            col for col in self.unique if col in df and df[col].duplicated().any()
        ]:
            msg = f"The following columns are not unique: {', '.join(non_unique)}."
            raise DataInputError(msg)

    def _test_type_check(self, df: pd.DataFrame):
        if wrong_type_cols := [
            col
            for col, dtype in self.types.items()
            if col in df and df[col].dtype != dtype
        ]:
            expected = {col: self.types[col] for col in wrong_type_cols}
            got = {col: df[col].dtype for col in wrong_type_cols}
            msg = (
                f"The following columns have incorrect types: {', '.join(wrong_type_cols)}. "
                f"Expected types: {expected}, got: {got}."
            )
            raise DataInputError(msg)

    def _test_default_type(self, df: pd.DataFrame):
        if self.default_type is None:
            return
        cols_to_check = set(df.columns) - set(self.types)
        if wrong_type_cols := [
            col for col in cols_to_check if df[col].dtype != self.default_type
        ]:
            got = {col: df[col].dtype for col in wrong_type_cols}
            msg = (
                f"The following columns have incorrect types: {', '.join(wrong_type_cols)}. "
                f"Expected types: {self.default_type}, got: {got}."
            )
            raise DataInputError(msg)


def load_abundance(df: pd.DataFrame) -> AbundanceTable:
    """Load abundance table from a DataFrame."""
    validator = DFValidator(
        must_have=["Sample"],
        unique=["Sample"],
        types={"Sample": "object"},
        default_type=dtype("float64"),
    )
    validator(df)
    return AbundanceTable(df.set_index("Sample"))


def load_groups(df: pd.DataFrame) -> GroupSeries:
    """Load groups from a DataFrame."""
    validator = DFValidator(
        must_have=["Group", "Sample"],
        unique=["Sample"],
        types={"Sample": "object"},
    )
    validator(df)
    return GroupSeries(df.set_index("Sample")["Group"])


GlycanParserType = Callable[[Iterable[tuple[str, str]]], GlycanDict]


def load_glycans(
    df: pd.DataFrame,
    *,
    mode: Literal["structure", "composition"],
    parser: Optional[GlycanParserType] = None,
) -> GlycanDict:
    """Load glycans from a DataFrame."""
    if parser is None:
        parser = parse_structures if mode == "structure" else parse_compositions
    glycan_col = "Structure" if mode == "structure" else "Composition"
    validator = DFValidator(
        must_have=["GlycanID", glycan_col],
        unique=["GlycanID", glycan_col],
        types={"GlycanID": "object", glycan_col: "object"},
    )
    validator(df)
    ids = df["GlycanID"].to_list()
    glycan_col = mode.capitalize()
    strings = df[glycan_col].to_list()
    return parser(zip(ids, strings))


def load_meta_property(df: pd.DataFrame) -> MetaPropertyTable:
    """Load meta-property table from a DataFrame."""
    validator = DFValidator(
        must_have=["GlycanID"], unique=["GlycanID"], types={"GlycanID": "object"}
    )
    validator(df)
    return MetaPropertyTable(df.set_index("GlycanID"))


def check_same_samples_in_abund_and_groups(
    abundance_df: pd.DataFrame,
    groups: pd.Series,
) -> None:
    """Check if the abundance table and the groups have the same samples.

    Args:
        abundance_df: Abundance table as a pandas DataFrame.
        groups: Sample groups as a pandas Series.

    Raises:
        DataInputError: If the samples in the abundance table and the groups are different.
    """
    abund_samples = set(abundance_df.index)
    groups_samples = set(groups.index)
    if abund_samples != groups_samples:
        samples_in_abund_not_in_groups = abund_samples - groups_samples
        samples_in_groups_not_in_abund = groups_samples - abund_samples
        msg = ""
        if samples_in_abund_not_in_groups:
            msg += (
                f"The following samples are in the abundance table but not in the groups: "
                f"{', '.join(samples_in_abund_not_in_groups)}."
            )
        if samples_in_groups_not_in_abund:
            msg += (
                f"The following samples are in the groups but not in the abundance table: "
                f"{', '.join(samples_in_groups_not_in_abund)}."
            )
        raise DataInputError(msg)


def check_all_glycans_have_struct_or_comp(
    abundance_df: pd.DataFrame,
    glycans: GlycanDict,
) -> None:
    """Check if all glycans in the abundance table have structures or compositions.

    Glycans in the structure or composition dict but not in the abundance table
    are not checked.

    Args:
        abundance_df: Abundance table as a pandas DataFrame.
        glycans: Glycans, either a dict of `Structure` objects or a dict of `Composition` objects.

    Raises:
        DataInputError: If any glycan in the abundance table does not
            have a structure or composition.
    """
    abund_glycans = set(abundance_df.columns)
    glycan_names = set(glycans.keys())
    if diff := abund_glycans - glycan_names:
        msg = (
            f"The following glycans in the abundance table do not have structures or "
            f"compositions: {', '.join(diff)}."
        )
        raise DataInputError(msg)


def check_all_glycans_have_mp(
    abundance_df: pd.DataFrame, mp_table: MetaPropertyTable
) -> None:
    """Check if all glycans in the abundance table have meta-properties.

    Glycans in the MP table but not in the abundance table are not handled.

    Args:
        abundance_df: Abundance table as a DataFrame.
        mp_table: The meta-property table as a DataFrame.

    Raises:
        DataInputError: If any glycans are missing in the MP table.
    """
    abund_glycans = set(abundance_df.columns)
    mp_glycans = set(mp_table.index)
    if diff := abund_glycans - mp_glycans:
        msg = (
            f"The following glycans in the abundance table do not have "
            f"meta properties: {', '.join(diff)}."
        )
        raise DataInputError(msg)
