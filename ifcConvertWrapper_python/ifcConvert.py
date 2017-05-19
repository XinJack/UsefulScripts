'''
	使用命令行调用ifcconvert将IFC文件转换为dae文件
'''
def process(ifc_file, out_file):
	'''
		使用命令行调用ifcconvert将IFC文件转换为dae文件
		ifc_file: IFC文件路径
		out_file: dae文件路径
	'''
	import os
	cmd = '''cd G:/BIM+GIS/IfcOpenShell/installed-vs2012-x64/bin & \
	ifcconvert.exe "%s" "%s"
	''' % (ifc_file, out_file)
	os.system(cmd)


if __name__ == '__main__':
	ifc_file = 'G:\\BIM+GIS\\IFCModels\\cabr architectrue.ifc'
	out_file = 'G:\\BIM+GIS\\IFCModels\\cabr architectrue.dae'
	process(ifc_file, out_file)