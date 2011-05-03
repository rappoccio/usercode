#! /usr/bin/env python

import subprocess
import sys

subprocess.call( ["removeCrab.py", "132440-148783_StreamExpress.txt"] )
subprocess.call( ["removeCrab.py", "132440_147146_StreamExpress.txt"] )
subprocess.call( ["removeCrab.py", "data3.txt"] )
