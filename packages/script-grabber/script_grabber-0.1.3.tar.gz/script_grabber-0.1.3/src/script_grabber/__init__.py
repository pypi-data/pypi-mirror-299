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

# Import standard library modules here.

# Import third-party modules here.

# Import local modules here.
__package__ = "pygrabber"

__author__ = "Meir Michanie"
__email__ = "meirm@riunx.com"
__version__ = "0.1.0"


from . import grabber
from . import grabmaster
from . import grabexceptions

__all__ = [
    grabber,
    grabmaster,
    grabexceptions,
]
