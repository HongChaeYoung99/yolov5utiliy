from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
from PIL import Image

def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))

if __name__ == '__main__':
    class_name_to_id_mapping = {'Plate': 0, 'N_1': 1, 'N_2': 2, 'N_3': 3, 'N_4': 4, 'N_5': 5, 'N_6': 6, 'N_7': 7,
                                'N_8': 8,
                                'N_9': 9, 'S_노': 10, 'S_러': 11, 'S_마': 12, 'S_로': 13, 'S_소': 14, 'S_다': 15, 'S_나': 16,
                                'S_거': 17, 'S_두': 18, 'S_서': 19, 'S_오': 20, 'S_조': 21, 'S_더': 22, 'S_너': 23, 'S_모': 24,
                                'S_부': 25, 'S_수': 26, 'S_무': 27, 'S_우': 28, 'S_주': 29, 'S_가': 30, 'S_어': 31, 'S_고': 32
        , 'S_보': 33, 'S_구': 34, 'S_버': 35, 'S_라': 36, 'S_머': 37, 'S_도': 38, 'S_저': 39, 'S_루': 40, 'S_누': 41, 'N_0': 42}

    class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))
    txt_src = "C:/Users/user/Documents/B/labels/src2"
    txt_list = [os.path.join(txt_src, x) for x in os.listdir(txt_src) if x[-3:] == "txt"]
    image_dir = "C:/Users/user/Documents/B/images/src/"
    for txt in txt_list:
        root = Element("annotation")
        folder = Element("folder")
        folder.text = "iamges"
        root.append(folder)

        filename = Element("filename")
        filename.text = os.path.basename(txt).replace("txt", "jpg")
        root.append(filename)

        path = Element("path")
        path.text = image_dir + os.path.basename(txt).replace("txt", "jpg")
        root.append(path)

        image_src = image_dir + os.path.basename(txt).replace("txt", "jpg")
        image1 = Image.open(image_src)  # 이미지를 연다
        w, h = image1.size  # 이미지 사이즈를 넣는다
        size = Element("size")
        root.append(size)

        sub_width = SubElement(size, "width")
        sub_width.text = w
        sub_height = SubElement(size, "height")
        sub_height.text = h

        f = open(txt, "r")
        info_list = []
        while True:
            line = f.readline()
            if not line: break
            line = line.replace("\n", "").split(" ")
            info_list.append(line)
        f.close()
        plate_size = []
        for line in info_list:
            object1 = Element("object")
            root.append(object1)
            sub_name = SubElement(object1, "name")
            print(line)

            sub_name.text = class_id_to_name_mapping[int(line[0])]
            if sub_name.text == "Plate":
                line[1] = line[1] * w
                line[2] = line[2] * h
                line[3] = line[3] * w
                line[4] = line[4] * h

                plate_size.append(line[2])
                plate_size.append(line[3])

                sub_bndbox = SubElement(object1, "bndbox")
                sub_sub_xmin = SubElement(sub_bndbox, "xmin")
                float_1 = line[1]
                float_1 = float(float_1)
                sub_sub_xmin.text = line[1] - line[3]/2
                plate_size.append(float(sub_sub_xmin.text))

                sub_sub_ymin = SubElement(sub_bndbox, "ymin")
                sub_sub_ymin.text = float(line[2]) - float(line[4])/2
                plate_size.append(float(sub_sub_ymin.text))
                sub_sub_xmax = SubElement(sub_bndbox, "xmax")
                sub_sub_xmax.text = float(line[1]) + float(line[3])/2

                sub_sub_ymax = SubElement(sub_bndbox, "ymax")
                sub_sub_ymax.text = float(line[2]) + float(line[4])/2

            else:
                line[1] = line[1] * plate_size[0]
                line[2] = line[2] * plate_size[1]
                line[3] = line[3] * plate_size[0]
                line[4] = line[4] * plate_size[1]

                sub_bndbox = SubElement(object1, "bndbox")
                sub_sub_xmin = SubElement(sub_bndbox, "xmin")
                sub_sub_xmin.text = float(line[1]) - float(line[3]) / 2 + plate_size[2]

                sub_sub_ymin = SubElement(sub_bndbox, "ymin")
                sub_sub_ymin.text = float(line[2]) - float(line[4]) / 2 + plate_size[3]

                sub_sub_xmax = SubElement(sub_bndbox, "xmax")
                sub_sub_xmax.text = float(line[1]) + float(line[3]) / 2 + plate_size[2]

                sub_sub_ymax = SubElement(sub_bndbox, "ymax")
                sub_sub_ymax.text = float(line[2]) + float(line[4]) / 2 + plate_size[3]

            _pretty_print(root)

            tree = ElementTree(root)

            fileName = "C:/Users/user/Documents/B/labels/src4" + os.path.basename(txt)
            with open(fileName, "wb") as file:
                tree.write(file, encoding='utf-8', xml_declaration=True)