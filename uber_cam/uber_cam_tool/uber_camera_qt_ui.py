import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from uber_cam_tool.maya_utilities import get_all_user_cameras, get_keyframes, set_keyframes
from uber_cam_tool.utilities import create_user_camera_dict, check_frame_overlaps, get_frame_range


class UberCamUI(QtWidgets.QDialog):

    camera_dict = create_user_camera_dict()

    def __init__(self):
        super(UberCamUI, self).__init__()

        self.setWindowTitle("Uber Camera")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        label = QtWidgets.QLabel("Select Camera:")
        layout.addWidget(label)

        self.camera_list = QtWidgets.QListWidget()
        layout.addWidget(self.camera_list)
        self.camera_list.setFixedHeight(100)

        self.populate_camera_list()

        self.camera_list.itemClicked.connect(self.select_camera)

        accepted_range = QtGui.QIntValidator(1001, 9999)

        self.frame_in = QtWidgets.QLineEdit()
        frame_in_label = QtWidgets.QLabel("Frame In:")
        self.frame_in.setValidator(accepted_range)
        self.frame_out = QtWidgets.QLineEdit()
        frame_out_label = QtWidgets.QLabel("Frame Out:")
        self.frame_out.setValidator(accepted_range)

        layout.addWidget(frame_in_label)
        layout.addWidget(self.frame_in)
        layout.addWidget(frame_out_label)
        layout.addWidget(self.frame_out)

        frames_button = QtWidgets.QPushButton("Set Frame Range")
        frames_button.clicked.connect(self.submit_frame_range)
        layout.addWidget(frames_button)

        uber_button = QtWidgets.QPushButton("Create Uber Camera")
        uber_button.clicked.connect(self.create_uber_camera)
        layout.addWidget(uber_button)

        uber_button = QtWidgets.QPushButton("Refresh")
        uber_button.clicked.connect(self.refresh)
        layout.addWidget(uber_button)

    def populate_camera_list(self):
        """
        Get all user-created cameras and add each camera to the list
        :return:
        """
        camera_transforms = get_all_user_cameras()
        for camera in camera_transforms:
            self.camera_list.addItem(camera)

    def submit_frame_range(self, *args):
        """
        Update frame in and out of selected camera
        :param args:
        :return:
        """
        warning = None
        if self.camera_list.selectedItems():
            selected_camera = self.camera_list.selectedItems()[0].text()
            frame_in = int(self.frame_in.text())
            frame_out = int(self.frame_out.text())
            warnings = check_frame_overlaps(selected_camera, UberCamUI.camera_dict, frame_in, frame_out)
            if len(warnings) > 0:
                cmds.confirmDialog(title='Frame Range Update Failed', message=warning)
            else:
                UberCamUI.camera_dict[selected_camera]['Frame_In'] = frame_in
                UberCamUI.camera_dict[selected_camera]['Frame_Out'] = frame_out
                cmds.confirmDialog(title='Frame Range Updated', message='Frame range updated for ' + selected_camera)
        else:
            warning = 'Please select a camera to submit a frame range'
            cmds.confirmDialog(title='Frame Range Update Failed', message=warning)

    def select_camera(self, *args):
        """
        Select a camera from the UI list to update frame in and out
        :param self:
        :param args:
        :return:
        """
        selected_camera = self.camera_list.selectedItems()[0].text()
        frame_in, frame_out = get_frame_range(selected_camera, UberCamUI.camera_dict)
        self.frame_in.setText(str(frame_in))
        self.frame_out.setText(str(frame_out))

    @staticmethod
    def create_uber_camera(*args):
        """
        Create a new camera and set keyframes using data from the global dict
        :param args:
        :return:
        """
        uber_camera_dict = {}
        for k, v in UberCamUI.camera_dict.items():
            if UberCamUI.camera_dict[k]['Frame_Out'] != 0:
                uber_camera_dict[k] = {}
                uber_camera_dict[k]['Frame_In'] = UberCamUI.camera_dict[k]['Frame_In']
                uber_camera_dict[k]['Frame_Out'] = UberCamUI.camera_dict[k]['Frame_Out']
        if uber_camera_dict:
            uber_camera = cmds.camera(name='uber_camera')[0]
            dict_frames = get_keyframes(uber_camera_dict)
            set_keyframes(uber_camera, dict_frames)
        else:
            warning = 'Cannot create Uber Camera - No frames have been set.'
            cmds.confirmDialog(title='Frame Range Update Failed', message=warning)

    def refresh(self, *args):
        """
        Update camera list after changes are made
        :param args:
        :return None:
        """
        self.camera_list.clear()
        UberCamUI.camera_dict = create_user_camera_dict()
        self.populate_camera_list()


def show_dialog():
    if cmds.window("UberCamUI", exists=True):
        cmds.deleteUI("UberCamUI", window=True)

    maya_main_window = None
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == "MayaWindow":
            maya_main_window = obj
            break

    if maya_main_window:
        dialog = UberCamUI()
        dialog.setParent(maya_main_window)
        dialog.setWindowFlags(QtCore.Qt.Window)
        dialog.show()


show_dialog()
