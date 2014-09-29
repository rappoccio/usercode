#! /usr/bin/env python

import subprocess
import sys

subprocess.call( ["multiCrab.py", "132440-148783_StreamExpress.txt", "crab_148783.cfg"] )
subprocess.call( ["multiCrab.py", "132440_147146_StreamExpress.txt", "crab_147146.cfg"] )
subprocess.call( ["multiCrab.py", "data3.txt", "crab_Nov5.cfg"] )
