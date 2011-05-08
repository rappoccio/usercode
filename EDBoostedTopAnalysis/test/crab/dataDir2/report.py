#! /usr/bin/env python

import subprocess
import sys

subprocess.call( ["multiCrabReport.py", "132440-148783_StreamExpress.txt"] )
subprocess.call( ["multiCrabReport.py", "132440_147146_StreamExpress.txt"] )
subprocess.call( ["multiCrabReport.py", "data3.txt"] )
