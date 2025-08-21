import pytest
import star as st

@pytest.fixture
def array():
    data = ["apple", "banana", "carrot", "date", "egg"]
    return st.Array(data)


# --- case int ---
def test_get_by_int(array):
    result = array[1]
    assert result.data == ["banana"]


# --- case str ---
def test_get_by_exact_str(array):
    result = array["apple"]
    assert result.data == ["apple"]

def test_get_by_prefix_str(array):
    result = array["app"]
    assert result.data == ["app"]


# --- case Slice ---
def test_slice_int_start(array):
    result = array[1:]
    assert result.data == ["pple"]

def test_slice_str_start(array):
    result = array["apple":]
    assert result.data == ["apple"]
    result = array["pl":]
    assert result.data == ["ple"]

def test_slice_int_end(array):
    result = array[:1:]
    assert result.data == ["a"]
    assert len(result.data) == 1

def test_slice_str_end(array):
    result = array[:"apple":]
    assert result.data == [""]
    result = array[:"ple":]
    assert result.data == ["ap"]

def test_slice_int_range(array):
    result = array[1:5:]
    assert result.data == ["pple"]
    assert len(result.data[0]) == 4

def test_slice_str_range(array):
    result = array["ap":"le":]
    assert result.data == ["app"]

def test_slice_int_with_step(array):
    result = array[1:3:2]
    assert result.data == ["p"]

def test_slice_str_with_step(array):
    result = array["a":"e":1]
    assert result.data == ["appl"]
    result = array["a":"e":2]
    assert result.data == ["apl"]

def test_index_plus_slice(array):
    result = array[2]["a":"e":1]
    assert result.data == []
    result = array[2][1:4:2]
    assert result.data == ["ar"]

def test_slice_tuple(array):
    result = array["a":"e":1, 2]
    assert result.data == ["appl", "carrot"]

# TODO: test tuple indexing



