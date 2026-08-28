"""Convert user search-attribute maps to/from protobuf SearchAttributes."""

from __future__ import annotations

from typing import Any, Mapping

from cadence.api.v1 import common_pb2
from cadence.data_converter import DataConverter


def search_attributes_to_proto(
    data_converter: DataConverter,
    attributes: Mapping[str, Any] | None,
) -> common_pb2.SearchAttributes | None:
    """Serialize ``attributes`` to protobuf, or ``None`` if none were provided.

    Each value is encoded as a single-element list via the data converter,
    matching memo encoding and Go/Java SDK JSON-per-key behavior.
    """
    if not attributes:
        return None
    out = common_pb2.SearchAttributes()
    for key, value in attributes.items():
        out.indexed_fields[key].CopyFrom(data_converter.to_data([value]))
    return out


def search_attributes_from_proto(
    data_converter: DataConverter,
    attributes: common_pb2.SearchAttributes,
) -> dict[str, Any]:
    """Deserialize protobuf search attributes back to a plain dict."""
    return {
        key: data_converter.from_data(payload, [None])[0]
        for key, payload in attributes.indexed_fields.items()
    }
