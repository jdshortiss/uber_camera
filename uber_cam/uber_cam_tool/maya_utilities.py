import maya.cmds as cmds


def get_all_user_cameras():
    """
    Get all user created cameras in the scene and return it as a list
    :rtype list
    :return camera_transforms:
    """
    all_user_cameras = [c for c in cmds.ls(cameras=True) if not cmds.camera(c, q=True, startupCamera=True)]
    camera_transforms = [cmds.listRelatives(c, p=True)[0] for c in all_user_cameras]
    return camera_transforms


def get_keyframes(camera_dict):
    """
    Iterate through each camera to find and store new keyframes and transform attributes at this frame
    :param dict camera_dict:
    :rtype dict
    :return dict_frames:
    """
    dict_frames = {}
    for k, v in camera_dict.items():
        camera_dict = camera_dict.get(k, {})
        start = camera_dict['Frame_In']
        end = camera_dict['Frame_Out']
        frames = [start, end]
        keyframes = []
        animation_curves = cmds.keyframe(k, query=True, name=True)
        if animation_curves:
            for curve in animation_curves:
                keyframes = cmds.keyframe(curve, query=True, timeChange=True)
            for keyframe in keyframes:
                if start <= keyframe <= end:
                    frames.append(keyframe)

        transform_attrs = ['translateX', 'translateY', 'translateZ',
                           'rotateX', 'rotateY', 'rotateZ',
                           'scaleX', 'scaleY', 'scaleZ']

        for frame in frames:
            attr_list = []
            for attribute in transform_attrs:
                cmds.currentTime(frame)
                attr_list.append(cmds.getAttr(k + '.' + attribute, time=frame))
            dict_frames[frame] = attr_list
    return dict_frames


def set_keyframes(camera, dict_frames):
    """
    Set keyframes on uber camera from our created dict_frames
    :param camera:
    :param dict_frames:
    :return:
    """
    for frame, attrs in dict_frames.items():
        cmds.setKeyframe(camera, attribute='translateX', t=frame, value=attrs[0])
        cmds.setKeyframe(camera, attribute='translateY', t=frame, value=attrs[1])
        cmds.setKeyframe(camera, attribute='translateZ', t=frame, value=attrs[2])
        cmds.setKeyframe(camera, attribute='rotateX', t=frame, value=attrs[3])
        cmds.setKeyframe(camera, attribute='rotateY', t=frame, value=attrs[4])
        cmds.setKeyframe(camera, attribute='rotateZ', t=frame, value=attrs[5])
        cmds.setKeyframe(camera, attribute='scaleX', t=frame, value=attrs[6])
        cmds.setKeyframe(camera, attribute='scaleY', t=frame, value=attrs[7])
        cmds.setKeyframe(camera, attribute='scaleZ', t=frame, value=attrs[8])

