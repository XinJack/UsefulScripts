def process(dae_dir_path, out_dir_path):
	import os
	if not os.path.exists(dae_dir_path):
		print('Path "%s" does not exist' % dae_dir_path)
		return
	if not os.path.exists(out_dir_path):
		os.makedirs(out_dir_path)

	files = os.listdir(dae_dir_path)
	for file in files:
		if file.endswith('.dae'):
			file = dae_dir_path + '\\' + file
			out_file = out_dir_path + '\\' + file[file.rfind('\\') + 1: file.find('.')] + '.gltf'
			cmd = ''' cd C:/Users/dell/Documents/Projects/BIM+GIS & \
				collada2gltf.exe -f "%s" -o "%s" -e
			''' % (file, out_file)
			print(cmd)
			os.system(cmd)

if __name__ == '__main__':
	dae_dir_path = 'C:\\Users\\dell\\Desktop\\Lab'
	out_dir_path = 'C:\\Users\\dell\\Desktop\\Lab\\gltf'
	process(dae_dir_path, out_dir_path)
