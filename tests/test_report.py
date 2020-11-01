import pytest
import argparse
import collect_framework
from unittest import mock


@pytest.mark.parametrize("string, expected", [
        ("qwwertt", 3),
        ("zxc", 3),
        ("asdasdasd", 0),
        ("q1w2e3", 6),
        ("qq11w2ee33", 2),
        ("asdasdasd", 0),
        ("q1w2e3", 6)
    ])
def test_typical(string, expected):
    assert collect_framework.get_number_of_unique(string) == expected


@pytest.mark.parametrize("item", [[], {}, None, True, 123])
def test_atypical(item):
    with pytest.raises(TypeError):
        collect_framework.get_number_of_unique(item)


def test_cache():
    with mock.patch("collect_framework.collections.Counter") as mock_counter:
        strings = ["qweqweq", "asdasdfc", "qweqweq"]
        for string in strings:
            collect_framework.get_number_of_unique(string)
        assert mock_counter.call_count == 2


def test_read():
    with mock.patch("builtins.open", mock.mock_open(read_data="asdccv\nxcv")) as mock_file:
        args = argparse.Namespace(string="asd", file="strings.txt")
        assert collect_framework.output(args) == [("asdccv", 4), ("xcv", 3), ("asd", 3)]
        mock_file.assert_called_with("strings.txt")


def test_argparse():
    with mock.patch("argparse.ArgumentParser.parse_args",
                    return_value=argparse.Namespace(string="asdasdd", file="strings.txt")) as mock_args:
        res = collect_framework.inp()
        assert res == argparse.Namespace(string="asdasdd", file="strings.txt")
        mock_args.assert_called_with()
