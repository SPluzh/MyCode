def limitPerJointInfluence(jnt_limit = 4, deselect = True):
	'''
	This script limits the influence for the number of joints affecting the deformation of a vertex.
	Select any skinned mesh vertices or geometry and runCommand >> 
	
	limitPerJointInfluence(jnt_limit = 4)
	
	'''
	import pymel.core as pm
	import time, sys, math

	start_time = time.time()

	initialSel = pm.ls(sl = True)
	if isinstance(initialSel[0], pm.nt.Transform):
		cmds.ConvertSelectionToVertices(initialSel)
		vertSel = pm.selected()
		geo = vertSel[0].node()
	else:
		vertSel = pm.selected()
		geo = vertSel[0].node()

	his = pm.listHistory(geo, pdo = True)
	sknCls = pm.ls(his, typ = 'skinCluster')[0]
	vertsList = cmds.ls(sl  = True, fl = True)
	
	for verts in vertsList:
		vertWt = pm.skinPercent(sknCls, verts, q = True, value = True)
		vertTrans = pm.skinPercent(sknCls, verts, q = True, transform = None)
	
		dict = {}
		for x in range(len(vertWt)):
			if vertWt[x] == 0:
				pass
			else:
				dict[vertTrans[x]] = vertWt[x]
	
		sorted_dict = sorted(dict.items(), key=lambda item: item[1], reverse = True)
		if len(sorted_dict) > jnt_limit:
			rangeLen = -1 * (len(sorted_dict) - (jnt_limit-1))
			for x in range(-1, rangeLen, -1):
				pm.skinPercent(sknCls, verts, tv = [sorted_dict[x][0], 0])
	
	lenVert = len(vertsList)
	
	if deselect == True:
		abc = geo.getTransform()
		pm.select(abc)
		pm.select(cl = True)
	sys.stdout.write('\n %s Verts weight refined in. ' " %s seconds " % (lenVert, (time.time() - start_time)))
	#### End of Script ####

limitPerJointInfluence(jnt_limit = 1, deselect = False)
