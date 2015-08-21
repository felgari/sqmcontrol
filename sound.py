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

"""Reproduces sounds to indicate the start and end of operations."""

def start_sound(sqm_config):
    """Reproduces a start sound if specified in configuration.
    
    Args:   
        sqm_config: Configuration parameters.     
    """
    
    if sqm_config.beep:
        print '\a'

def end_sound(sqm_config):
    """Reproduces an end sound if specified in configuration.
    
    Args:   
        sqm_config: Configuration parameters.     
    """
    
    if sqm_config.beep:
        print '\a'