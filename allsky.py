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

"""This modules performs the all sky measures and save them in different 
formats.
"""

import logging
import time
from config import *

# Azimuths and vertical values.
AZIMUTH_VALUES = [ 0, 20, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 ]
VERTICAL_VALUES = [ 20, 40, 60, 80 ]

DELAY_BETWEEN_REPEATED_MEASURES = 0.5

class AllSkyException(Exception):
    
    def __init__(self, msg):
        self._msg = msg
        
    def __str(self):
        return self._msg
            
class AllSkyMeasures(object):
    """This class stores a set of measures for all the sky and save them to
    a file with different formats.
    
    """
    
    def __init__(self, dim1, dim2):
        
        self._dim1 = dim1
        self._dim2 = dim2
        self._matrix = [[0 for x in range(dim2)] for x in range(dim1)] 
        self._zenith = None
                     
    def set(self, dim1, dim2, val):
        
        if dim1 >= 0 and dim1 < self._dim1 and \
            dim2 >= 0 and dim2 < self._dim2:
            self._matrix[dim1][dim2] = val
        else:
            raise AllSkyException("set: Invalid coordinates: %d %d" % 
                                  (dim1, dim2))
        
    def get(self, dim1, dim2):
        
        Val = None
        
        if dim1 >= 0 and dim1 < self._dim1 and \
            dim2 >= 0 and dim2 < self._dim2:
            val = self._matrix[dim1][dim2]
        else:
            raise AllSkyException("get: Invalid coordinates: %d %d" % 
                                  (dim1, dim2))
        
        return val 
    
    @property
    def zenith(self):
        return self._zenith    
    
    @zenith.setter
    def zenith(self, zenith):
        self._zenith = zenith
        
def do_beep():
    print '\a'
        
def mean_measure(ser, sqm_config):
    """Perform several measures and returns the mean value.
    
    Args:
        ser: Serial object used to communicate with SQM.     
        sqm_config: Configuration parameters.
        
    Returns.
        The mean value of the measures taken as a string.
    """
    
    mean_value = None

    measures = []
    
    for i in range(int(sqm_config.repetitions)):
        measures.append(float(ser.get_sqm_measure()))
        
        # Delay between repeated measures
        time.sleep(DELAY_BETWEEN_REPEATED_MEASURES)
        
    logging.debug("Repeated measures taken: %s" % measures)
    
    return str(sum(measures) / float(len(measures)))
    
def all_sky_measures(ser, sqm_config):
    """Perform the all sky measures.
    
    Args:
        ser: Serial object used to communicate with SQM.     
        sqm_config: Configuration parameters.
        output_file: Object to write output messages.
    """
    
    logging.debug("Starting all sky measures.")
    
    external_loop_name = None
    internal_loop_name = None
    
    # Depending on the order set the appropriate list for external and internal 
    # loops. 
    if sqm_config.order_is_azimuth:
        external_loop_values = VERTICAL_VALUES
        internal_loop_values = AZIMUTH_VALUES
               
        external_loop_name = "Vertical"
        internal_loop_name = "Azimuth"        
         
        print "Order: Processing all the azimuths of each vertical value ", \
            "before passing to the next vertical value."
    else:
        external_loop_values = AZIMUTH_VALUES
        internal_loop_values = VERTICAL_VALUES
               
        external_loop_name = "Azimuth"
        internal_loop_name = "Vertical"  
                
        print "Order: Processing all the vertical value before passing ", \
            "next azimuths."
            
    all_sky_values = AllSkyMeasures(len(external_loop_values), 
                                    len(internal_loop_values))
    
    delay = int(sqm_config.delay)
    delay_between_azimuth_vertical = int(sqm_config.delay_bet_azi_ver)
        
    for i in range(len(external_loop_values)):
        for j in range(len(internal_loop_values)):
            
            do_beep() 
            
            for k in range(delay):
                print "Waiting %d seconds before next measure ..." % (delay - k)
            
                time.sleep(1)            
            
            do_beep()
            
            print "Measuring next value: %s %d %s %d" % \
                (external_loop_name, external_loop_values[i], 
                 internal_loop_name, internal_loop_values[j])    
                
            measure = mean_measure(ser, sqm_config)
            
            all_sky_values.set(i, j, measure)
            
            logging.info("Measure: %s %d %s %d is %s" % \
                         (external_loop_name, external_loop_values[i], 
                          internal_loop_name, internal_loop_values[j],
                          measure))
            
        for k in range(delay_between_azimuth_vertical):
            print "Waiting %d seconds to change between azimuth and vertical." % \
                (delay_between_azimuth_vertical - k)
            
            time.sleep(1)
            
    print "Next value: zenith."
    
    measure = ser.get_sqm_measure()
    
    all_sky_values.zenith = measure
    
    logging.info("Measure: zenith is %s" % measure)