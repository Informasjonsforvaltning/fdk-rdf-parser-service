from typing import Any, List

import pytest

from fdk_rdf_parser_service.parser.rdf_utils import string_to_float
from fdk_rdf_parser_service.parser.reference_data.utils import remove_none_values


@pytest.mark.unit
def test_string_to_float() -> None:
    assert string_to_float("3.14") == float(3.14)
    assert string_to_float("3,14") == float(3.14)
    assert string_to_float("314") == float(314)
    assert string_to_float("asdfg") is None
    assert string_to_float("3,000.14") == float(3000.14)
    assert string_to_float("3,000,14") is None
    assert string_to_float("3.000,14") == float(3000.14)
    assert string_to_float("3,000.000,14") is None
    assert string_to_float("3,000.000,14") is None


@pytest.mark.unit
def test_remove_none() -> None:
    input_list1 = [1, 2, 3, None, 4, None, 5]
    input_list2 = [None, None, None]
    expected1 = [1, 2, 3, 4, 5]
    expected2: List[Any] = []
    assert remove_none_values(input_list1) == expected1
    assert remove_none_values(input_list2) == expected2
