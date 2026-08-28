from dataclasses import dataclass

import pytest

from cadence._internal.workflow.search_attributes import (
    search_attributes_from_proto,
    search_attributes_to_proto,
)
from cadence.data_converter import DefaultDataConverter


def test_search_attributes_to_proto_none() -> None:
    dc = DefaultDataConverter()
    assert search_attributes_to_proto(dc, None) is None


def test_search_attributes_to_proto_empty_dict() -> None:
    dc = DefaultDataConverter()
    assert search_attributes_to_proto(dc, {}) is None


def test_search_attributes_to_proto_single_key_matches_to_data() -> None:
    dc = DefaultDataConverter()
    proto = search_attributes_to_proto(dc, {"k": "v"})
    assert proto is not None
    assert list(proto.indexed_fields.keys()) == ["k"]
    assert proto.indexed_fields["k"] == dc.to_data(["v"])


def test_search_attributes_to_proto_multiple_keys() -> None:
    dc = DefaultDataConverter()
    proto = search_attributes_to_proto(dc, {"a": 1, "b": "two", "c": True})
    assert proto is not None
    assert proto.indexed_fields["a"] == dc.to_data([1])
    assert proto.indexed_fields["b"] == dc.to_data(["two"])
    assert proto.indexed_fields["c"] == dc.to_data([True])


@dataclass
class _Sample:
    x: int
    y: str


def test_search_attributes_round_trip() -> None:
    dc = DefaultDataConverter()
    original = {"CustomIntField": 2, "CustomKeywordField": "seattle"}
    proto = search_attributes_to_proto(dc, original)
    assert proto is not None
    assert search_attributes_from_proto(dc, proto) == original


def test_search_attributes_to_proto_encoding_error_propagates() -> None:
    dc = DefaultDataConverter()
    with pytest.raises(Exception):
        search_attributes_to_proto(dc, {"bad": object()})
