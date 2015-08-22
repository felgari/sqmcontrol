sqmcontrol
==========

Python program to control a [SQM-LU](http://www.unihedron.com/projects/darksky/) and perform different types of measure with it.

Functionality
-------------
This software performs the following tasks:
* Continuos measures with a SQM indicating the periodicity and total duration of the measures.
* Set of measures related to different positions in the sky to obtain a map of darkness of the whole sky. These measures are composed in a structure that corresponds to their positions in the sky. These measures could be plotted using [darkskyplot](https://github.com/felgari/darkskyplot)

Requirements
------------
This software has been developed with python 2.7 and should work properly with newer versions of python and the modules listed below.

Also the following python modules are needed:
* argparse 1.1
* logging 0.5.1.2
* pyserial