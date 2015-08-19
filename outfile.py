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

"""This modules writes the results of the measures to a file."""

import logging
import time

class OutputFileException(Exception):
    
    def __init__(self, msg):
        
        self._msg = msg
        
    def __str__(self):
        
        return self._msg

class OutputFile(object):
    """This class manages the output file."""
    
    _COMMENT_CHAR = "#"
    _FILE_EXT = "out"
    
    def __init__(self, original_filename):
        
        self._file = None
        
        filename = self._get_output_filename(original_filename)
        
        try:
            self._file = open(filename, "w")
            
        except (OSError, IOError) as ioe:
            
            msg = "Opening output file %s" % filename
            
            logging.error(msg)
            
            raise OutputFileException(msg)
        
    def __del__(self):
        
        if self._file is not None:
            self._file.close()

    def _get_output_filename(self, original_filename):
        """Generate the output file name from the name given as parameter and 
        the current data and time.
        
        Args:
            original_filename: Original name for the file.
        
        Returns:
           The name of the output file name. 
        
        """
        
        return "%s_%s.%s" % (time.strftime("%Y%m%d%H%M%S", time.localtime()),
                             original_filename, OutputFile._FILE_EXT)
            
    def write(self, msg):
        """Write the message received to the output file.
        
        Args:
            msg: String to write.
            
        """
        
        if self._file is not None:
            self._file.write(msg)
            self._file.flush()
            
    def write_com(self, msg):
        """Write the message received to the output file as a comment.
        
        Args:
            msg: String to write.
            
        """   
        
        if self._file is not None:
            self._file.write("%s %s\n" % (OutputFile._COMMENT_CHAR, msg))
            self._file.flush()             