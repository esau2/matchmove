#coding=utf-8
import maya.cmds as mc
import pymel.core as pm

#删除场景中的灯光
def delete_light():
    light_all = pm.ls(type='light')
    for item in light_all:
        pm.delete(item.getTransform())

# 获取场景的开始和结束时间
def get_env():
    maya_env = pm.Env()
    end_time = maya_env.getAnimEndTime()
    start_time = maya_env.getAnimStartTime()
    return start_time, end_time

# 获取场景中的非默认摄影机,返回摄影机的transform节点
def get_cam():
    cam_all = pm.ls(type = 'camera')
    cam_default = ['top','front','side','persp']
    cam_nodes = []
    track_list = ['pf_data', 'SynthEyesGroup', '3de']
    for item in cam_all:
        if item.getTransform() not in cam_default:
            cam_nodes.append(item.getTransform())
    for item in cam_nodes:
        if item.getParent() in track_list:
            shot_cam = item
    return cam_nodes, shot_cam

# 分别获取参考物体， 动画物体， 静态场景, 返回物体的transform节点
def get_geo_by_type():

    geo_nodes = pm.ls(type = 'mesh')
    ref_nodes = []
    ani_geo_nodes = []
    env_geo_nodes = []
    for item in geo_nodes:
        item_transform_node = item.getTransform()
        if item_transform_node.isReferenced():
            ref_nodes.append(item_transform_node)
        elif is_ani_obj(item_transform_node):
            ani_geo_nodes.append(item_transform_node)
        else:
            env_geo_nodes.append(item_transform_node)
    return ref_nodes, ani_geo_nodes, env_geo_nodes

# 获取场景中的locator,返回locator的transform节点
def get_locator():
    locator_shape = pm.ls(type='locator')
    locator_transform = []
    for item in locator_shape:
        locator_transform.append(item.getTransform())
    return locator_transform

# 判断物体是否带有动画
def is_ani_obj(node):
    nodeTx = '%s.tx' % node
    nodeTy = '%s.ty' % node
    nodeTz = '%s.tz' % node

    nodeRx = '%s.rx' % node
    nodeRy = '%s.ry' % node
    nodeRz = '%s.rz' % node

    nodeSx = '%s.sx' % node
    nodeSy = '%s.sy' % node
    nodeSz = '%s.sz' % node

    keyframe_num = range(9)
    keyframe_num[0] = pm.keyframe(nodeTx, query=True, keyframeCount=True)
    keyframe_num[1] = pm.keyframe(nodeTy, query=True, keyframeCount=True)
    keyframe_num[2] = pm.keyframe(nodeTz, query=True, keyframeCount=True)
    keyframe_num[3] = pm.keyframe(nodeRx, query=True, keyframeCount=True)
    keyframe_num[4] = pm.keyframe(nodeRy, query=True, keyframeCount=True)
    keyframe_num[5] = pm.keyframe(nodeRz, query=True, keyframeCount=True)
    keyframe_num[6] = pm.keyframe(nodeSx, query=True, keyframeCount=True)
    keyframe_num[7] = pm.keyframe(nodeSy, query=True, keyframeCount=True)
    keyframe_num[8] = pm.keyframe(nodeSz, query=True, keyframeCount=True)
    i = 0
    for item in keyframe_num:
        if item > 1:
            #print keyframe_num[i]
            return True
        i = i+1
    return False


# 检查场景的设置：帧率 单位  帧数
def check_fps_unit():

    pass


def check_time():

    pass

# 将父级的transfrom变换烘焙到子物体中
def bake_animation(child_geo, start_time, end_time):
    print 'child_geo:', child_geo
    temp = pm.duplicate(child_geo)[0]
    print 'temp:', temp
    pm.parent(temp, world=True)
    pc = pm.parentConstraint(child_geo, temp)
    sc = pm.scaleConstraint(child_geo, temp, maintainOffset=True)
    pm.bakeResults(temp, time=(start_time, end_time), simulation=True)
    pm.delete(pc)
    pm.delete(sc)
    child_geo_name = child_geo.nodeName()
    pm.delete(child_geo)
    temp.rename(child_geo_name)
    print 'new_temp:', temp
    return temp

def lock_camera():
    pass



def main():

    # 删除所有灯光
    delete_light()

    #建立新的组结构
    if not pm.objExists('mm'):
        pm.group(em=True, name='mm')
        pm.group(em=True, name='reference_points')
        pm.group(em=True, name='env_geo')
        pm.group(em=True, name='ani_geo')
        pm.parent('reference_points', 'mm')
        pm.parent('env_geo', 'mm')
        pm.parent('ani_geo', 'mm')

    cam_nodes, shot_cam = get_cam()

    start_time, end_time = get_env()

    # 重新分配跟踪信息的组
    track_data = shot_cam.getParent()
    track_child = track_data.getChildren()
    print track_child
    new_track_child = []
    for item in track_child:
        item = bake_animation(item, start_time, end_time)
        new_track_child.append(item)
    pm.delete(track_data)

    ref_nodes, ani_geo_nodes, env_geo_nodes = get_geo_by_type()

    locator_nodes = get_locator()

    # 获取非默认节点
    nodes = pm.ls(type='transform')
    cam_default = ['top', 'front', 'side', 'persp']
    root_nodes = []
    for item in nodes:
        if not item.getParent():
            if item not in cam_default:
                root_nodes.append(item)

    # 获取root下的节点
    valid_nodes = []
    for item in root_nodes:
        if not item.isReferenced():
            valid_nodes.append(item)

    # 根据root节点类型重新组织到mm组下
    for item in valid_nodes:
        if item in env_geo_nodes:
            pm.parent(item, 'env_geo')
        elif item in ani_geo_nodes:
            pm.parent(item, 'ani_geo')
        elif item in locator_nodes:
            pm.parent(item, 'reference_points')
        elif item in cam_nodes:
            pm.parent(item, 'mm')

    print 'new_track_child:', new_track_child

    for item in new_track_child:
        try:
            type = item.getShape().type()
        except:
            type = 'group'

        if type == 'mesh':
            print "mesh:",item
            if is_ani_obj(item):
                pm.parent(item, 'ani_geo')
            else:
                pm.parent(item, 'env_geo')
        elif type == 'camera':
            print 'cam:', item
            pm.parent(item, 'mm')
            cam_attr_list = range(10)
            cam_attr_list[0] = '%s.tx' % item
            cam_attr_list[1] = '%s.ty' % item
            cam_attr_list[2] = '%s.tz' % item

            cam_attr_list[3] = '%s.rx' % item
            cam_attr_list[4] = '%s.ry' % item
            cam_attr_list[5] = '%s.rz' % item

            cam_attr_list[6] = '%s.sx' % item
            cam_attr_list[7] = '%s.sy' % item
            cam_attr_list[8] = '%s.sz' % item

            cam_attr_list[9] = '%s.visibility' % item

            camShape_attr_list = range(15)
            camShape_attr_list[0] = '%sShape.horizontalFilmAperture' % item
            camShape_attr_list[1] = '%sShape.verticalFilmAperture' % item
            camShape_attr_list[2] = '%sShape.focalLength' % item
            camShape_attr_list[3] = '%sShape.lensSqueezeRatio' % item
            camShape_attr_list[4] = '%sShape.fStop' % item
            camShape_attr_list[5] = '%sShape.focusDistance' % item
            camShape_attr_list[6] = '%sShape.shutterAngle' % item
            camShape_attr_list[7] = '%sShape.centerOfInterest' % item
            camShape_attr_list[8] = '%sShape.locatorScale' % item
            camShape_attr_list[9] = '%sShape.aiUseGlobalShutter' % item
            camShape_attr_list[10] = '%sShape.aiEnableDOF' % item
            camShape_attr_list[11] = '%sShape.motionBlurOverride' % item
            camShape_attr_list[12] = '%sShape.aiFov' % item
            camShape_attr_list[13] = '%sShape.aiHorizontalFov' % item
            camShape_attr_list[14] = '%sShape.aiVerticalFov' % item

            for cam_attr in cam_attr_list:
                pm.setAttr(cam_attr,lock=True)

            for camShape_attr in camShape_attr_list:
                pm.setAttr(camShape_attr, lock=True)
        elif type == 'group':
            print 'group:', item
            pm.parent(item, 'reference_points')







