#!/usr/bin/env python3
import os
from src.Scheduler import Scheduler
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.main()
