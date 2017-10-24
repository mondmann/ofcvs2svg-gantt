#!/usr/bin/env python3
# convert omni focus csv to svg gantt

from typing import Dict

import csv
import gantt
import datetime
import sys
import os


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


def main(csvfilename: str, svgfilename: str):
    af = ActionFactory()
    af.read_csv(csvfilename)

    projects = {}
    all_dates = [a.start_date for a in af.actions if a.start_date is not None] + \
                [a.due_date for a in af.actions if a.due_date is not None] + \
                [a.completion_date for a in af.actions if a.completion_date is not None] + \
                [datetime.date.today()]
    start = min(all_dates)
    end = max(all_dates)
    for action in af.actions:
        task_start = action.start_date or start
        task_end = action.completion_date or action.due_date or end
        task_duration = (task_end - task_start).days

        task = gantt.Task(name=action.name,
                          start=task_start,
                          duration=task_duration)

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


if len(sys.argv) > 3:
    print("Usage: ofcvs2svg <infile> [<outfile>]")
    exit(1)
else:
    infilename = sys.argv[1]
    if len(sys.argv) == 2:
        outfilename = os.path.splitext(infilename)[0] + ".svg"
    else:
        outfilename = sys.argv[2]

    main(infilename, outfilename)
