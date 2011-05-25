#! /usr/bin/env python

import subprocess
import sys

subprocess.call( ["haddCrab.py", "132440-148783_StreamExpress.txt"] )
subprocess.call( ["haddCrab.py", "132440_147146_StreamExpress.txt"] )
subprocess.call( ["haddCrab.py", "data3.txt"] )
subprocess.call( ["hadd -f allJet_data.root Jet*.root"], shell=True )
