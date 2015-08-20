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

"""Process the program arguments received by main function."""

import argparse

class ProgramArguments(object):
    """Encapsulates the definition and processing of program arguments."""
    
    # At least the configuration file.
    MIN_NUM_ARGVS = 0   
    DEFAULT_LOG_LEVEL = "DEBUG"
    DEFAULT_LOG_FILE_NAME = "sqmcontrol.log"
    DEFAULT_CFG_FILE_NAME = "sqm.cfg"       
    
    def __init__(self):
        """Initializes parser. 
        
        Initialization of the parse and parsing of the program arguments.

        """                              
            
        # Creates the object that parses the program arguments.
        self.__parser = argparse.ArgumentParser()        
        
        # Initiate arguments of the parser.
        self.__parser.add_argument("-c", dest="c", metavar="cfg",
                                   help="Name of the configuration file.")                             
        
        self.__parser.add_argument("-l", metavar="log file name", dest="l", 
                                   help="File to save the log messages") 
        
        self.__parser.add_argument("-v", metavar="log level", dest="v", 
                                   help="Level of the log messages to generate")               
        
        self.__parser.add_argument("-p", dest="p", action="store_true", 
                                   help="Save plots to files.")           
        
        # Parse program arguments.
        self.__args = self.__parser.parse_args()  
        
        # Set default values if not supplied as program arguments.
        if self.__args.c is None:
            self.__args.c = ProgramArguments.DEFAULT_CFG_FILE_NAME
            
        if self.__args.l is None:
            self.__args.l = ProgramArguments.DEFAULT_LOG_FILE_NAME
            
        if self.__args.v is None:
            self.__args.v = ProgramArguments.DEFAULT_LOG_LEVEL                                  
        
    @property    
    def config_file_name(self):        
        return self.__args.c        
        
    @property
    def store_plot(self):
        return self.__args.p
    
    @property
    def log_file_name(self):
        return self.__args.l       
    
    @property
    def log_level(self):
        return self.__args.v                        
            
    def print_usage(self):
        """Print arguments options."""
                
        self.__parser.print_usage()     
        
    def print_help(self):
        """Print help for arguments options."""
                
        self.__parser.print_help()   