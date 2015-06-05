# -*- coding: utf-8 -*-
"""
Pneunets.py
Ryan Truby, Harvard Lewis Research Group
04/16/2015

Library of mecode functions for printing soft robot pneunet actuators.
"""

import numpy as np
import e3DMatrixPrinting
import e3DPGlobals

# Define the export file that will hold the generated G code
import os
cur_filepath = os.path.dirname(os.path.realpath(__file__))
splitted = cur_filepath.split('/')
n = len(splitted)
cur_dir = ''.join((dir+'/') for dir in splitted[:n-1])
exportFileDir = cur_dir + "soft_robotics_octobot/Pneunet.pgm"
print "Exporting to file " + str(exportFileDir)

e3DPGlobals.init_G(exportFileDir)

def print_void_layer(length, width):
        e3DMatrixPrinting.move_y(length/2.0)
        e3DMatrixPrinting.move_x(width)
        e3DMatrixPrinting.move_y(-1*length)
        e3DMatrixPrinting.move_x(-1*width)
        e3DMatrixPrinting.move_y(length/2.0)
        
def print_pneunet(num_bladders, num_layers, substrate_zero):
   
    # "80" = for printing at 80 psi with microgels and long blue tip
    # "85" = for printing at 85 psi with 27% F127 with lavendar tip                           
    # bladder spacer parameters
    spacer_print_speed = 4 # "80" 
    spacer_print_speed = 0.5 # "85"
    spacer_layers = int(num_layers)
    spacer_layer_increment = 0.82 # "80" 
    spacer_layer_increment = 0.8  # "85"
    spacer_spacing = 6
    spacer_length = 12
    spacer_width = 0.85 # "80" 
    spacer_with = 1 # "85"
    num_spacers = num_bladders - 1
    
    # bladder parameters
    bladder_print_speed = 3 # "80" 
    bladder_print_speed = 0.5 # "85"
    bladder_layers = int(num_layers)
    bladder_layer_increment = 0.9 # "80" 
    bladder_layer_increment = 0.8 # "85"
    bladder_spacing = spacer_spacing
    bladder_length = spacer_length-2
    bladder_width = 1
    
    
    # bus line parameters
    bus_line_print_speed = 1 # "80"
    bus_line_print_speed = 0.5 # "85"
    bus_line_length = num_spacers * spacer_spacing
    
    # sensor parameters
    sensor_print_speed = 5 # "80"
    sensor_print_speed = 2 # "85"
    
    spacer_print_height = substrate_zero + spacer_layer_increment
        
    def print_bladder_spacers():
        e3DMatrixPrinting.travel_mode()
        e3DPGlobals.g.write("\n; Print pneunet bladders.")
        for spacer in range(num_spacers):
            e3DMatrixPrinting.move_x(spacer_spacing)
            spacer_print_height = substrate_zero + spacer_layer_increment
            e3DMatrixPrinting.print_mode(print_height_abs = spacer_print_height, print_speed = 50)
            e3DPGlobals.g.feed(spacer_print_speed)
            for layer in range(spacer_layers):
                print_void_layer(length = spacer_length, width = spacer_width)
                e3DPGlobals.g.feed(10)
                e3DPGlobals.g.move(z = spacer_layer_increment)
                e3DPGlobals.g.feed(spacer_print_speed)
            e3DMatrixPrinting.travel_mode()
        
    bladder_print_height = (3 * spacer_layer_increment) + substrate_zero
        
    def print_bladders():
        e3DMatrixPrinting.move_x(-1*spacer_spacing*(num_spacers-1)-1*bladder_spacing/2.0)
        for bladder in range(num_bladders):    
            e3DMatrixPrinting.print_mode(print_height_abs = bladder_print_height, print_speed = 20)
            e3DPGlobals.g.feed(bladder_print_speed)
            for layer in range(bladder_layers):
                print_void_layer(length = bladder_length, width = bladder_width)
                e3DPGlobals.g.move(z = bladder_layer_increment)
            e3DMatrixPrinting.travel_mode()
            e3DMatrixPrinting.move_x(bladder_spacing)
    
    bus_line_print_height = bladder_print_height + ((bladder_layers+1) * bladder_layer_increment) # should this be bladder_layers+1?
    
    def print_bladder_bus_line():
        e3DMatrixPrinting.move_x(-1*bladder_spacing*(num_bladders))
        e3DMatrixPrinting.print_mode(print_height_abs = bus_line_print_height, print_speed = 20)
        e3DPGlobals.g.feed(bus_line_print_speed)
        e3DMatrixPrinting.move_x(bladder_spacing*(num_bladders-0.5))
        e3DMatrixPrinting.travel_mode()
    
    def print_sensor():
       sensor_width = 4
       sensor_height_offset = 0.5
       sensor_length_offset = 3
       e3DMatrixPrinting.move_y(sensor_width/2)
       e3DMatrixPrinting.print_mode(print_height_abs = bus_line_print_height+sensor_height_offset, print_speed = 20)
       e3DPGlobals.g.feed(sensor_print_speed)
       e3DMatrixPrinting.move_x(-1*bladder_spacing*(num_bladders-0.5)-sensor_length_offset)
       e3DMatrixPrinting.move_y(-1*sensor_width)
       e3DMatrixPrinting.move_x(bladder_spacing*(num_bladders-0.5)+sensor_length_offset)
       e3DMatrixPrinting.travel_mode()
        
    
    print_bladder_spacers()
    print_bladders()
    print_bladder_bus_line()
    print_sensor()


print_pneunet(num_bladders = 9, num_layers = 12, substrate_zero = -73.805)
#print_pneunet(num_bladders = 3, num_layers = 3, substrate_zero = -55.08)

e3DPGlobals.g.view('matplotlib')
#e3DPGlobals.g.view()
e3DPGlobals.g.teardown()
    