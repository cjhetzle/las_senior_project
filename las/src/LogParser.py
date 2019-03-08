import re
import logging
from src.datastructures import Job, Run, FIELDS

logger = logging.getLogger(__name__)


class LogParser:
    @staticmethod
    def parse_log_files(logs):
        """ Returns a list of runs parsed from the log file.

        Returns:
          List of runs given in the constructor.
        """
        # Double chain because parse_log returns a list of runs,
        # not a single run
        return [LogParser.parse_log(i) for i in logs]

    @staticmethod
    def parse_log(log_file_name):
        """ Parses a log file given a name.

        Arguments:
          log_file_name: The name of the log file to read

        Returns:
          Run: The run of the given log file
        """
        with open(log_file_name, 'r') as log_file:
            # The name of the analytic being read
            analytic_name = log_file_name
            # The list of runs in this log file
            process_job = False
            run = Run()
            for line in log_file:

                # Ignore whitespace lines and end processing
                if re.match(r'^\s*$', line):
                    process_job = False
                    continue

                # Start processing if the fields match
                if re.match(r'\s+'.join(FIELDS), line):
                    process_job = True
                    continue

                # Get the runtime of the script in milliseconds
                if re.search(r'Pig script completed in', line):
                    # TODO: Remove magic number. Needed to convert to minutes
                    # TODO: Do not fail when match not found
                    run.runtime = int(re.match(r'.+\((\d+)\s+ms\)\s*$', line).group(1))/60000

                if process_job:
                    job = Job()
                    tokens = re.split(r'\s+', line.strip())
                    [
                        setattr(job, key, value)
                        for key, value
                        in zip(FIELDS, tokens)
                    ]
                    run.jobs.append(job)
            run.compute_statistics()
            return (analytic_name, run)
