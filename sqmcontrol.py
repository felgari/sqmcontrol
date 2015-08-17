#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Felipe Gallego. All rights reserved.
#
# This file is part of sqmcontrol: https://github.com/felgari/sqmcontrol
#
# This is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Performs a sequence of measures sending commands to a SQM.

SQM stands for Sky Quality Meter. It is a device to measure the sky darkness.
It is manufactured by Unihedron and one of the versions has a USB port.
This version is controlled with this software to perform a given sequence of 
measures.
"""

import sys
import logging

from sqmcparser import *
from cfgfile import *
from logutil import init_log

def periodic_measures(sqm_config, output_file_name):
    """ Perform the periodic measures.
    
    Args:
        sqm_config: Configuration parameters.
        output_file_name: Name of the file for the results.
    """
    
    pass 

def all_sky_measures(sqm_config, output_file_name):
    """ Perform the all sky measures.
    
    Args:
        sqm_config: Configuration parameters.
        output_file_name: Name of the file for the results.
    """
    
    pass

def sqm_measures(progargs, sqm_config):
    """Call the methods to perform the measures required.
    
    Args:
        progargs: Program arguments.
        sqm_config: Configuration parameters.
    """
    
    if sqm_config.mode_periodic:
        periodic_measures(sqm_config, progargs.output_file_name)
    else:
        all_sky_measures(sqm_config, progargs.output_file_name)

def main(progargs):
    """Main function.
    
    Args:
        progargs: Program arguments.
        
    """
    
    try:
        # Process program arguments and check that programs arguments are used
        # coherently.
        progargs = ProgramArguments()        
        
        # Initializes logging.
        init_log(progargs)
        
        logging.debug("Reading configuration file.")
        
        # Read configuration file. 
        sqm_config = SQMControlCfg(progargs.config_file_name)
        
        # Perform the measures.
        sqm_measures(progargs, sqm_config)

    except SQMControlException as sce:
        print sce

    except Exception as e:
        # To catch any other Exception.
        print e.__doc__
        print e.message     

# Where all begins ...
if __name__ == "__main__":

    # Create object to process the program arguments.
    progargs = ProgramArguments() 
    
    # Check the number of arguments received.
    if len(sys.argv) <= ProgramArguments.MIN_NUM_ARGVS:
        
        # If no arguments are provided show help and exit.
        print "The number of program arguments are not enough."   
             
        progargs.print_help()
        
        sys.exit(1)
        
    else: 
        # Number of arguments is right, execute main function.
        sys.exit(main(progargs)) 
    