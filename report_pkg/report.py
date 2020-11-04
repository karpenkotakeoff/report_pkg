import datetime
import argparse
import sys
import os
from dataclasses import dataclass


@dataclass
class PilotStats:
    position: int
    name: str
    team: str
    fastest_lap: str


abbreviations = "abbreviations.txt"
end = "end.log"
start = "start.log"


def build_report(folder):
    """
    Take params and returned report of qualification

    :param folder: folder path
    :return: report list
    """
    pilots = {}
    lap_times = {}
    report = []
    with open(os.path.join(folder, abbreviations)) as abb_file:
        for line in abb_file.read().split("\n"):
            abbreviation, name, team = line.split("_")
            pilots[abbreviation] = (name, team,)
    with open(os.path.join(folder, end))as end_file:
        for line in end_file.read().split("\n"):
            abbreviation = line[:3]
            end_datetime = line[3:]
            lap_times[abbreviation] = datetime.datetime.fromisoformat(end_datetime)
    with open(os.path.join(folder, start)) as start_file:
        for line in start_file.read().split("\n"):
            abbreviation = line[:3]
            start_datetime = line[3:]
            lap_times[abbreviation] -= datetime.datetime.fromisoformat(start_datetime)
    sorted_laps = list(lap_times.items())
    sorted_laps.sort(key=lambda i: i[1])
    for position, abbr_time_tuple in enumerate(sorted_laps, 1):
        abbreviation, lap_time = abbr_time_tuple
        name, team = pilots[abbreviation]
        fastest_lap = format_delta(lap_time)
        report.append(PilotStats(position, name, team, fastest_lap))
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
    if len(report) > 15:
        separator = "---------------------------------------------------------------------"
        report.insert(15, separator)
    if driver:
        printer = [line for line in report if line.name == driver]
    elif desc:
        printer = [line for line in report[::-1]]
    else:
        printer = report
    for line in printer:
        if not isinstance(line, PilotStats):
            print(line)
        else:
            print("{:>2}. {:<20}| {:<30}| {}".format(line.position, line.name,
                                                     line.team, line.fastest_lap))


def input_from_argparse():
    """
    Parse args from command line

    :return: args
    """
    arguments = ['--' + arg if arg == "driver" else arg for arg in sys.argv[1:]]
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-f", "--file", type=str, help="Folder path")
    group.add_argument("--asc", action="store_true", help="Order by time asc")
    group.add_argument("--desc", action="store_true", help="Order by time desc")
    parser.add_argument("--driver", help="Enter name of driver", type=str)
    args = parser.parse_args(arguments)
    return args


def main():
    """
    Main func 

    :return: none
    """
    args = input_from_argparse()
    report = build_report(args.file)
    print_report(report, args.driver, args.desc)


if __name__ == "__main__":
    main()
