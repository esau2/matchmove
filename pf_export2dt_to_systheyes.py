#coding=utf-8
"""
@Author： Liwei
@Date： 2018.11.02

使用说明：
将export2dt_to_systheyes .py文件复制到C:\Program Files\The Pixel Farm\PFTrack 2017\nodes目录下

在pf中使用python面板下的 export2dto systheyes节点，连接在usertrack节点之后，然后运行，选择保存路径

在systheyes中 使用import》import 2d track path  导入保持的txt文件
"""



import pfpy, sys
from pfpy import Camera, Tracker, Lens, Mesh, Clip, Group, Cloud


def pfNodeName():
	return 'Exmport 2dt to systheyes'

def pfAutoRun():
	# by default, this script does not run automatically
	return False
'''
def stripQuotes(s) :
	return s[1:len(s)-2]
'''

def main() :
	shot = pfpy.getClipRef(0)
	shot_start_frame = shot.getInPoint()
	shot_end_frame= shot.getOutPoint()
	shot_width = shot.getFrameWidth()
	shot_height = shot.getFrameHeight()
	print("start_frame: {0} ,end_frame: {1}\n".format(shot_start_frame, shot_end_frame))
	print("shot_width: {0}, shot_height: {1} \n".format(shot_width, shot_height))


	track_number= pfpy.getNumTrackers()	#获取跟踪点数目
	valid_frame = shot_end_frame - shot_start_frame +1

	print "tracker number: {0} \n".format(track_number)
	track_info = []
	for index in range(track_number):
		t= pfpy.getTrackerRef(index, 0)
		track_name = t.getName()  #获取跟踪点名字
		for current_frame in range(shot_start_frame,shot_end_frame+1):
			if t.validPosition(current_frame):
				track_position = t.getTrackPosition(current_frame) 	#获取跟踪点2D信息
				track_u = 2*(track_position[0]/shot_width)-1.0
				track_v = 1.0-2*(track_position[1]/shot_height)   #转换成systheyes中的uv信息

				print track_name,current_frame,track_u,track_v

				track_line = "{0} {1} {2} {3}\n".format(track_name,current_frame,track_u,track_v)
				track_info.append(track_line)


	filename = raw_input("choose a file to output:")


	with open(filename, 'w') as f:
		f.writelines(track_info)



	# ask for a filename
	#filename= raw_input("")

	# open the file to write
	
	#f= open(filename, 'w')


'''
	# read contents
	l= f.readline()
	while len(l) > 0 :
		if l[0] == '\"' :

			# primary camera?
			p= f.readline()
			if stripQuotes(p) == "Primary" :

				# create a new tracker
				t= Tracker.new(stripQuotes(l))

				# how many frames?
				n= int(f.readline())

				print "Creating tracker", t.getName(), n, "frames"

				for idx in range(0, n, 1) :
					d= f.readline().split()
					if len(d) == 4 :

						# fetch the frame number	
						frame= int(d[0])

						# first or last frame?
						if idx == 0 :
							t.setInPoint(frame)
						elif idx == n-1 :
							t.setOutPoint(frame)

						# store position
						t.setTrackPosition(frame, float(d[1]), float(d[2]))

						# store matching score
						t.setTrackScore(frame, 1.0-float(d[3]))

		l= f.readline()
	print
'''

