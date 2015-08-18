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

"""This module performs the communication with SQL using a serial USB. """

import logging
import serial

class SerialPortException(Exception):
    
    def __init__(self, msg):
        
        self._msg = msg
        
    def __str__(self):
        
        return self._msg

class SerialPort(object):
    
    SERIAL_DEVICES_UNIX = ["/dev/ttyUSB0", "/dev/ttyUSB1", \
                           "/dev/ttyUSB2", "/dev/ttyUSB3"]
    
    SERIAL_DEVICES_WIN = ["COM1", "COM2", "COM3", "COM4"]   
    
    SERIAL_DEVICES = [ 0, 1, 2, 3 ]
    
    BAUD_RATE = 115200
    
    DATA_BITS = serial.EIGHTBITS  
    
    STOP_BITS = serial.STOPBITS_ONE
    
    PARITY = serial.PARITY_NONE
    
    READ_TIMEOUT = 1
    
    MAX_BYTES_TO_READ = 255 
    
    SQM_DATA_SEP = ","
    
    MEASURE_POS = 1
    
    def __init__(self):
        
        self._ser = serial.Serial()
        self._device = None
        
    def __del__(self):
        
        if self._ser.isOpen():
            self._ser.close()
        
    def _setup_port(self, port):
        
        success = False
        
        self._ser.port = SerialPort.SERIAL_DEVICES_UNIX[port]
        self._ser.baudrate = SerialPort.BAUD_RATE
        self._ser.bytesize = SerialPort.DATA_BITS
        self._ser.stopbits = SerialPort.STOP_BITS
        self._ser.parity = SerialPort.PARITY 
        self._ser.timeout = SerialPort.READ_TIMEOUT 
        
        self._ser.open()
        
        if self._ser.isOpen():
            success = True
            
        self._ser.close()
            
        return success        
        
    def _detect_port(self):
        
        found = False
        
        # Try all the devices available in order.
        for sd in SerialPort.SERIAL_DEVICES:
            
            logging.debug("Trying device %d ..." % sd)
            try:
            
                if self._setup_port(sd):
                    
                    self._ser.open()
                
                    br = self._get_measure()
                    
                    self._ser.close()
                    
                    # Check if there was a successful reading of data.
                    if len(br) > 0:
                        self._device = sd
                        found = True
                        break
                    
            except serial.SerialException as se:
                print se
            except serial.SerialTimeoutException as ste:
                print ste
            
        return found
        
    def _get_measure(self):
        """Get a measure from SQM."""
        
        bytes_read = None
        
        if self._ser.isOpen():
            
            # Send request to SQM.
            self._ser.write("rx\r")
            
            # Read from SQM.
            bytes_read = self._ser.readline(SerialPort.MAX_BYTES_TO_READ)
            
            logging.debug("SQM Read: %s" % bytes_read.strip())
        else:
            raise SerialPortException("Serial port not open to get a measure.")
        
        return bytes_read
    
    def _parse_sqm_data(self, sqm_data):
        """Parse the data read from SQM.
        
        Args:
            sqm_data: Data read from SQM.
            
        """
        
        splitted_data = sqm_data.split(SerialPort.SQM_DATA_SEP)
        
        stripped_data = [ sd.strip() for sd in splitted_data]
        
        logging.debug("Stripped data from SQM: %s" % stripped_data)
        
        return stripped_data
        
    def init_port(self):
        
        if self._detect_port():
            logging.debug("Device found at %s" % self._device)
        else:
            raise SerialPortException("Device not found")        
        
    def get_sqm_measure(self):
        """Returns a measure taken by the SQM."""
        
        measure = None
        
        self._ser.open()
                
        sqm_measure = self._get_measure()
        
        self._ser.close()        
        
        parsed_data = self._parse_sqm_data(sqm_measure)
        
        if len(parsed_data) > SerialPort.MEASURE_POS:
            measure_value = parsed_data[SerialPort.MEASURE_POS] 
        
        # Remove the final character used for the unit.
        only_num_value = measure_value[:-1]
            
        logging.debug("Value read: %s, unit removed: %s" % 
                      (measure_value, only_num_value))
        
        return only_num_value
        