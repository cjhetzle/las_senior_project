#!/usr/bin/env python3
from collections import defaultdict

import csv
import importlib
import logging

import sys

import numpy as np

from src.BlockingAlgorithm import BlockingAlgorithm
from src.Database import Database
from src.datastructures import Analytic
from src.LogParser import LogParser
from src.RandomScheduling import RandomScheduling
logger = logging.getLogger(__name__)


class Scheduler:
    """The list of analytics"""
    analytics = defaultdict(Analytic)

    def __init__(self):
        if len(sys.argv) < 4:
            logger.error("Usage: {} IN.csv Func.py [0-1 Algorithm] [*.log]"
                         .format(sys.argv[0]))
            sys.exit(1)

        self.schedule = []
        self.input_file = sys.argv[1]
        self.load_function_file = sys.argv[2]
        try:
            self.load_module = importlib.import_module(self.load_function_file
                                                       .replace('.py', ''))
            # for name in dir(self.load_module):
            #    print(getattr(self.load_module, name))
            logger.info("Load function loaded")
        except ImportError:
            logger.error("Import error")
        self.algorithm_type = sys.argv[3]
        self.log_files = sys.argv[4:]
        self.input_analytics = []
        self.schedule = []
        self.database = Database("data.p")

    def main(self):
        # Loads existing data
        data = self.database.load_data()
        if data is not None:
            self.analytics = data

        # Read new logs and merge them into each analytic
        [
            self.analytics[id].merge_run(run)
            for id, run
            in LogParser.parse_log_files(self.log_files)
        ]
        # Assign the id of the dictionary to the analytic
        for id in self.analytics.keys():
            self.analytics[id].analytic_id = id

        # Saves the loaded analytic data
        self.database.save_data(self.analytics)

        # Load CSV of jobs to get frequency
        self.load_analytic_list(self.input_file)

        # Call scheduler
        if (self.algorithm_type == '0'):
            logger.info("***Random Scheduling has been chosen")
            self.scheduling_algorithm = RandomScheduling(7 * 24 * 60 * 60)
        else:
            logger.info("***Block Scheduling has been chosen")
            self.scheduling_algorithm = BlockingAlgorithm(7 * 24 * 60 * 60)
        # TODO: Map the analytics with something along the lines of:
        # [self.analytics[i] for i in self.input_analytics] (filter by input)
        self.schedule = self.scheduling_algorithm \
                            .build_schedule(self.analytics.values(),
                                            self.load_module)
        logger.info("Built schedule")
        logger.debug("Schedule: {}".format(self.schedule))

        # Create schedule CSV
        self.schedule = self.scheduling_algorithm.schedule
        self.write_schedule()
        # TODO: Remove random save
        print("Max: {}".format(max(self.scheduling_algorithm.current_load)))
        np.save("schedule.npy", self.scheduling_algorithm.current_load)

    def load_analytic_list(self, file_path):
        """ Loads in the CSV of analytics.

        Arguments:
          file_path: the relative path of the .csv
          list of analytics that will be scheduled
            """
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                self.analytics[row[0]].run_frequency = row[2]
                logger.info("Analytic ID:" + row[0] + " Frequency: " + row[1])

    def write_schedule(self):
        """ Writes the schedule to a CSV file
            named schedule.csv.
        """
        with open('schedule.csv', 'w') as csv_file:
            schedule_writer = csv.writer(csv_file,
                                         delimiter=',',
                                         quotechar='"',
                                         quoting=csv.QUOTE_MINIMAL)
            for analytic in self.schedule:
                schedule_writer.writerow(list(analytic))
