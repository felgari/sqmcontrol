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
import time
from astropy.time import Time

from logutil import init_log
from sprogargs import *
from config import *
from sqmserial import *
from allsky import *
from outfile import *
from sound import *

# Default names for output files.
DEFAULT_SKY_OUT_FILE_NAME = "all_sky"
DEFAULT_CONT_OUT_FILE_NAME = "continuous"      

# To separate time from measure in output messages.
SEP_STR = "->"       
    
def process_continuous_measure(measure, output_file):
    """Process the continuous measure received, saving it.
    
    Args:
        measure: The value of the measure.
        output_file: Object to write output messages.      
    """
    
    msg ="%s %s %s\n" % (time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()),
                         SEP_STR, measure)
    
    # Avoid the final new line character.
    print msg[:-1]
    
    output_file.write(msg)

def continuous_measures(ser, sqm_config, output_filename):
    """ Perform the continuous measures.
    
    Args:
        ser: Serial object used to communicate with SQM. 
        sqm_config: Configuration parameters.
        output_filename: Object to write output messages.
    """
    
    logging.debug("Starting continuous measures.")
    
    output_file = OutputFile(output_filename)     
    
    output_file.write_com(sqm_config.str_continuous_par())
    
    running_time = 0
    
    periodicity = int(sqm_config.periodicity)
    
    duration = int(sqm_config.duration)
    
    # Check if a key has been pressed to exit.
    try:
        while running_time < duration:
            
            # Get a measure from SQM.
            measure = ser.get_sqm_measure()
                        
            # Process measure.
            process_continuous_measure(measure, output_file)
                    
            # Wait the time indicated between measures.
            for i in range(periodicity):                                    
                time.sleep(1)
                
                running_time += 1                    
                    
    # To catch a Ctrl-C.
    except KeyboardInterrupt:
        logging.debug("Exiting from continuous measures loop by Ctrl-C.")   
        
def one_measures(ser, sqm_config):
    """ Perform the continuous measures.
    
    Args:
        ser: Serial object used to communicate with SQM. 
        sqm_config: Configuration parameters.
    """
    
    exit = False
    
    logging.debug("Starting independent measures.")   
    
    # Use the periodicity parameter to wait bwtween measures.
    periodicity = int(sqm_config.periodicity) 
    
    while not exit:
    
        # Check if a key has been pressed to exit.
        try:       
            
            # Wait the time indicated between measures.
            for i in range(periodicity):
                print "Waiting %d seconds before measuring ..." % \
                    (periodicity - i)
                    
                if i == periodicity - 1:
                    start_sound(sqm_config)
                                                    
                time.sleep(1)
            
            measure = ser.get_sqm_measure()
            
            end_sound(sqm_config)
            
            print "Value measured: %s" % measure
                             
        # To catch a Ctrl-C.
        except KeyboardInterrupt:
            exit = True
            msg = "Exiting from independent measures by Ctrl-C."
            print msg
            logging.debug(msg)   
        
def sqm_measures(progargs, sqm_config):
    """Call the methods to perform the measures required.
    
    Args:
        progargs: Program arguments.
        sqm_config: Configuration parameters.
    """
    
    try:
        ser = SerialPort()
        
        ser.init_port()
        
        if sqm_config.mode_continuous:
            continuous_measures(ser, sqm_config, DEFAULT_CONT_OUT_FILE_NAME)
        elif sqm_config.mode_all_sky:
            all_sky_measures(ser, sqm_config, DEFAULT_SKY_OUT_FILE_NAME)
        elif sqm_config.mode_one:
            one_measures(ser, sqm_config)
            
    except SerialPortException as spe:
         logging.error(spe) 
         print spe
    except OutputFileException as ofe:
        logging.error(ofe)        

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
        
        logging.debug("Program finished.")

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
    