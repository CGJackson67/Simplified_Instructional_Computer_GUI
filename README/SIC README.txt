This project (Simplified_Instructional_Computer_GUI) is a GUI implementation of SIC System Software
(Assembler, Loader, Simulator) as described in the textbook System Software by Leland L. Beck,
3rd Edition.  Only basic SIC functionality is provided.  Implementation of SIC/XE features was
not attempted. This project was developed in PyCharm 2023.3.3 (Community Edition) using Python 3.12.
It is meant to be run inside the Pycharm IDE and has not been tested elsewhere.  The GUI
implementation was based on an earlier commandline driven implementation which can be found in
the SIC_System_Software repository.  The runnable file for the GUI implementaion can be found here:
SIC_GUI > sic_gui_app.py.  This application contains both the SIC Assembler and the SIC Simulator.
Examples of SIC assembly programs are provided in the Assembly Code folder.
These program examples have been taken from the book, and some have been modified for testing
purposes.  Some of these assembly programs run to completion successfully, and others fail
deliberately.  The assembly program, ReadWrite.asm, exercises the simulated peripheral devices
(both input and output).  SIC_DEFAULT_WORKING_DIRECTORY must be configured properly before running
either the GUI application.  The configuration file is found here: SIC_GUI > sic_configuration.py.
Extensive development notes can be found in the README folder.


GUI RUNNABLE
============
SIC_GUI > sic_gui_app.py

GUI CONFIGURATION
SIC_GUI > sic_configuration.py