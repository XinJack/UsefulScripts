'''
	利用命令行工具调用gltf-pipeline提供的命令行工具来将某个文件夹下的所有gltf文件转换成glb文件
'''
def process(gltf_dir_path):
	import os
	if not os.path.exists(gltf_dir_path):
		print("文件夹%s不存在" % gltf_dir_path)
		return

	for fileName in os.listdir(gltf_dir_path):
		if fileName.endswith('.gltf'): 
			gltf_file_path = gltf_dir_path + '/' + fileName
			out_file_path = gltf_dir_path + '/' + fileName[0: fileName.find('.')] + '.glb'
			cmd = '''cd G:/BIM+GIS/gltf-pipeline/bin & \
			node gltf-pipeline.js -i "%s" -o "%s" -b 
			''' % (gltf_file_path, out_file_path)
			os.system(cmd)
			print('%s --> done' % cmd)

if __name__ == '__main__':
	gltf_dir_path = "G:\\BIM+GIS\IFCModels\\demo\\gltf"
	process(gltf_dir_path)