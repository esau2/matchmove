#coding=utf-8

"""
@Time:2018.11.17
@Author: Liwei

使用说明：
支持maya2018
选择一个物体的动画曲线上需要平滑的关键帧，然后运行这个脚本。
支持一个物体同时选中多根动画曲线进行平滑。
不支持多个物体同时选中。

"""

import maya.cmds as mc
import pymel.core as pm

# 将动画曲线名称转化重动画曲线属性
def convert_aniName_to_attr(ani_name , geo_name):
    length = len(ani_name)
    for i in range(length):
        if ani_name[length-i-1] == '_':
            at = geo_name+'.'+ani_name[length-i:]
            return at

# 获取选中的动画曲线列表和选中的物体名称,只能选中一个物体
def getSelectAnimaitonCurve():
    selectGeo = pm.ls(sl=True)
    if len(selectGeo) == 1:
        geo_name =  selectGeo[0].name()
        print 'geo_name: ', geo_name
        aniCurve_list = pm.keyframe(selectGeo[0],query=True,sl=True,name = True)
		
        aniCurve_list_attr = []
        for item in aniCurve_list:
            aniCurve_list_attr.append(convert_aniName_to_attr(item,geo_name))
			
        print 'aniCurve_list: ',aniCurve_list
        print 'attr: ' , aniCurve_list_attr
        return aniCurve_list,geo_name,aniCurve_list_attr 
    else:
        print '错误，只能选中一个物体'
     
 
# 获取关键帧的时间序列
def get_time(key_info):
    bbb = []
    for item in key_info:
        bbb.append(item[0])
    return bbb
 
# 获取关键帧的值列表
def get_value(key_info):
    aaa = []
    for item in key_info:
        aaa.append(item[1])
    return aaa
    

# 三点线性平滑
def linearSmooth3(in_value, N):
    out_value = range(N)
    if N < 3:
        for i in range(N-1):
            out_value[i] = in_value[i]        
    else:
        out_value[0] = ( 5.0 * in_value[0] + 2.0 * in_value[1] - in_value[2] ) / 6.0
        #print out_value[0] 
        for i in range(1,N-1):        
            out_value[i] = ( in_value[i-1] + in_value[i] + in_value[i+1] ) / 3.0
            print 'out_value[i]:', out_value[i]         
        out_value[N-1] = ( 5.0 * in_value[N-1]+ 2.0*in_value[N-2]- in_value[N-3])/6.0
    return out_value

# 获取单根曲线上的关键帧时间，平滑值，数量
def smooth_single_curve(curves):
    key_info = pm.keyframe(curves,q=True,tc=True,vc=True, sl=True) #��ȡѡ�еĶ��������Ϲؼ�֡��ʱ���ֵ
    key_num = len(key_info)
    print key_info, key_num 
    
    key_value = get_value(key_info)
    print 'key_value: ', key_value
    
    key_time = get_time(key_info)
    print 'key_time:' , key_time
    
    smooth_value = linearSmooth3(key_value, key_num)
    print 'smooth_value: ',smooth_value
    
    return key_time,smooth_value,key_num
    
###########################################

if __name__=='__main__':

    current_aniCurve_list, current_geo_name, current_aniCurve_attr = getSelectAnimaitonCurve()
    
    print current_aniCurve_list,current_geo_name,current_aniCurve_attr

    #current_keytime,current_smooth_value = smooth_single_curve('pSphere1_translateX')

    for item in current_aniCurve_list:
        current_attr = convert_aniName_to_attr(item,current_geo_name) 
        print 'current_attr:', current_attr
        
        current_keytime, current_smooth_value, current_num = smooth_single_curve(item)
        
        print current_num

        for i in range(current_num):
            pm.setKeyframe(item, v=current_smooth_value[i], t=current_keytime[i])
