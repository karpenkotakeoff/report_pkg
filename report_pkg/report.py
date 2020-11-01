import datetime
import argparse
import sys


def build_report(folder, driver=None, desc=False):
    """
    Take params and returned report of qualification or driver statistic

    :param folder: folder path
    :param driver: name of driver whose statistic you wish to show
    :param desc: order descending
    :return: report list
    """
    pilots = {}
    lap_times = {}
    report = []
    with open(f"{folder}/abbreviations.txt") as abb:
        for line in abb.read().split("\n"):
            split_line = line.split("_")
            abbreviation = split_line[0]
            name = split_line[1]
            team = split_line[2]
            pilots[abbreviation] = (name, team,)
    with open(f"{folder}/end.log") as end:
        for line in end.read().split("\n"):
            abbreviation = line[:3]
            end_datetime = line[3:]
            lap_times[abbreviation] = datetime.datetime.fromisoformat(end_datetime)
    with open(f"{folder}/start.log") as start:
        for line in start.read().split("\n"):
            abbreviation = line[:3]
            start_datetime = line[3:]
            lap_times[abbreviation] -= datetime.datetime.fromisoformat(start_datetime)
    sorted_laps = list(lap_times.items())
    sorted_laps.sort(key=lambda i: i[1])
    for i in range(len(sorted_laps)):
        position = i + 1
        name = pilots[sorted_laps[i][0]][0]
        team = pilots[sorted_laps[i][0]][1]
        fastest_lap = str(sorted_laps[i][1])[3:-3]
        if i == 15:
            report.append("--------------------------------------------------------------------")
            report.append((position, name, team, fastest_lap,))
        else:
            report.append((position, name, team, fastest_lap,))
    if driver:
        return [line for line in report if line[1] == driver]
    elif desc:
        report.reverse()
        return report
    else:
        return report


def print_report(report):
    """
    Print report to stdout

    :param report: report of qualification result
    :return: None
    """
    for line in report:
        if not isinstance(line, tuple):
            print(line)
        else:
            position, name, team, time = line
            print("{:>2}. {:<20}| {:<30}| {}".format(position, name, team, time))


def inp():
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
    args = inp()
    report = build_report(args.file, args.driver, args.desc)
    print_report(report)


if __name__ == "__main__":
    main()
