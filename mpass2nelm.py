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

"""A simple script to convert measures in MPASS unit to NELM values."""

import sys
import csv
from math import pow, log

def read_file(file_name):
    """Read the input file in CSV format.
    
    Args:
        file_name: Name of the file to read.
        
    Returns:
        A list with the rows read.
        
    """
    
    print "Reading from to file: %s" % file_name
    
    rows = []
    
    try:
        with open(file_name, "rb") as fr:
            
            reader = csv.reader(fr, delimiter=',', quotechar='"')        
            
            for row in reader:   
                 
                rows.append(row)
                
    except csv.Error as e:
        print "Error reading data from CSV file: '%s'" % file_name 
                
    except IOError as ioe:
        print "Error reading CSV file: '%s'" % file_name       
    
    return rows

def convert_values(data):
    """Convert the values of the data received. All the float values received
    are processed as MPASS values and converted to NELM ones using the
    calculation described in:
    http://www.unihedron.com/projects/darksky/NELM2BCalc.html 
    
    Args:
        data: data with the values to convert.
        
    Returns:
        The data with its float values converted.
        
    """
    
    print data
    
    converted_data = []
    
    for row in data:
        new_row = []
        for item in row:
            
            try:
                mpass = float(item)
                
                nelm = 7.93 - 5 * log(pow(10, 4.316 - (mpass / 5.0)) + 1, 10)
                
                new_row.append(nelm)
                
                print "Converted %.10g to %.10g" % (mpass, nelm)   
                         
            except ValueError as ve:
                # If the conversion to float is not successful the data is not
                # converted and is stored as is.
                print "Ignoring for conversion: %s" % item
                new_row.append(item)
            
        converted_data.append(new_row)    
    
    return converted_data

def write_file(file_name, rows):
    """Write the rows received to the output file in CSV format.
    
    Args:
        file_name: Name of the file to read.
        rows: List of rows to write to the file.
        
    """
    
    print "Saving to file: %s" % file_name
    
    try:                
        with open(file_name, 'w') as fw:
            
            writer = csv.writer(fw, delimiter='\t')
    
            for r in rows:
            
                writer.writerow(r)   
                
    except csv.Error as e:
        print "Error writing data in CSV file: '%s'" % file_name                
                
    except IOError as ioe:
        print "Error writing CSV file: '%s'" % file_name      

def main(argv):
    """Main function.
    
    Read the input file, convert the values and write then to the output file.
    """
    
    # The names of the files should be received as program arguments. 
    input_file_name = argv[1]
    output_file_name = argv[2]
    
    rows = read_file(input_file_name)
    
    # Check if at least one row has been read.
    if len(rows) > 0:
        rows_converted = convert_values(rows)
        
        write_file(output_file_name, rows_converted)

if __name__ == "__main__":
    
    if len(sys.argv) == 3:    
        main(sys.argv)
    else:
        print "Usage: %s input_file_name output_file_name" % sys.argv[0]