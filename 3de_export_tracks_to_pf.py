#coding=utf-8
#
# 3DE4.script.name:	Export 2D Tracks to PF ...
#
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Main Window::3DE4::File::Export
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
#
# 3DE4.script.comment:	Writes the 2D tracking curves of all selected points to an Ascii file.
#
#

#
# main script...

c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	n	= tde4.getCameraNoFrames(c)
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)
	
	p	= tde4.getContextMenuObject()			# check if context menu has been used, and retrieve point...
	if p!=None:
		pg	= tde4.getContextMenuParentObject()	# retrieve point's parent pgroup (not necessarily being the current one!)...
		l	= tde4.getPointList(pg,1)
	else:
		l	= tde4.getPointList(pg,1)		# otherwise use regular selection... 获取跟踪点列表
	if len(l)>0:
		req	= tde4.createCustomRequester()
		tde4.addFileWidget(req,"file_browser","Filename...","*.txt")	
		tde4.addTextFieldWidget(req,"frame_offset_field","Frame Offset","0")
		ret	= tde4.postCustomRequester(req,"Export 2D Tracks To PFtrack v2...",500,0,"Ok","Cancel")
		if ret==1:
			path	= tde4.getWidgetValue(req,"file_browser")
			offset	= int(tde4.getWidgetValue(req,"frame_offset_field"))
			if offset<0: offset = 0
			if path!=None:
				#
				# main block...
				
				if path.find(".txt",len(path)-4)==-1: path += ".txt"
				f	= open(path,"w")
				if not f.closed:
					print "start:SSSSSSSSSSSSSSSSSSSSSSSSSSS"
					f.write('# "Name"');f.write("\n")
					f.write('# clipNumber');f.write("\n")
					f.write('# frameCount');f.write("\n")
					f.write('# frame, xpos, ypos, similarity');f.write("\n")


					#f.write("%d\n"%(len(l))) #写入跟踪点的总数
					for point in l:
						f.write("\n") #写入每个跟踪点信息前的空行
						name	= tde4.getPointName(pg,point)	#获取跟踪点的名字
						f.write('\"3de'+name+'\"'); f.write("\n")
						#color	= tde4.getPointColor2D(pg,point)
						#f.write("%d\n"%(color))

						f.write('1') ; f.write("\n") #写入摄影机组

						c2d	= tde4.getPointPosition2DBlock(pg,point,c,1,n)
						
						n0	= 0
						for v in c2d:
							print "v:" , v
							if v[0]!=-1.0 and v[1]!=-1.0: n0 += 1
						print "n0:", n0
						f.write("%d\n"%(n0))   #写入跟踪点持续的帧数
						frame	= 1+offset
						valid_frame = []
						for v in c2d:
							if v[0]!=-1.0 and v[1]!=-1.0:
								valid_frame.append(frame)
							frame +=1
						#f.write(str(valid_frame[0])); f.write("\n")  #写入跟踪点起始帧
						#print "track_info_start:", valid_frame[0]
						#f.write(str(valid_frame[-1])); f.write("\n") #写入跟踪点结束帧
						#print "track_info_end:",valid_frame[-1]
						 


						frame = 1+offset
						for v in c2d:
							if v[0]!=-1.0 and v[1]!=-1.0: f.write("%d %.6f %.6f \n"%(frame,v[0]*width,v[1]*height)) #写入每个点的信息
							frame	+= 1
						#f.write("*"*10) #

					f.close()
				else:
					tde4.postQuestionRequester("Export 2D Tracks...","Error, couldn't open file.","Ok")
				
				# end main block...
				#
				
	else:
		tde4.postQuestionRequester("Export 2D Tracks...","There are no selected points.","Ok")
else:
        tde4.postQuestionRequester("Export 2D Tracks...","There is no current Point Group or Camera.","Ok")


"""
read me：

copy this script to  C:\Program Files\3DE4_win64_r5\sys_data\py_scripts

in 3de， select tracks which you want， right check mouse，then choose command “Export 2D Tracks to PF”


"""