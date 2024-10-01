# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientEnsureRowsParams", "Row", "RowCell", "RowRow"]


class ClientEnsureRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    rows: Required[Iterable[Row]]


class RowCell(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]
    """The column's name or system ID."""

    cell_id: Annotated[str, PropertyInfo(alias="cellId")]

    value: object


class RowRow(TypedDict, total=False):
    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]

    is_template: Annotated[bool, PropertyInfo(alias="isTemplate")]


class Row(TypedDict, total=False):
    cells: Iterable[RowCell]

    row: RowRow

    row_id: Annotated[str, PropertyInfo(alias="rowId")]
