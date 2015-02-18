# -*- coding: utf-8 -*-
"""

Filename: FuelOctobot.py
Author: Ryan L. Truby
Affiliation: Lewis Research Group, Harvard University
Data: 2015.01.19

Description:
    This code prints the downstream components of a "fancy" octobot. These 
    components include the actuators and all networks interconnecting them. 
    Additionally, the fuel reservoir is printed upstream of a logic module.
    All interconnects to the logic module are also printed. This code is an
    adaptation based off Daniel Fitzgerald's script "FuelSpider.py". 
    
"""

from mecode import G
from math import sqrt

import numpy as np
import matplotlib.pyplot as plt

# Soft robot printing libraries
import e3DMatrixPrinting
import MultiMaterial

# Soft robot features
import Actuators
import e3DPGlobals
import FancyOctobot
import LogicModule
import OctobotLogicModule

# Define the export file that will hold the generated G code
import os
cur_filepath = os.path.dirname(os.path.realpath(__file__))
splitted = cur_filepath.split('/')
n = len(splitted)
cur_dir = ''.join((dir+'/') for dir in splitted[:n-1])
exportFileDir = cur_dir + "soft_robotics_octobot/FuelOctobot.pgm"
print "Exporting to file " + str(exportFileDir)

e3DPGlobals.init_G(exportFileDir)

'''
    Note from RTruby:
        On Jan 19, 2015, I went through all of Dan Fitzgerald's code, and made
        sure I understood anything up until this comment.
        
        GO BACK AND REVIEW THE CODE BELOW AND WHAT IT'S DOING.
'''

def print_fuel_spider(flow_connector_height_abs, centerline_x, flow_connectors_centerline_offset, flow_connectors_back_y):    
    plenum_bottom_height = -3 #FancyOctobot.mold_top - 7.6
    plenum_top_height = FancyOctobot.mold_top - 5
    plenum_meander_print_height = (plenum_top_height + plenum_bottom_height)/2.0
    plenum_meander_print_height = -6 # added 2015.02.03, changed from 6.9 to 6 on 2015.02.04
    plenum_meander_print_height = -5.5 #added 2015.02.06
    #line below commented out on 2015.02.03
    #module_top_print_height = -1 # max(LogicModule.module_hole_top+0.2,flow_connector_height_abs) # TODO: Compensate for this if it ends up being below the flow_connector_height_abs
    module_top_print_height = -2.3    
    module_print_height_back = -4.3 # 2015.02.03 was -1
    module_print_height_back = -3.5 # changed 2015.02.06
    e3DPGlobals.g.absolute()
    
    LogicModule.init(centerline = centerline_x, offset = flow_connectors_centerline_offset, print_height = module_top_print_height)
    OctobotLogicModule.hook_module_into_fancy_spider()
        
       
    def print_plenum_meander(Left):
        x_offset_mult = (-1 if Left else 1)
        
        '''
        Note from RTruby, 2015.01.20:
            Below, I have commented out code writted by Dan Fitzgerald that 
            allowed us to print meander-shaped fuel reservoirs for the soft
            robot. These meander designs are not practical, and I have edited
            my code for Octobot mold's to have a straight line connected to the
            inlets of our soft logic module.
            
            The code begins below...
            
        # Print a meander, starting in the hole and ending with a back inlet
        LogicModule.interface_with_hole(Left=Left, Front = False, to_cliff = False)
        e3DMatrixPrinting.move_z_abs(module_print_height_back, vertical_travel_speed = e3DMatrixPrinting.default_z_drag_speed)
        e3DMatrixPrinting.travel_mode()
        
        # meander layers
        n_meander_layers = 0
        meander_layer_separation_z = 0.75 
        
        # meander properties
        meander_back_y = -50 # -38.6 - 20
        meander_front_y = -44.5 # LogicModule.module_back_edge_y - 1
        max_meander_lobe_width_x = 3
        meander_separation = 1
        meander_connection_dwell_time = 1
        meander_print_speed = 0.6
        meander_inner_x_offset = 0.75
        n_longitudinal_meanders = 2*int((max_meander_lobe_width_x / (0.0+meander_separation))/2.0)
        meander_outer_x_offset = meander_inner_x_offset+n_longitudinal_meanders*meander_separation
        print "Meander outer x offset = " + str(meander_outer_x_offset)
        n_transverse_meanders = 2*int(((meander_front_y - meander_back_y)/meander_separation)/2)
        meander_separation_transverse = (meander_front_y - meander_back_y)/n_transverse_meanders
        connection_overlap = 0.5
        
        # start the meander
        e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*meander_inner_x_offset, y=meander_back_y-connection_overlap)
        e3DMatrixPrinting.print_mode(print_height_abs = plenum_meander_print_height, print_speed = meander_print_speed)
        e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*meander_outer_x_offset, y=meander_back_y-connection_overlap)         # move to the back left corner of the meander (for the right lobe - LEFT is False)
        
        #NOTE: all meanders must end in the opposite corner
        longitudinal = True
        for meander_layer in range(n_meander_layers):
            if (longitudinal):
                foreward = True
                for meander in range(n_longitudinal_meanders):
                    e3DPGlobals.g.abs_move(y=(meander_front_y if foreward else meander_back_y))
                    e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*(meander_outer_x_offset-(meander+1)*meander_separation))
                    foreward = not foreward
                e3DPGlobals.g.abs_move(y=meander_front_y)
            else:
                across = True
                for meander in range(n_transverse_meanders):
                    e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*(meander_outer_x_offset if across else meander_inner_x_offset))
                    e3DPGlobals.g.abs_move(y=meander_front_y-(meander+1)*meander_separation_transverse)
                    across = not across
                e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*meander_outer_x_offset, y= meander_back_y)
            longitudinal = not longitudinal
            e3DMatrixPrinting.move_z_abs(height=plenum_meander_print_height+(meander_layer+1)*meander_layer_separation_z)

            # get in position to safely go to the hole
            safe_hole_connection_x_offset=1
            if (n_meander_layers % 2 ==0): # if there's an even number of meanders (we ended at the back outer corner instead of the front inside corner)
                e3DMatrixPrinting.move_z_abs(height=plenum_meander_print_height+(n_meander_layers)*meander_layer_separation_z)
                e3DPGlobals.g.feed(e3DMatrixPrinting.default_print_speed)
                e3DPGlobals.g.abs_move(y=meander_front_y)
                e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*meander_inner_x_offset)
            e3DMatrixPrinting.move_z_abs(height=module_print_height_back)
            e3DPGlobals.g.feed(e3DMatrixPrinting.default_print_speed)
            e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*safe_hole_connection_x_offset, y=LogicModule.module_back_edge_y)
            hole_pos = (LogicModule.back_left_hole_pos if Left else LogicModule.back_right_hole_pos)
            e3DPGlobals.g.abs_move(x=hole_pos[0], y=hole_pos[1]) # move above the hole
            e3DPGlobals.g.dwell(meander_connection_dwell_time)
            e3DMatrixPrinting.travel_mode()
            
            # INLET
        
            # starting point of trace to needle inlet
            meander_end_x_offset = meander_inner_x_offset
            meander_end_y = meander_back_y-connection_overlap
            meander_end_z = plenum_meander_print_height    
                    
            inlet_centerline_offset = 2 
            inlet_print_height = flow_connector_height_abs
            inlet_back_tip_y = -52 #  -29
        
            # print from the end of the meander to  an inlet
            e3DPGlobals.g.abs_move(x=centerline_x + x_offset_mult*meander_end_x_offset, y = meander_end_y) # go ever the end of the meander
            e3DMatrixPrinting.print_mode(print_height_abs = meander_end_z)
            e3DPGlobals.g.dwell(meander_connection_dwell_time)
            e3DPGlobals.g.abs_move(x=centerline_x + x_offset_mult*inlet_centerline_offset, y=inlet_back_tip_y+e3DMatrixPrinting.default_inlet_length, z=inlet_print_height)
            e3DPGlobals.g.feed(e3DMatrixPrinting.default_inlet_print_speed)
            e3DPGlobals.g.abs_move(y=inlet_back_tip_y)
            print "Inlet back tip Y = " + str(inlet_back_tip_y) + "."
            e3DMatrixPrinting.travel_mode()
            
        '''
        
        # Begin to print the fuel reservoirs; first interface with the inlets
        # of the soft logic module
        LogicModule.interface_with_hole(Left=Left, Front = False, to_cliff = False)
        # Is the line below needed? Leave it commented for now, but I think it is just redudant code that is already implemented in the call to interface_with_hole
        e3DMatrixPrinting.move_z_abs(module_print_height_back, vertical_travel_speed = e3DMatrixPrinting.default_z_drag_speed)
        e3DMatrixPrinting.travel_mode()
        
        meander_front_y = -41 # 2015.02.03 - switched from -45, -40 was too close
        meander_back_y = -45 # 2015.02.03 - switched from -50
        meander_inner_x_offset = 3 # was originally 0.75 in Dan's code
        meander_outer_x_offset = 3 # was originally > 2 mm
        connection_overlap = 0.0   # what is this? it was originally in Dan's code as 0.5 originally
        meander_print_speed = 0.5 # switched from 0.6 on 2014.02.06
        meander_connection_dwell_time = 1
        
        e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*meander_inner_x_offset, y=meander_back_y-connection_overlap)
        e3DMatrixPrinting.print_mode(print_height_abs = plenum_meander_print_height, print_speed = meander_print_speed)
        # Again, is the code below redundant?
        #e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*meander_outer_x_offset, y=meander_back_y-connection_overlap)   
        
        # Note from RTruby, 2015.01.21 - I didn't add/edit code block from Dan under
        # the comment listed above that starts, "#NOTE: all meanders must end in opposite corner"
        
        # Now, connect the fuel line to the module inlets
        safe_hole_connection_x_offset = meander_inner_x_offset
        e3DMatrixPrinting.move_z_abs(height = plenum_meander_print_height) # redundant?
        e3DPGlobals.g.feed(e3DMatrixPrinting.default_print_speed)
        e3DPGlobals.g.abs_move(y = meander_front_y)
        e3DPGlobals.g.abs_move(x = centerline_x+x_offset_mult*meander_inner_x_offset)
        e3DMatrixPrinting.move_z_abs(height = module_print_height_back)
        e3DPGlobals.g.feed(e3DMatrixPrinting.default_print_speed)
        ############if things are working, looking around these lines of code, RTruby, 2015.01.21########
        e3DPGlobals.g.abs_move(x=centerline_x+x_offset_mult*safe_hole_connection_x_offset, y=LogicModule.module_back_edge_y)
        e3DPGlobals.g.abs_move(y = LogicModule.module_back_edge_y)
        hole_pos = (LogicModule.back_left_hole_pos if Left else LogicModule.back_right_hole_pos)
        e3DPGlobals.g.abs_move(x=hole_pos[0], y=hole_pos[1]) # move above the hole
        e3DPGlobals.g.dwell(meander_connection_dwell_time)
        e3DMatrixPrinting.travel_mode()                
        
    print_plenum_meander(Left=True)
    print_plenum_meander(Left=False)

# SET THESE: LEG ACTUATOR ECOFLEX ZEROS
left_zero = -59.2112
right_zero = -59.2489

FancyOctobot.print_robot(ecoflex_zero_left = left_zero, ecoflex_zero_right = right_zero, func_print_internal_soft_logic=print_fuel_spider)     

#The line below commented out on 2014.09.10 by RTruby, for Experiment C-95
e3DPGlobals.g.view('matplotlib')
#e3DPGlobals.g.view()
e3DPGlobals.g.teardown()

