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
from outfile import *

# Azimuths and vertical values.
AZIMUTH_VALUES = [ 0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 ]
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
    
    _VALUES_SEP = ","
    
    def __init__(self, az_dim, vert_dim):
        
        self._az_dim = az_dim
        self._vert_dim = vert_dim
        self._matrix = [[0 for x in range(vert_dim)] for x in range(az_dim)] 
        self._zenith = None
                     
    def set(self, az_index, vert_index, val):
        """Set the values for the coordinates received.
        
        Args:
            az_index: Azimuth coordinate.
            vert_index: Vertical coordinate.
            val: Value to set.
            
        """
        
        if az_index >= 0 and az_index < self._az_dim and \
            vert_index >= 0 and vert_index < self._vert_dim:
            self._matrix[az_index][vert_index] = val
        else:
            raise AllSkyException("set: Invalid coordinates: %d %d" % 
                                  (az_index, vert_index))
        
    def get(self, az_index, vert_dim):
        """Returns the values for the coordinates received.
        
        Args:
            az_index: Azimuth coordinate.
            vert_index: Vertical coordinate.
            
        Returns:
            The value.
            
        """
                
        Val = None
        
        if az_index >= 0 and az_index < self._az_dim and \
            vert_dim >= 0 and vert_dim < self._vert_dim:
            val = self._matrix[az_index][vert_dim]
        else:
            raise AllSkyException("get: Invalid coordinates: %d %d" % 
                                  (az_index, vert_dim))
        
        return val
    
    def save_as_list(self, output_filename, info):
        """Save the values in a list by sorted first by azimuth.
        
        Args:
            info: Information to add to the file.
        """
        
        try:
            output_file = OutputFile(output_filename)  
            
            output_file.write_com(info)       
            
            for i in range(self._az_dim):
                for j in range(self._vert_dim):
                    output_file.write("%s%s" %
                                      (self._matrix[j][i],
                                       AllSkyMeasures._VALUES_SEP))
                        
                # Writes the separator if it is not the last value.
                if i < self._az_dim - 1:
                    output_file.write("%s%s" % (self._zenith, 
                                                AllSkyMeasures._VALUES_SEP))
                else:
                    output_file.write("%s" % self._zenith)
            
        except OutputFileException as ofe:
            logging.error(ofe)
    
    @property
    def zenith(self):
        return self._zenith    
    
    @zenith.setter
    def zenith(self, zenith):
        self._zenith = zenith
        
def do_beep(sqm_config):
    """Reproduces a beep if specified in configuration.
    
    Args:   
        sqm_config: Configuration parameters.     
    """
    
    if sqm_config.beep:
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
    
def all_sky_measures(ser, sqm_config, output_filename):
    """Perform the all sky measures.
    
    Args:
        ser: Serial object used to communicate with SQM.     
        sqm_config: Configuration parameters.
        output_filename: Object to write output messages.
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
            
    all_sky_values = AllSkyMeasures(len(AZIMUTH_VALUES), 
                                    len(VERTICAL_VALUES))
    
    delay = int(sqm_config.delay)
    delay_between_azimuth_vertical = int(sqm_config.delay_bet_azi_ver)
        
    for i in range(len(external_loop_values)):
        for j in range(len(internal_loop_values)):
            
            do_beep(sqm_config) 
            
            for k in range(delay):
                print "Waiting %d seconds before next measure ..." % (delay - k)
            
                time.sleep(1)            
            
            do_beep(sqm_config)
            
            print "Measuring next value: %s %d %s %d" % \
                (external_loop_name, external_loop_values[i], 
                 internal_loop_name, internal_loop_values[j])    
                
            measure = mean_measure(ser, sqm_config)
            
            if sqm_config.order_is_azimuth:            
                all_sky_values.set(j, i, measure)
            else:
                all_sky_values.set(i, j, measure)
            
            logging.info("Measure: %s %d %s %d is %s" % \
                         (external_loop_name, external_loop_values[i], 
                          internal_loop_name, internal_loop_values[j],
                          measure))
            
        for k in range(delay_between_azimuth_vertical):
            print "Waiting %d seconds to change between azimuth and vertical." % \
                (delay_between_azimuth_vertical - k)
            
            time.sleep(1)
            
    print "Measuring next value: zenith."
    
    measure = ser.get_sqm_measure()
    
    all_sky_values.zenith = measure
    
    logging.info("Measure: zenith is %s" % measure)
    
    all_sky_values.save_as_list(output_filename, sqm_config.info)