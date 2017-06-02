// var fs = require('fs');
var glb2b3dm = require('./glb2b3dm');
var Cesium = require('cesium');
var cp = require('./cp.js');
var fs = require('fs-extra');
var Promise = require('bluebird');

// glb和gltf文件所在的文件夹
var glbDir = "G:/BIM+GIS/IFCModels/demo/gltf/glb";
var gltfDir = "G:/BIM+GIS/IFCModels/demo/gltf"

// 构造位置矩阵
var modelMatrix = Cesium.Transforms.eastNorthUpToFixedFrame(
                  Cesium.Cartesian3.fromDegrees(-75.62898254394531, 40.02804946899414, 0.0));
var transform = [];
for(var i = 0; i < 16; ++i){
	transform.push(modelMatrix[i.toString()]);
}


// 读取glb文件夹下的所有glb文件
// fs.readdir(glbDir, function(err, glbFiles) {
// 	if (err) throw err;

// 	var index = 0;
// 	console.log(glbFiles);
// 	process(index, glbFiles);
// });

// 读取glb文件夹下的所有glb文件
fs.readdir(glbDir).then(function(glbFiles) {
	// 下面的操作是耗时的异步操作，使用promise来处理
	var promises = [];

	glbFiles.forEach(function(glbFile) {
		console.log(glbFile);
		// 构造输出文件名称
		var fileName = glbFile.substring(0, glbFile.indexOf('.'));
		// 读取glb文件
		promises.push(readGLBandOutput(fileName, glbFile));
	});

	Promise.all(promises)
		.then(function(result){
			console.log(result);
		})
		.catch(function(err) {
			console.log(err);
		});

}).catch(function(err) {
	console.log('读取glb文件夹出错 ==> ', glbDir);
});


function readGLBandOutput(fileName, glbFile) {
	return fs.readFile(glbDir + '/' + glbFile).then(function(glb) {
		console.log('成功读取glb文件 ==> ', glbFile);
		
		// 将glb内容转化为b3dm
		var b3dm = glb2b3dm(glb);
		// 构造b3dm文件夹的路径
		var b3dmDir = glbDir + '/' + fileName;
		return fs.ensureDir(b3dmDir)
		 .then(function() {
		 	// 构造b3dm文件的路径
		 	var b3dmFile = b3dmDir + '/' + fileName + '.b3dm';

		 	// 写入b3dm文件
		 	return fs.writeFile(b3dmFile, b3dm)
		 	 .then(function() {
		 	 	// 读取b3dm文件对应的gltf文件
		 	 	var gltfFile = gltfDir + '/' + fileName + '.gltf';
		 	 	return fs.readFile(gltfFile)
		 	 	 .then(function(gltf) {
		 	 	 	// 获取该gltf文件的内容并计算包围核
					var gltfJson = JSON.parse(gltf);
					var result = cp(gltfJson);
						
					// 构造tileset的内容
					var tilesetJson = {
						"asset": {
							"version": "0.0"
						},
						"geometricError": 40,
						"root": {
							"transform": transform,
							"boundingVolume": {
								"sphere": [
									result.center.x,
									result.center.y,
									result.center.z,
									result.radius
								]
							},
							"geometricError": 0,
							"refine": "replace",
							"content": {
								"url": "./" + fileName + ".b3dm"
							}
							// ,
							// "children": [
							// 	{
							// 		"boundingVolume": {
							// 			"sphere": [
							// 				result.center.x,
							// 				result.center.y,
							// 				result.center.z,
							// 				result.radius
							// 			]
							// 		},
							// 		"geometricError": 0,
							// 		"content": {
							// 			"url": "./" + fileName + ".b3dm"
							// 		}
							// 	}
							// ]
						}
					};

					// 输出tileset文件
					var tilesetFile = b3dmDir + '/tileset.json';
					return fs.writeJson(tilesetFile, tilesetJson)
					 .then(function() {
					 	return Promise.resolve('输出tileset文件成功 ==> ', tilesetFile);
					 })
					 .catch(function(err) {
					 	console.log('输出tileset文件失败 ==> ', tilesetFile);
					 	return Promise.resolve(err);
					 });
		 	 	 })
		 	 	 .catch(function(err) {
		 	 	 	console.log('读取gltf文件失败 ==> ', gltfFile);
		 	 	 	Promise.resolve(err);
		 	 	 })
		 	 })
		 	 .catch(function(err) {
		 	 	console.log('写入b3dm文件失败 ==> ', b3dmFile);
		 	 	return Promise.resolve(err);
		 	 })
		 })
		 .catch(function(err) {
			console.log('创建b3dm文件夹失败 ==> ', b3dmDir);
			return Promise.resolve(err);
		 });
	}).catch(function(err) {
		console.log('读取glb文件失败 ==> ', glbFile);
		return Promise.resolve(err);
	})
}


// function process(index, glbFiles) {
// 	if (index >= glbFiles.length) return;

// 	// 获取每个glb文件的名字->用于构造输出文件路径
// 	var glbFile = glbFiles[index];
// 	var fileName = glbFile.substring(0, glbFile.indexOf('.'));

// 	// 读取glb文件
// 	fs.readFile(glbDir + '/' + glbFile, function(err, glb){
// 		console.log('读取glb文件： ', glbFile);

// 		// 将glb内容转化为b3dm
// 		var b3dm = glb2b3dm(glb);
// 		// 构造b3dm文件的路径
// 		var b3dmDir = glbDir + '/' + fileName;
// 		if (!fs.exists(b3dmDir)) {
// 			fs.mkdir(b3dmDir);
// 		}
// 		var b3dmFile = b3dmDir + '/' + fileName + '.b3dm';
// 		console.log(b3dm);
// 		// 输出b3dm
// 		fs.writeFile(b3dmFile, b3dm, function(err) {
// 			if (err) throw err;

// 			console.log('输出b3dm文件成功：', b3dmFile);

// 			// 读取与该glb文件相对应的gltf文件
// 			var gltfFile = gltfDir + '/' + fileName + '.gltf';
// 			fs.readFile(gltfFile, function(err, gltf) {
// 				if (err) throw err;
// 				console.log('读取gltf文件成功：', gltfFile);
				
// 				// 获取该gltf文件的内容并计算包围核
// 				var gltfJson = JSON.parse(gltf);
// 				var result = cp(gltfJson);
					
// 				// 构造tileset的内容
// 				var tilesetJson = {
// 					"asset": {
// 						"version": "0.0"
// 					},
// 					"geometricError": 40,
// 					"root": {
// 						"transform": transform,
// 						"boundingVolume": {
// 							"sphere": [
// 								result.center.x,
// 								result.center.y,
// 								result.center.z,
// 								result.radius
// 							]
// 						},
// 						"geometricError": 0,
// 						"refine": "replace",
// 						"content": {
// 							"url": "./" + fileName + ".b3dm"
// 						}
// 						// ,
// 						// "children": [
// 						// 	{
// 						// 		"boundingVolume": {
// 						// 			"sphere": [
// 						// 				result.center.x,
// 						// 				result.center.y,
// 						// 				result.center.z,
// 						// 				result.radius
// 						// 			]
// 						// 		},
// 						// 		"geometricError": 0,
// 						// 		"content": {
// 						// 			"url": "./" + fileName + ".b3dm"
// 						// 		}
// 						// 	}
// 						// ]
// 					}
// 				};

// 				// 输出tileset
// 				tilesetJson = JSON.stringify(tilesetJson);
// 				var tilesetFile = b3dmDir + '/tileset.json';
// 				fs.writeFile(tilesetFile, tilesetJson, function(err) {
// 					if(err) throw err;
// 					console.log('输出tileset文件成功：', tilesetFile);
// 					console.log('============================')
// 					process(index + 1, glbFiles);
// 				});
// 			});
// 		});
// 	});
// }