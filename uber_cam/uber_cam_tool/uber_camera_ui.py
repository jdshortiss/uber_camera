import maya.cmds as cmds

from uber_cam_tool.maya_utilities import get_keyframes, set_keyframes, get_all_user_cameras
from uber_cam_tool.utilities import check_frame_overlaps, create_user_camera_dict


class UberCamUI(object):

    create_user_camera_dict()

    def __init__(self):
        if cmds.window('uber_camera_ui', exists=True):
            cmds.deleteUI('uber_camera_ui', window=True)

        window = cmds.window('uber_camera_ui', title='Uber Camera', widthHeight=(300, 250))

        form_layout = cmds.formLayout(numberOfDivisions=100)

        text_scroll_list = cmds.textScrollList('camera_list', numberOfRows=10, allowMultiSelection=False)
        frame_in_text = cmds.text(label='Frame In')
        self.frame_in_field = cmds.intField('frame_in_field')
        frame_out_text = cmds.text(label='Frame Out')
        self.frame_out_field = cmds.intField('frame_out_field')
        submit_button = cmds.button(label='Set Frame Range', command=self.submit_frame_range)
        uber_button = cmds.button(label='Create Uber Camera', command=self.create_uber_camera)
        update_button = cmds.button(label='Update', command=self.update)

        cmds.formLayout(form_layout,
                        edit=True,
                        attachForm=[(text_scroll_list, 'top', 10), (text_scroll_list, 'left', 10),
                                    (text_scroll_list, 'right', 10), (frame_in_text, 'left', 10),
                                    (frame_in_text, 'bottom', 100), (frame_out_text, 'left', 10),
                                    (frame_out_text, 'bottom', 70), (submit_button, 'left', 10),
                                    (submit_button, 'bottom', 10), (uber_button, 'right', 10),
                                    (uber_button, 'bottom', 10), (update_button, 'right', 10),
                                    (update_button, 'bottom', 10)],
                        attachControl=[(self.frame_in_field, 'left', 15, frame_in_text),
                                       (self.frame_in_field, 'bottom', -15, frame_in_text),
                                       (self.frame_out_field, 'left', 5, frame_out_text),
                                       (self.frame_out_field, 'bottom', -15, frame_out_text)])

        cmds.textScrollList(text_scroll_list,
                            edit=True,
                            append=UberCamUI.camera_transforms,
                            selectCommand=self.select_camera)

        cmds.showWindow(window)

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
        frame_in, frame_out = self.get_frame_range(selected_camera, UberCamUI.camera_dict)
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


myWindow = UberCamUI()
