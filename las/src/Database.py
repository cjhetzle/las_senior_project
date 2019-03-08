import logging
import pickle
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, fname):
        self.fname = fname

    def load_data(self):
        """Loads existing analytic data from the given file.

        Arguments:
          fname: The file name to load
                """
        try:
            with open(self.fname, "rb") as file:
                logger.info("Loading pickle file")
                return pickle.load(file)
        except IOError:
            logger.warning("No data.p file, not importing old data")
        logger.info("Could not read data from file. Returning None")
        return None

    def save_data(self, data):
        """ Saves data as pickle

        Arguments:
          fname: The file name to save the pickle data
        """
        with open(self.fname, "wb") as file:
            pickle.dump(data, file)
