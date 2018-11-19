#coding=utf-8
#
# 3DE4.script.name:	Import PF 2D Tracks...
#
# 3DE4.script.version:	v1.1
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
#
#
# 3DE4.script.comment:	Imports PF 2D tracking curves from an Ascii file.
#
#

#
# main script...

"""
@Author：Liwei
@date： 2018.11.09

使用说明
将import_pf_2d_tracks.py 复制到 3de的脚本目录C:\Program Files\3DE4_win64_r5\sys_data\py_scripts
然后启动3de软件，从菜单3DE> File > Import > import PF 2D Tracks

pf在usertrack节点 或者autotrack节点中 选择需要导出的track，然后点击export按钮，可以导出pf的2dtrack信息，保存为txt文件

然后在3de软件中 使用 import PF 2D Tracks命令，导入刚才保存的txt文件，即可

"""



def getTotalnumber(f):
	file_context =  f.readlines()
	track_number = 0
	for line in file_context:
		if line =='\n':
			track_number = track_number+1
	print 'track_number:', track_number
	return track_number


c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	frames	= tde4.getCameraNoFrames(c)
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)
	
	req	= tde4.createCustomRequester()
	tde4.addFileWidget(req,"file_browser","Filename...","*.txt")
	tde4.addOptionMenuWidget(req,"mode_menu","","Always Create New Points","Replace Existing Points If Possible")
	
	ret	= tde4.postCustomRequester(req,"Import PF 2D Tracks...",500,120,"Ok","Cancel")
	if ret==1:
		create_new = tde4.getWidgetValue(req,"mode_menu")
		path	= tde4.getWidgetValue(req,"file_browser")
		if path!=None:
			#
			# main block...
			
			f	= open(path,"r")
			if not f.closed:
				#确定跟踪点总数
				#total_track_number = '5' 
				#string	= f.readline() #跟踪点总数
				 
				n	=  getTotalnumber(f)
				print  "n : ", n
				f.close()

				f	= open(path,"r")
				
				string	= f.readline()
				print "first_line:", string
				string	= f.readline()
				print "second_line:",string 
				string	= f.readline()
				print "third_line:",string
				string	= f.readline()
				print "forth_line:", string
				#跳过开始的4行
				for i in range(n):
					#name	= f.readline() #跟踪点名字
					name = f.readline() #读取空行
					name = f.readline()  #读取track名字
					name	= name.strip()
					print 'name : ', name
					name = name[1:-1]
					print "raw_name: ", name
					p	= tde4.findPointByName(pg,name)
					if create_new==1 or p==None: p = tde4.createPoint(pg)
					tde4.setPointName(pg,p,name)
					
					string = '0'
					#string	= f.readline()	#跟踪点颜色
					color	= int(string)
					print "color :", color
					tde4.setPointColor2D(pg,p,color)
					
					l	= []
					for j in range(frames): l.append([-1.0,-1.0])
					#string = f.readlin()   #跟踪数据的帧数
					string_start_frame	= int(f.readline())  
					print 'string_start_frame : ', string_start_frame 
					string_end_frame = int(f.readline())
					print 'string_end_frame : ', string_end_frame

					n0	= string_end_frame - string_start_frame + 1
					print "frames_number:", n0
					for j in range(n0):
						string	= f.readline()
						line	= string.split()
						l[int(line[0])-1] = [float(line[1])/width,float(line[2])/height]
					tde4.setPointPosition2DBlock(pg,p,c,1,l)

					print "*"*10
				f.close()
			else:
				tde4.postQuestionRequester("Import PF 2D Tracks...","Error, couldn't open file.","Ok")
			
			# end main block...
			#
else:
	tde4.postQuestionRequester("Import PF 2D Tracks...","There is no current Point Group or Camera.","Ok")

