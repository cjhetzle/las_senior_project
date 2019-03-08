
from datetime import datetime, timedelta
import logging
import random

import numpy as np
from src.datastructures import Frequency
from src.SchedulingAlgorithm import SchedulingAlgorithm

logger = logging.getLogger(__name__)


@SchedulingAlgorithm.register
class RandomScheduling:
    SEC_PER_MIN = 60
    SEC_PER_HOUR = 60 * SEC_PER_MIN
    SEC_PER_DAY = 24 * SEC_PER_HOUR
    SEC_PER_WEEK = 7 * SEC_PER_DAY

    def __init__(self, period):
        self.period = period
        self.schedule = []
        # Create an array that represents load in a one minute slice
        self.current_load = np.array([0] * self.period, dtype=np.float64)

    def build_schedule(self, analytics, load):
        dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # Create a list of tupleas (analytic name, time to execute at)
        # Divide the analytics into their given frequency

        # maybe this should be somewhere else?
        hourly = []
        daily = []
        weekly = []
        for analytic in analytics:
            if analytic.run_frequency == Frequency.HOUR:
                hourly.append(analytic)
            elif analytic.run_frequency == Frequency.DAY:
                daily.append(analytic)
            else:
                weekly.append(analytic)

        # Iterate over hourly analytics first
        for analytic in hourly:
            self.place(analytic, RandomScheduling.SEC_PER_HOUR, dt)

        for analytic in daily:
            self.place(analytic, RandomScheduling.SEC_PER_DAY, dt)

        for analytic in weekly:
            self.place(analytic, RandomScheduling.SEC_PER_WEEK, dt)

        return self.schedule

    # Interval is defined in number of minutes
    def place(self, analytic, interval, dt):
        # Iterate over the daily sections we need to schedule
        for i in range(0, self.period, interval):
            # Select a random time slice to place the job in.
            # TODO: Add logic to only place the job where it
            # can be reasonable completed within the day
            offset = random.randint(i, i + interval)
            # Place the block in that time slice by adding
            # it's "load" to the load array
            # TODO: Verify addition logic here. casting
            # analytic.average_time to int seems bad
            self.current_load[i + offset: i + offset +
                              int(analytic.average_time)] \
                += analytic.average_load
            # Add execution to schedule list
            self.schedule.append((analytic.analytic_id,
                                 (dt + timedelta(minutes=offset)).timestamp()))
