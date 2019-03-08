import logging
from enum import Enum
logger = logging.getLogger(__name__)

FIELDS = [
    "JobId", "Maps", "Reduces", "MaxMapTime", "MinMapTime", "AvgMapTime", "MedianMapTime", "MaxReduceTime",
    "MinReduceTime", "AvgReduceTime", "MedianReducetime", "Alias", "Feature", "Outputs"
]


class Frequency(Enum):
    UNDEFINED = 0
    HOUR = 1
    DAY = 2
    WEEK = 3


class Analytic:
    def __init__(self):
        self.runs = []
        self.run_frequency = Frequency.UNDEFINED
        self.script_path = ""
        self.analytic_id = "Undefined"
        self.average_load = 0
        self.average_time = 0

    # TODO: Change to merge runs
    def merge_run(self, run):
        self.runs.append(run)
        self.compute_statistics()

    def compute_statistics(self):
        if len(self.runs) == 0:
            return
        # Limit to 100 runs
        self.runs = self.runs[:100]
        self.average_load = sum([run.avg_load for run in self.runs]) / len(self.runs)
        self.average_time = sum([run.runtime for run in self.runs]) / len(self.runs)

    def __str__(self):
        return "Analytic runs: {}".format(self.runs)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()


class Run:
    def __init__(self):
        self.runtime = 0
        self.jobs = []
        self.log_file_name = ""
        self.avg_maps = 0
        self.avg_reduces = 0
        self.max_map_time = 0
        self.min_map_time = 0
        self.avg_map_time = 0
        self.median_map_time = 0
        self.max_reduce_time = 0
        self.min_reduce_time = 0
        self.avg_reduce_time = 0
        self.median_reduce_time = 0
        self.total_time = 0
        self.avg_load = 0

    def compute_statistics(self):
        if len(self.jobs) == 0:
            return
        self.avg_maps = sum([int(job.Maps) for job in self.jobs]) / len(self.jobs)
        self.avg_reduces = sum([int(job.Reduces) for job in self.jobs]) / len(self.jobs)
        self.avg_map_time = sum([int(job.AvgMapTime) for job in self.jobs]) / len(self.jobs)
        self.avg_reduce_time = sum([int(job.AvgReduceTime) for job in self.jobs]) / len(self.jobs)
        # TODO: Change based on which statistic we're testing/make this dynamic at runtime
        self.avg_load = self.avg_maps

    # Required to print out a run
    def __str__(self):
        return "{} jobs: {}".format(self.log_file_name, self.jobs)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()


class Job:
    def __init__(self):
        [setattr(self, key, "") for key in FIELDS]

    # Required to print out a job
    def __str__(self):
        return str({key: getattr(self, key) for key in FIELDS})

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()
