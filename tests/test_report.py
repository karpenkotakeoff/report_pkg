import pytest
import argparse
import report_pkg
from unittest import mock

abbreviations = """DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
LHM_Lewis Hamilton_MERCEDES"""
end = """LHM2018-05-24_12:19:32.585
SVF2018-05-24_12:04:11.332
DRR2018-05-24_12:12:36.080"""
start = """SVF2018-05-24_12:02:58.917
DRR2018-05-24_12:11:24.067
LHM2018-05-24_12:18:20.125"""
report = [report_pkg.PilotStats(abbreviation="DRR", position=1, name='Daniel Ricciardo',
                                team='RED BULL RACING TAG HEUER', fastest_lap='1:12.013'),
          report_pkg.PilotStats(abbreviation="SVF", position=2, name='Sebastian Vettel',
                                team='FERRARI', fastest_lap='1:12.415'),
          report_pkg.PilotStats(abbreviation="LHM", position=3, name='Lewis Hamilton',
                                team='MERCEDES', fastest_lap='1:12.460')]
reversed_report = report[::-1]
print_asc = [
    mock.call(" 1. Daniel Ricciardo    | RED BULL RACING TAG HEUER     | 1:12.013"),
    mock.call(" 2. Sebastian Vettel    | FERRARI                       | 1:12.415"),
    mock.call(" 3. Lewis Hamilton      | MERCEDES                      | 1:12.460")]
print_vettel = [mock.call(" 2. Sebastian Vettel    | FERRARI                       | 1:12.415")]
input_data = [abbreviations, end, start]


def test_typical_build_report():
    with mock.patch('builtins.open') as patched_open:
        patched_open.side_effect = [mock.mock_open(read_data=text)() for text in input_data]
        assert report_pkg.build_report("data") == report


def test_argparse():
    a = ["--file", "data", "driver", "Sebastian Vettel"]
    assert report_pkg.input_from_argparse(a) == argparse.Namespace(asc=False, desc=False,
                                                                   driver="Sebastian Vettel", file="data")


@pytest.mark.parametrize("params, expected", [
    ((report, None, False,), print_asc),
    ((report, None, True,), print_asc[::-1]),
    ((report, "Sebastian Vettel", False), print_vettel),
])
def test_print_report(params, expected):
    with mock.patch('builtins.print') as patched_print:
        report_pkg.print_report(*params)
        assert patched_print.call_args_list == expected
