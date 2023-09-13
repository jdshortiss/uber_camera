import sys
import os

script_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
tools_folder = os.path.join(script_folder, 'uber_cam_tool')

if tools_folder not in sys.path:
    sys.path.append(tools_folder)

import utilities
import maya_utilities
import uber_camera_qt_ui

uber_camera_qt_ui.show_dialog()
