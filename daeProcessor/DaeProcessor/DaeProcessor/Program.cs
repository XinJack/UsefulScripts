using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;

namespace DaeProcessor
{
    class Program
    {
        static void Main(string[] args)
        {
            string daePath = @"G:\BIM+GIS\IFCModels\demo.dae";
            string outDaeDir = @"G:\BIM+GIS\IFCModels\demo";

            if (!File.Exists(daePath))
            {
                Console.WriteLine(string.Format("Error >> Dae文件: \"{0}\" 不存在", daePath));
                Console.Read();
                return;
            }


            if (daePath.Substring(daePath.IndexOf('.') + 1)  != "dae")
            {
                Console.WriteLine(string.Format("Error >> 文件: \"{0}\" 不是一个Dae文件", daePath));
                Console.Read();
                return;
            }


            if (!Directory.Exists(outDaeDir))
            {
                Console.WriteLine(string.Format("Warning >> 输出文件夹 \"{0}\" 不存在，将进行创建", outDaeDir));
                Directory.CreateDirectory(outDaeDir);
                Console.WriteLine(string.Format("Output >> \"{0}\" 创建成功", daePath));
            }

            XmlDocument doc = new XmlDocument();
            doc.Load(daePath);
            XmlNode assetTag = doc.GetElementsByTagName("asset")[0];
            XmlNodeList materialTags = doc.GetElementsByTagName("material");
            XmlNodeList effectTags = doc.GetElementsByTagName("effect");
            XmlNodeList geometryTags = doc.GetElementsByTagName("geometry");
            XmlNodeList nodeTags = doc.GetElementsByTagName("node");
            XmlNode sceneTag = doc.GetElementsByTagName("scene")[0];

            // 居然同一个id属性可以有多个实例，坑
            Dictionary<string, List<XmlNode>> tagDict = new Dictionary<string, List<XmlNode>>();
            foreach (XmlNode geometry in geometryTags)
            {
                string geometryId = geometry.Attributes["id"].Value;
                if (!tagDict.ContainsKey(geometryId))
                {
                    tagDict.Add(geometryId, new List<XmlNode>());
                }
                tagDict[geometryId].Add(geometry);
            }

            foreach (XmlNode material in materialTags)
            {
                string materialId = material.Attributes["id"].Value;
                if (!tagDict.ContainsKey(materialId))
                {
                    tagDict.Add(materialId, new List<XmlNode>());
                }
                tagDict[materialId].Add(material);
            }

            foreach (XmlNode effect in effectTags)
            {
                string effectId = effect.Attributes["id"].Value;
                if (!tagDict.ContainsKey(effectId))
                {
                    tagDict.Add(effectId, new List<XmlNode>());
                }
                tagDict[effectId].Add(effect);
            }

            int count = 0;
            string outDaePath = "";
            foreach (XmlNode node in nodeTags)
            {
                XmlNode instanceGeometry = node.LastChild;
                string geometryId = instanceGeometry.Attributes["url"].Value.Substring(1);
                List<XmlNode> geometryList = tagDict[geometryId];
                //XmlNode geometry = tagDict[geometryId];
                outDaePath = outDaeDir + "\\" + geometryId + "-" + count.ToString() + ".dae";

                //创建一个新的文档
                XmlDocument new_doc = new XmlDocument();
                //创建根节点COLLADA
                XmlNode collada = new_doc.CreateElement("COLLADA");
                XmlAttribute colladaXmlns = new_doc.CreateAttribute("xmlns");
                colladaXmlns.Value = "http://www.collada.org/2005/11/COLLADASchema";
                collada.Attributes.Append(colladaXmlns);
                XmlAttribute colladaVersion = new_doc.CreateAttribute("version");
                colladaVersion.Value = "1.4.1";
                collada.Attributes.Append(colladaVersion);

                //向COLLADA节点添加asset节点
                collada.AppendChild(new_doc.ImportNode(assetTag, true));

                //创建一个library_effects节点和一个library_materials节点
                XmlNode library_effects = new_doc.CreateElement("library_effects");
                XmlNode library_materials = new_doc.CreateElement("library_materials");

                XmlNodeList instanceMaterials = instanceGeometry.FirstChild.FirstChild.ChildNodes;
                foreach (XmlNode instanceMaterial in instanceMaterials)
                {
                    string materialId = instanceMaterial.Attributes["target"].Value.Substring(1);
                    //XmlNode material = tagDict[materialId];
                    List<XmlNode> materialList = tagDict[materialId];

                    //向library_materials节点添加material子节点
                    foreach (XmlNode material in materialList)
                    {
                        library_materials.AppendChild(new_doc.ImportNode(material, true));

                        XmlNode instanceEffect = material.FirstChild;
                        string effectId = instanceEffect.Attributes["url"].Value.Substring(1);
                        List<XmlNode> effectList = tagDict[effectId];

                        //向library_effects节点添加effect子节点
                        foreach (XmlNode effect in effectList)
                        {
                            library_effects.AppendChild(new_doc.ImportNode(effect, true));
                        }
                    }
                    //library_materials.AppendChild(new_doc.ImportNode(material, true));

                    //XmlNode instanceEffect = material.FirstChild;
                    //string effectId = instanceEffect.Attributes["url"].Value.Substring(1);
                    //XmlNode effect = tagDict[effectId];

                    ////向library_effects节点添加effect子节点
                    //library_effects.AppendChild(new_doc.ImportNode(effect, true));

                }

                //向COLLADA节点添加library_effects节点
                collada.AppendChild(library_effects);

                //向COLLADA节点添加library_materials节点
                collada.AppendChild(library_materials);

                //创建一个library_geometries节点并加入到COLLADA节点
                XmlNode library_geometries = new_doc.CreateElement("library_geometries");
                foreach (XmlNode geometry in geometryList)
                {
                    library_geometries.AppendChild(new_doc.ImportNode(geometry, true));
                }
                //library_geometries.AppendChild(new_doc.ImportNode(geometry, true));
                collada.AppendChild(library_geometries);

                //创建一个library_visual_scenes节点并加入到COLLADA节点
                XmlNode library_visual_scenes = new_doc.CreateElement("library_visual_scenes");
                XmlNode visual_scene = new_doc.CreateElement("visual_scene");
                XmlAttribute visual_scene_id = new_doc.CreateAttribute("id");
                visual_scene_id.Value = "IfcOpenShell";
                visual_scene.Attributes.Append(visual_scene_id);
                visual_scene.AppendChild(new_doc.ImportNode(node, true));
                library_visual_scenes.AppendChild(visual_scene);
                collada.AppendChild(library_visual_scenes);

                //向COLLADA节点添加scene节点
                collada.AppendChild(new_doc.ImportNode(sceneTag, true));

                //将COLLADA节点添加到文档中
                new_doc.AppendChild(collada);

                Console.WriteLine(string.Format("Output >> 开始写入第{0}个文件", count + 1));
                //Console.WriteLine(new_doc.OuterXml);
                //using (XmlWriter writer = XmlWriter.Create(outDaePath))
                //{
                //    new_doc.WriteTo(writer);
                //}
                new_doc.Save(outDaePath);
                Console.WriteLine(string.Format("Output >> 第{0}个文件写入完成", count + 1));
                Console.WriteLine("==============================");

                count++;
            }
            Console.WriteLine(string.Format("Output >> 总共需要输出{0}个文件， 实际生成了{1}个文件", nodeTags.Count, count));
            Console.WriteLine("Success >> 全部输出完成");
            Console.Read();
        }
    }
}
