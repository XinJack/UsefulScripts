'''
	用于将dea模型中的构件拆分到单独的dae文件中
'''

def process(dae_path, base_output_dae_path):
	'''
		将dae文件中的一个个构件分开到多个dae文件中
	'''
	import xml.dom.minidom
	import os
	import time

	if not os.path.exists(dae_path):
		print('路径%s不存在' % dae_path)
	# 文件夹路径
	output_dir = base_output_dae_path + '\\' + dae_path[dae_path.rfind('\\') + 1: dae_path.find('.')]
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	doc = xml.dom.minidom.parse(dae_path)

	impl = xml.dom.minidom.getDOMImplementation()

	# 获取基础的Tag
	asset_tag = doc.getElementsByTagName('asset')[0]
	effect_tags = doc.getElementsByTagName('effect')
	material_tags = doc.getElementsByTagName('material')
	geometry_tags = doc.getElementsByTagName('geometry')
	node_tags = doc.getElementsByTagName('node')
	scene_tag = doc.getElementsByTagName('scene')[0]

	print('effect_tags: ', len(effect_tags))
	print('material_tags: ', len(material_tags))
	print('geometry_tags: ', len(geometry_tags))
	print('node_tags: ', len(node_tags))

	# 遍历所有的node
	count = 0
	for node in node_tags:

		# 新建一个dae文档对象
		new_doc = impl.createDocument(None, 'COLLADA', None)

		# 获取新建dae文档对象的根节点COLLADA节点
		new_doc_root = new_doc.documentElement
		new_doc_root.setAttribute('xmlns', 'http://www.collada.org/2005/11/COLLADASchema')
		new_doc_root.setAttribute('version', '1.4.1')
		
		# 将asset节点添加到新建的dae文档对象中
		new_doc_root.appendChild(asset_tag)

		# 将当前node节点添加到新建的dae文档对象中
		library_visual_scenes = new_doc.createElement('library_visual_scenes')
		visual_scene = new_doc.createElement('visual_scene')
		visual_scene.setAttribute('id', 'IfcOpenShell')
		visual_scene.appendChild(node)
		library_visual_scenes.appendChild(visual_scene)
		new_doc_root.appendChild(library_visual_scenes)

		# 获取当前node对应的geometry的id
		instance_geometry = node.getElementsByTagName('instance_geometry')[0]
		geometry_id = instance_geometry.getAttribute('url')[1:]

		geometrys = getElementsById(geometry_tags, geometry_id)

		# 将当前geometry节点添加到新建的dae文档对象中
		library_geometries = new_doc.createElement('library_geometries')
		for geometry in geometrys:
			library_geometries.appendChild(geometry)
		new_doc_root.appendChild(library_geometries)

		# 将material节点和effect节点的父节点
		library_materials = new_doc.createElement('library_materials')
		library_effects = new_doc.createElement('library_effects')

		instance_materials = node.getElementsByTagName('instance_material')

		for instance_material in instance_materials:
			material_id = instance_material.getAttribute('target')[1:]
			materials = getElementsById(material_tags, material_id)

			for material in materials:
				library_materials.appendChild(material)
				instance_effect = material.getElementsByTagName('instance_effect')[0]
				effect_id = instance_effect.getAttribute('url')[1:]
				effects = getElementsById(effect_tags, effect_id)
				for effect in effects:
					library_effects.appendChild(effect)
			

		# 将material节点和effect节点添加到新建的dae文档对象中
		new_doc_root.appendChild(library_materials)	
		new_doc_root.appendChild(library_effects)

		# 将scene节点添加到新建的dae文档对象中
		new_doc_root.appendChild(scene_tag)

		# encoding='utf-8'很重要，解决了编码问题
		output_file = output_dir + '\\' + dae_path[dae_path.rfind('\\') + 1: dae_path.find('.')] + '-' + geometry_id + '-' + str(count) + '.dae'
		with open(output_file, mode='w', encoding='utf-8') as f:
			print('start writing...')
			print(count)
			new_doc.writexml(f, addindent='', newl='', encoding='utf-8')
			print('done writing...')
			print('#'*100)
			count += 1
			print('current count', count)
		print('-'*20)


def getElementsById(doms, id):
	'''
		根据id从查找相关dom
	'''
	result = list()
	for dom in doms:
		dom_id = dom.getAttribute('id')
		if dom_id == id:
			result.append(dom)
	return result

if __name__ == '__main__':
	dae_path = 'G:\\BIM+GIS\\IFCModels\\demo.dae'
	base_output_dae_path = 'G:\\BIM+GIS\\IFCModels'

	# 1iUTeNLx945xp4Fd_hV3Bb存在两次

	# dae_path = input('请输入dae文件路径: ')
	# base_output_dae_path = input('请输入生成文件所在的路径: ')

	process(dae_path, base_output_dae_path)