#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The `pygrabber` package provides a distributed job scheduling system based on a master-grabber architecture.

This package consists of two main scripts:
- `grabmaster.py`: A Python script that manages the job queue and schedules job execution by grabbers.
- `grabber.py`: A Python script that fetches jobs from the queue and executes them.

Both scripts rely on a shared file system for communication and coordination between grabbers.

This package also includes a `Dockerfile` and `docker-compose.yaml` to run the grabmaster and one grabber in a Docker container.

Author: Meir Michanie
Email: meirm@riunx.com
License: MIT
"""

import os
import sys
import time
from pathlib import Path
import shutil
import subprocess
import argparse
import logging
import signal
from typing import List, Optional
from datetime import datetime, timedelta
# Import local modules here.
from pygrabber.grabber import Grabber


__package__ = "pygrabber"
__author__ = "Meir Michanie"
__email__ = "meirm@riunx.com"
__version__ = "0.1.0"

__all__ = [
    # List exported symbols here.
]



class GrabMaster:
    def __init__(self):
        pass