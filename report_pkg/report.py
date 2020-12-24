import datetime
import argparse
import sys
import os
from dataclasses import dataclass


@dataclass
class PilotStats:
    abbreviation: str
    position: int
    name: str
    team: str
    fastest_lap: datetime.timedelta


abbreviations = "abbreviations.txt"
end = "end.log"
start = "start.log"


def build_report(file):
    """
    Take params and returned report of qualification

    :param file: folder path
    :return: report list
    """
    pilots = {}
    lap_times = {}
    report = []
    with open(os.path.join(file, abbreviations)) as abb_file:
        for line in abb_file.read().split("\n"):
            abbreviation, name, team = line.split("_")
            pilots[abbreviation] = (name, team,)
    with open(os.path.join(file, end))as end_file:
        for line in end_file.read().split("\n"):
            abbreviation = line[:3]
            end_datetime = line[3:]
            lap_times[abbreviation] = datetime.datetime.fromisoformat(end_datetime)
    with open(os.path.join(file, start)) as start_file:
        for line in start_file.read().split("\n"):
            abbreviation = line[:3]
            start_datetime = line[3:]
            lap_times[abbreviation] -= datetime.datetime.fromisoformat(start_datetime)
    sorted_laps = list(lap_times.items())
    sorted_laps.sort(key=lambda i: i[1])
    for position, abbr_time_tuple in enumerate(sorted_laps, 1):
        abbreviation, lap_time = abbr_time_tuple
        name, team = pilots[abbreviation]
        fastest_lap = lap_time
        report.append(PilotStats(abbreviation, position, name, team, fastest_lap))
    return report


def format_delta(timedelta):
    if timedelta.microseconds == 0:
        mic = "000"
    else:
        mic = str(timedelta)[-6:-3]
    sec = timedelta.seconds
    minutes, seconds = divmod(sec, 60)
    string = "{}:{}.{:>3}".format(minutes, seconds, mic)
    return string


def print_report(report, driver=None, desc=False):
    """
    Print report to stdout

    :param report: report of qualification result
    :param driver: name of driver whose statistic you wish to show
    :param desc: order descending
    :return: None
    """
    separator = "-" * 70
    if driver:
        printer = [line for line in report if line.name == driver]
    elif desc:
        separator_line_num = -15
        printer = report[::-1]
        printer.insert(separator_line_num, separator)
    else:
        separator_line_num = 15
        printer = report[:]
        printer.insert(separator_line_num, separator)
    for line in printer:
        if isinstance(line, PilotStats):
            print("{:>2}. {:<20}| {:<30}| {}".format(line.position, line.name,
                                                     line.team, format_delta(line.fastest_lap)))
        else:
            print(line)


def input_from_argparse(cl_args):
    """
    Parse args from command line

    :return: args
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands',
                                       help='Name of driver whose statistics you wish to watch')
    parser.add_argument("-f", "--file", type=str, help="Folder path")
    parser_driver = subparsers.add_parser("driver", help="Name")
    parser_driver.add_argument("driver", type=str)
    group.add_argument("--asc", action="store_true", help="Order by time asc")
    group.add_argument("--desc", action="store_true", help="Order by time desc")
    args = parser.parse_args(cl_args)
    return args


def main():
    """
    Main func 

    :return: none
    """
    args = input_from_argparse(sys.argv[1:])
    report = build_report(args.file)
    if "driver" in args:
        print_report(report, driver=args.driver)
    else:
        print_report(report, desc=args.desc)


if __name__ == "__main__":
    main()
