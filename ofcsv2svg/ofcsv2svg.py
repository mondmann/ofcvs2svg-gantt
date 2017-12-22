#!/usr/bin/env python3
# convert omni focus csv to svg gantt
import argparse
import csv
import datetime
import os
from typing import Dict, List

import gantt


class Action(object):
    """
    Attributes: 'task_id', 'type', 'name', 'status', 'project', 'context',
    'start_date', 'due_date', 'completion_date', 'duration', 'flagged', 'notes'
    """

    def __init__(self, data: Dict):
        self.__dict__ = data

    def __str__(self):
        return repr(self.__dict__)


class ActionFactory(object):
    def __init__(self):
        self.__headings = None
        self.__actions = None

    def read_csv(self, filename: str):
        with open(filename, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

            self.__actions = []
            self.__headings = None
            for row in csvreader:
                if self.__headings is None:
                    self.__headings = [h.replace(" ", "_").lower() for h in csvreader.fieldnames]

                if row["Type"] == "Action":
                    data = {}
                    for index, (item_type, item) in enumerate(row.items()):
                        if item_type.endswith("Date"):
                            if len(item) == 0:
                                item = None
                            else:
                                item = datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S %z").date()

                        data[self.__headings[index]] = item
                    self.__actions.append(Action(data))

    @property
    def headings(self):
        return self.__headings

    @property
    def actions(self):
        return self.__actions


def convert(csvfilename: str, svgfilename: str, start: datetime = None, end: datetime = None, nwdays: List[int] = None):
    gantt.define_not_worked_days([] if nwdays is None else nwdays)  # for OmniFocus, every day is a working day
    af = ActionFactory()
    af.read_csv(csvfilename)

    projects = {}
    all_dates = [a.start_date for a in af.actions if a.start_date is not None] + \
                [a.due_date for a in af.actions if a.due_date is not None] + \
                [a.completion_date for a in af.actions if a.completion_date is not None] + \
                [datetime.date.today()]
    start = min(all_dates) if start is None else start
    end = max(all_dates) if end is None else end
    for action in af.actions:
        task_start = action.start_date or start
        task_end = action.completion_date or action.due_date or end

        task = gantt.Task(name=action.name,
                          start=task_start,
                          stop=task_end)

        if action.project not in projects:
            projects[action.project] = gantt.Project(name=action.project)
        projects[action.project].add_task(task)

    mainproject = gantt.Project()
    for project in projects.values():
        mainproject.add_task(project)

    mainproject.make_svg_for_tasks(svgfilename,
                                   start=start,
                                   end=end,
                                   today=datetime.date.today())


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def valid_weekday(s):
    msg = "Not a valid weekday: '{0}'.".format(s)
    exception = argparse.ArgumentTypeError(msg)
    try:
        day = int(s)
        if day not in range(7):
            raise exception
        else:
            return day
    except ValueError:
        raise exception


def main():
    argparser = argparse.ArgumentParser(description="Convert OmniFocus CSV export to GANTT SVG")
    argparser.add_argument("infile", help="Input file in CSV format exported from OmniFocus")
    argparser.add_argument("--outfile", "-o", help="Output filename for SVG document")
    argparser.add_argument("--start", "-s", help="Override start date manually.", type=valid_date, metavar="YYYY-MM-DD")
    argparser.add_argument("--end", "-e", help="Override end date manually.", type=valid_date, metavar="YYYY-MM-DD")
    argparser.add_argument("--notworking", "-n",
                           help="add day of week you are not working (0: monday .. 6: sunday). Default is none. " +
                                "Use multiple times for multiple days (e. g. '-n 5 -n 6' for weekends).",
                           action="append", type=valid_weekday, metavar="N")
    args = argparser.parse_args()

    if args.outfile is not None:
        outfile = args.outfile
    else:
        outfile = os.path.splitext(args.infile)[0] + ".svg"
    convert(args.infile, outfile, start=args.start, end=args.end, nwdays=args.notworking)


if __name__ == "__main__":
    main()
