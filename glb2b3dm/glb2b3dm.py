'''
	利用命令行工具调用3d-tiles-tools提供的命令行工具来将某个文件夹下的所有glb文件转换成3dbm文件
'''
def process(glb_dir_path):
	import os
	if not os.path.exists(glb_dir_path):
		print("文件夹%s不存在" % glb_dir_path)
		return

	for fileName in os.listdir(glb_dir_path):
		if fileName.endswith('.glb'): 
			glb_file_path = glb_dir_path + '/' + fileName
			out_file_path = glb_dir_path + '/' + fileName[0: fileName.find('.')] + '/' + fileName[0: fileName.find('.')] + '.b3dm'
			cmd = '''cd G:/BIM+GIS/3d-tiles-tools/tools/bin & \
			node 3d-tiles-tools.js glbToB3dm -i "%s" -o "%s"
			''' % (glb_file_path, out_file_path)
			os.system(cmd)
			print('%s --> done' % cmd)

if __name__ == '__main__':
	glb_dir_path = "G:/BIM+GIS/IFCModels/smallWall/gltf/glb"
	process(glb_dir_path)