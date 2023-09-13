from uber_cam_tool.maya_utilities import get_all_user_cameras


def get_frame_range(camera, camera_dict):
    """
    Get the frame range of a camera stored in a dict
    :param camera_dict:
    :param camera:
    :return:
    """
    frame_in = camera_dict[camera]['Frame_In']
    frame_out = camera_dict[camera]['Frame_Out']
    frame_range = frame_in, frame_out
    return frame_range


def check_frame_overlaps(selected_camera, camera_dict, frame_in, frame_out):
    warnings = []
    for k, v in camera_dict.items():
        if k != selected_camera:
            if camera_dict[k]['Frame_In'] <= frame_in <= camera_dict[k]['Frame_Out']:
                warning = 'Frame range overlaps previously set frame range'
                warnings.append(warning)
            elif camera_dict[k]['Frame_In'] <= frame_out <= camera_dict[k]['Frame_Out']:
                warning = 'Frame range overlaps previously set frame range'
                warnings.append(warning)
            elif camera_dict[k]['Frame_In'] >= frame_in \
                    and frame_out >= camera_dict[k]['Frame_Out']:
                warning = 'Frame range overlaps previously set frame range'
                warnings.append(warning)
    return warnings


def create_user_camera_dict():
    """
    Create a dictionary containing dictionaries for all user created cameras with Frame In and Out values
    :rtype dict
    :return camera_dict:
    """
    camera_transforms = get_all_user_cameras()
    camera_dict = {}
    for camera in camera_transforms:
        camera_dict[camera] = {}
        camera_dict[camera]['Frame_In'] = 0
        camera_dict[camera]['Frame_Out'] = 0
    return camera_dict
