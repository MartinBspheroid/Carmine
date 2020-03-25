# Embedded file name: C:\ProgramData\Ableton\Live 9.7 Suite\Resources\MIDI Remote Scripts\ClyphX_Pro\clyphx_pro\OSProxy.py
""" This module redirects calls to os and open methods and is replaceable in testing. """
import os
import PathProxy as path
listdir = os.listdir
makedirs = os.makedirs
open_file = open