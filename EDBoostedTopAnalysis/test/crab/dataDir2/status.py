#! /usr/bin/env python

import subprocess
import sys

subprocess.call( ["multiCrabStatus.py", "132440-148783_StreamExpress.txt"] )
subprocess.call( ["multiCrabStatus.py", "132440_147146_StreamExpress.txt"] )
subprocess.call( ["multiCrabStatus.py", "data3.txt"] )
