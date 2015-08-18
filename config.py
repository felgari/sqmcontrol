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

"""This module provides some functions on text files. """

import os
import logging
import csv

class SQMControlException(Exception):
    
    def __init__(self, msg):
        
        self._msg = msg
        
    def __str__(self):
        return self._msg

class SQMControlCfg(object):
    
    # Character to separate parameter name from its value in the configuration
    # file.
    _CFG_FILE_SEP_CHAR = "="
    _COMMENT_CHARACTER = "#"    
    
    # Names of the configuration parameters.
    _MODE_PAR_NAME = "MODE"
    _PERIODICITY_PAR_NAME = "PERIODICITY"
    _DURATION_PAR_NAME = "DURATION"    
    _REPETITIONS_PAR_NAME = "REPETITIONS"
    _DELAY_PAR_NAME = "DELAY"    
    _DELAY_BET_AZI_VER_PAR_NAME = "DELAY_BET_AZI_VER"
    _ORDER_PAR_NAME = "ORDER"
    _PLOT_COLORS_PAR_NAME = "PLOT_COLORS"
    _INFO_PAR_NAME = "INFO"
    _BEEP_PAR_NAME = "BEEP"
    
    # Valid values for each parameter.
    _MODE_CONTINUOUS_NAME = "CONTINUOUS"
    _MODE_SKY_NAME = "SKY"
    _MODE_VALUES = [ _MODE_CONTINUOUS_NAME, _MODE_SKY_NAME ]
    _PERIODICITY_MAX_VALUE = 45000
    _DURATION_MAX_VALUE = 450000    
    _REPETITIONS_MAX_VALUE = 1000
    _DELAY_MAX_VALUE = 60
    _DELAY_BET_AZI_VER_MAX_VALUE = 60
    _ORDER_VALUES = [ "AZIMUTH", "ZENITH" ]
    _PLOT_COLORS_VALUES = [ "FIXED", "EXTEND" ]       
    _BEEP_VALUES = [ "YES", "NO" ] 
    
    def __init__(self, file_name):

        self._cfg_params = {}
        
        self._error_params = 0
        
        if os.path.exists(file_name):
        
            self._read_cfg_file(file_name)
            
            self._check_cfg_values()
            
        else:
            raise SQMControlException("Configuration file '%s' doesn't exist."
                                      % file_name)
            
    def __str__(self):        
        return str(self._cfg_params)
        
    @property
    def mode(self):
        return self._cfg_params[SQMControlCfg._MODE_PAR_NAME]
    
    @property
    def mode_continuous(self):
        return self.mode == SQMControlCfg._MODE_CONTINUOUS_NAME
    
    @property
    def mode_all_sky(self):
        return self.mode == SQMControlCfg._MODE_SKY_NAME    

    @property
    def periodicity(self):
        return self._cfg_params[SQMControlCfg._PERIODICITY_PAR_NAME]
    
    @property
    def duration(self):
        return self._cfg_params[SQMControlCfg._DURATION_PAR_NAME]    
    
    @property
    def repetitions(self):
        return self._cfg_params[SQMControlCfg._REPETITIONS_PAR_NAME]
    
    @property
    def delay(self):
        return self._cfg_params[SQMControlCfg._DELAY_PAR_NAME]
    
    @property
    def delay_bet_azi_ver(self):
        return self._cfg_params[SQMControlCfg._DELAY_BET_AZI_VER_PAR_NAME]
    
    @property
    def order(self):
        return self._cfg_params[SQMControlCfg._ORDER_PAR_NAME]
    
    @property
    def order_is_azimuth(self):
        return self.order == SQMControlCfg._ORDER_VALUES[0]
    
    @property
    def order_is_zenith(self):
        return self.order == SQMControlCfg._ORDER_VALUES[1]    
    
    @property
    def plot_colors(self):
        return self._cfg_params[SQMControlCfg._PLOT_COLORS_PAR_NAME]   
    
    @property
    def plot_color_fixed(self):
        return self.plot_colors == SQMControlCfg._PLOT_COLORS_VALUES[0]
    
    @property
    def plot_color_extended(self):
        return self.plot_colors == SQMControlCfg._PLOT_COLORS_VALUES[1]      
    
    @property
    def info(self):
        return self._cfg_params[SQMControlCfg._INFO_PAR_NAME]  
    
    @property
    def beep(self):
        return self._cfg_params[SQMControlCfg._BEEP_PAR_NAME] == \
            SQMControlCfg._BEEP_VALUES[0]
        
    def _read_cfg_file(self, file_name):
        """Read parameters from a text file containing a pair parameter/value
        in each line separated by an equal character.
        
        Args:
            file_name: Name of the configuration file to read.
        
        """
                
        logging.debug("Reading configuration from file: %s" % (file_name))
        
        try:
        
            # Read the file that contains the self._cfg_params of interest.
            with open(file_name, 'rb') as fr:
                reader = csv.reader(fr, 
                                    delimiter=SQMControlCfg._CFG_FILE_SEP_CHAR)        
                
                for row in reader:    
                    # Discard if it is a comment line.
                    if len(row) > 0 and \
                        row[0].strip()[0] <> SQMControlCfg._COMMENT_CHARACTER:
                         
                        # Just two elements, the parameter name and value.
                        if len(row) == 2:             
                            try:
                                # Remove spaces before using the values.                
                                param_name = row[0].strip()
                                param_value = row[1].strip()
                                
                                self._cfg_params[param_name] = param_value
                                
                            except TypeError as te:
                                logging.error(te)
                        else:
                            # the line has not a valid number of elements.
                            logging.warning("Format invalid in '%s' of file %s, line ignored." %
                                            (row, file_name))  
                    
            logging.debug("Read these configurations parameters: %s from %s" % 
                          (self._cfg_params, file_name))
                   
        except IOError as ioe:
            err_msg = "Reading configuration file: %s" % (file_name)
            logging.error(err_msg)
            
            SQMControlException(err_msg)
            
            # Assign an empty set.
            self._cfg_params = set()   

    def _check_cfg_values(self):
        """Check that all the parameters needed have been supplied and have
        valid values.
        
        """

        self._check_mode()
        
        self._check_periodicity()             
        
        self._check_duration()               
        
        self._check_repetitions()       
        
        self._check_delay()          
        
        self._check_delay_between_azimuth_and_vertical() 
        
        self._check_order()        
        
        self._check_plot_colors()      
        
        self._check_beep()  
        
        if self._error_params > 0:            
            raise SQMControlException("There is one or more errors with ",
                                      "configuration parameters, see log.")
        
    def _check_mode(self):
        """Check this parameter has been provided and with a valid value.

        """
        
        try:
            m = self.mode
            
            if not m in SQMControlCfg._MODE_VALUES:
                logging.error(
                    "Value '%s' not valid for '%s'. Valid values are: %s" %
                    (m, SQMControlCfg._MODE_PAR_NAME, 
                     SQMControlCfg._MODE_VALUES))
                
        except KeyError as ke:
            logging.error("%s parameter is required." % 
                          SQMControlCfg._MODE_PAR_NAME)
       
    def _check_periodicity(self):
        """Check this parameter has been provided and with a valid value.
                    
        """     
                
        try:          
            self._check_numeric_value(self.periodicity,
                                      SQMControlCfg._PERIODICITY_PAR_NAME,
                                      SQMControlCfg._PERIODICITY_MAX_VALUE)
            
        except KeyError as ke:            
            logging.error("%s parameter is required." %
                SQMControlCfg._PERIODICITY_PAR_NAME)
    
    def _check_duration(self):
        """Check this parameter has been provided and with a valid value.
             
        """     
                
        try:          
            self._check_numeric_value(self.duration, 
                                      SQMControlCfg._DURATION_PAR_NAME,
                                      SQMControlCfg._DURATION_MAX_VALUE)
            
        except KeyError as ke:
            logging.error("%s parameter is required." %
                SQMControlCfg._DURATION_PAR_NAME)  
    
    def _check_repetitions(self):
        """Check this parameter has been provided and with a valid value.
                    
        """      
                
        try:          
            self._check_numeric_value(self.repetitions, 
                                      SQMControlCfg._REPETITIONS_PAR_NAME,
                                      SQMControlCfg._REPETITIONS_MAX_VALUE)
            
        except KeyError as ke:
            logging.error("%s parameter is required." %
                SQMControlCfg._REPETITIONS_PAR_NAME)   
        
    def _check_numeric_value(self, par_value, par_name, max_value):
        """Check this parameter has been provided and with a valid value.
                    
        """
        
        # Check it is a number.
        if par_value.isdigit():
            
            # Check it has a valid value.
            num_val = int(par_value)
            
            if num_val <= 0 or num_val > max_value:
                logging.error("'%s' parameter value %d is invalid [1-%d]." %
                              (par_name, num_val, max_value))
        else:
            logging.error("%s parameter must be numeric." % par_name)
            
    def _check_delay(self):
        """Check this parameter has been provided and with a valid value.
             
        """
        
        try:          
            self._check_numeric_value(self.delay, 
                                      SQMControlCfg._DELAY_PAR_NAME,
                                      SQMControlCfg._DELAY_MAX_VALUE)
            
        except KeyError as ke:
            logging.error("%s parameter is required." %
                SQMControlCfg._DELAY_PAR_NAME)   
            
    def _check_delay_between_azimuth_and_vertical(self):      
        """Check this parameter has been provided and with a valid value.
             
        """
        
        try:          
            self._check_numeric_value(self.delay_bet_azi_ver, 
                                      SQMControlCfg._DELAY_BET_AZI_VER_PAR_NAME,
                                      SQMControlCfg._DELAY_BET_AZI_VER_MAX_VALUE)
            
        except KeyError as ke:
            logging.error("%s parameter is required." %
                SQMControlCfg._DELAY_BET_AZI_VER_PAR_NAME)           
    
    def _check_order(self):
        """Check this parameter has been provided and with a valid value.
             
        """
        
        try:
            m = self.order
            
            if not m in SQMControlCfg._ORDER_VALUES:
                logging.error("Value '%s' not valid for '%s'. Valid values are: %s" %
                    (m, SQMControlCfg._ORDER_PAR_NAME, 
                     SQMControlCfg._ORDER_VALUES))
                
        except KeyError as ke:
            logging.error("%s parameter is required." %
                SQMControlCfg._ORDER_PAR_NAME)
         
    def _check_plot_colors(self):
        """Check this parameter has been provided and with a valid value."""
        
        try:
            m = self.plot_colors
            
            if not m in SQMControlCfg._PLOT_COLORS_VALUES:
                logging.error("Value '%s' not valid for '%s'. Valid values are: %s" %
                    (m, SQMControlCfg._PLOT_COLORS_PAR_NAME, 
                     SQMControlCfg._PLOT_COLORS_VALUES))
                
        except KeyError as ke:
           logging.error("%s parameter is required." %
                SQMControlCfg._PLOT_COLORS_PAR_NAME) 
           
    def _check_beep(self):
        try:
            m = self.plot_colors
            
            if not m in SQMControlCfg._BEEP_VALUES:
                logging.error("Value '%s' not valid for '%s'. Valid values are: %s" %
                    (m, SQMControlCfg._BEEP_PAR_NAME, 
                     SQMControlCfg._BEEP_VALUES))
                
        except KeyError as ke:
           logging.error("%s parameter is required." %
                SQMControlCfg._BEEP_PAR_NAME)         
           
    def str_continuous_par(self):
        """Returns a string with the values of the continuous mode."""
        
        return "Mode %s - Periodicity: %s - Duration: %s" % \
            (SQMControlCfg._MODE_CONTINUOUS_NAME, self.periodicity, 
             self.duration)
        
    def str_all_sky_par(self):
        """Returns a string with the values of the all sky mode."""
        
        return "Mode %s - Repetitions: %s - Order: %s" % \
            (SQMControlCfg._MODE_SKY_NAME, self.repetitions, self.order)       