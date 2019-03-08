import logging
from datetime import datetime, timedelta

import numpy as np

from src.SchedulingAlgorithm import SchedulingAlgorithm
from src.datastructures import Frequency
logger = logging.getLogger(__name__)


@SchedulingAlgorithm.register
class BlockingAlgorithm:
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
        logger.info("Analytic lists created")

        # populate the analytic lists
        for analytic in analytics:
            if analytic.run_frequency == Frequency.HOUR:
                hourly.append(analytic)
            elif analytic.run_frequency == Frequency.DAY:
                daily.append(analytic)
            else:
                weekly.append(analytic)
        logger.info("Analytic lists populated")

        # Order the list from largest to smallest
        hourly = sorted(hourly, key=lambda analytic:
                        analytic.average_load, reverse=True)
        daily = sorted(daily, key=lambda analytic:
                       analytic.average_load, reverse=True)
        weekly = sorted(weekly, key=lambda analytic:
                        analytic.average_load, reverse=True)
        logger.info("Analytic lists sorted Largest > Smallest")

        # Iterate over hourly analytics first
        for analytic in hourly:
            self.place(analytic, BlockingAlgorithm.SEC_PER_HOUR, dt, load)
        logger.info("Placed all hourly jobs")
        for analytic in daily:
            self.place(analytic, BlockingAlgorithm.SEC_PER_DAY, dt, load)
        logger.info("Placed all daily jobs")
        for analytic in weekly:
            self.place(analytic, BlockingAlgorithm.SEC_PER_WEEK, dt, load)
        logger.info("Placed all weekly jobs")
        return self.schedule

    # Interval is defined in number of minutes
    def place(self, analytic, interval, dt, desired_load):
        # Iterate over the daily sections we need to schedule
        for i in range(0, self.period, interval):
            # Select a random time slice to place the job in.
            # TODO: Add logic to only place the job where
            # it can be reasonable completed within the day

            offset = 0
            min = sum(self.current_load[i: i + int(analytic.average_time)])

            # this is to find the smallest sum of load in a given interval
            for j in range(1, interval - int(analytic.average_time)):
                t_min = sum(self.current_load[
                            i + j: i + j + int(analytic.average_time)])
                t_min = self.availability(j, int(analytic.average_time),
                                          desired_load)
                if (t_min > min):
                    offset = j
                    min = t_min

            # Place the block in that time slice by
            # adding it's "load" to the load array
            logger.info("Stats:")
            logger.debug(analytic)
            logger.debug("ID: " + str(analytic.analytic_id))
            logger.debug("AL: " + str(analytic.average_load))
            logger.debug("AT: " + str(analytic.average_time))
            logger.debug("CL: " + str(self.current_load))
            # TODO: Verify addition logic here. casting
            # analytic.average_time to int seems bad
            self.current_load[i + offset: i + offset +
                              int(analytic.average_time)] \
                += analytic.average_load
            # Add execution to schedule list
            self.schedule.append((analytic.analytic_id, (dt +
                                 timedelta(minutes=offset)).timestamp()))

    def availability(self, start, end, desired_load):
        """ """
        sum = 0
        for i in range(start, end + 1):
            sum += desired_load.load_function(i)
        return sum
