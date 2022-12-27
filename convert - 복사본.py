#xml파일에서 자른 이미지에 맞춰서 좌표를 변경해 txt파일로 저장하는 코드
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
from shutil import move

#데이터를 담아둔 폴더
src = 'C:/Users/user/Documents/B/'
#xml에서 정보 추출해서 info_dict딕셔너리에 넣기
#xml파일 하나씩 들어옴
def extract_info_from_xml(xml_file):
    #파일 열기
    f=open(xml_file,'r', encoding="UTF-8" )
    xml_text = f.read()
    #xml파일 읽을 준비
    root = ET.fromstring(xml_text)
    f.close()
    #info_dict 하나당 파일 하나의 정보가 담김
    info_dict = {}
    info_dict['bboxes'] = [] #object들 넣을 곳

    for elem in root:
        if elem.tag == "filename":
            info_dict['filename'] = os.path.basename(xml_file).replace("xml","jpg")


        elif elem.tag == "size":

            image_size = []

            for subelem in elem:
                image_size.append(int(subelem.text))

            info_dict['image_size'] = tuple(image_size)

        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)
                    info_dict['bboxes'].append(bbox)

    return info_dict


class_name_to_id_mapping = {'Plate': 0, 'N_1': 1, 'N_2': 2, 'N_3': 3, 'N_4': 4, 'N_5': 5, 'N_6': 6, 'N_7': 7, 'N_8': 8,
                            'N_9': 9, 'S_노': 10, 'S_러': 11, 'S_마': 12, 'S_로': 13, 'S_소': 14, 'S_다': 15, 'S_나': 16,
                            'S_거': 17, 'S_두': 18, 'S_서': 19, 'S_오': 20, 'S_조': 21, 'S_더': 22, 'S_너': 23, 'S_모': 24,
                            'S_부': 25, 'S_수': 26, 'S_무': 27, 'S_우': 28, 'S_주': 29, 'S_가': 30, 'S_어': 31, 'S_고': 32
                               , 'S_보': 33, 'S_구': 34, 'S_버': 35, 'S_라': 36, 'S_머': 37, 'S_도': 38, 'S_저': 39, 'S_루': 40, 'S_누': 41,'N_0':42}

def convert_to_yolov5(info_dict):
    print_buffer = []
    plate_size = []
    class_id = 9999
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid Class.")

        #Plate객체일 경우 plate_soze에 그들의 값을 넣어주고 중앙값들은 왼쪽 위 점의 좌표만큼 줄여준다.
        if class_id == 0:
            plate_size.append(b["xmin"])
            plate_size.append(b["ymin"])
            w, h ,c = info_dict['image_size']
            b_center_x = (b["xmin"] + b["xmax"]) / 2
            b_center_y = (b["ymin"] + b["ymax"]) / 2
            b_width = (b["xmax"] - b["xmin"])
            b_height = (b["ymax"] - b["ymin"])


            b_center_x /= w
            b_center_y /= h

            plate_size.append(b_width)
            plate_size.append(b_height)

            b_width /= w
            b_height /= h

            print_buffer.append(
                "{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
            break
            # plate_size.append(b["xmin"])
            # plate_size.append(b["ymin"])
            # b_center_x = (b["xmin"] + b["xmax"]) / 2 - b["xmin"]
            # b_center_y = (b["ymin"] + b["ymax"]) / 2 - b["ymin"]
            # b_width = (b["xmax"]-b["xmin"])
            # b_height = (b["ymax"]-b["ymin"])
            #
            #
            # #이미지를 Plate로 크롭했기때문에 Plate의 너비와 높이가 이미지의 너비와 높이이다.
            # b_center_x /= b_width
            # b_center_y /= b_height
            #
            # plate_size.append(b_width)
            # plate_size.append(b_height)
            #
            #
            # b_width /= b_width
            # b_height /= b_height
            #
            # print_buffer.append(
            #     "{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
            # break
    noPlate_src = src + "NoPlate/" #Plate가 없는 파일을 분리할 폴더
    xml_src = src + "labels/src/" #xml파일이 들어있는 폴더
    image_src = src + "images/src/" #이미지 파일이 들어있는 폴더
    txt_src = src + "labels/src2" #txt파일이 들어있는 폴더


    # plate_size가 담기지 않았다면 NoPlate폴더에 이미지랑 xml을 둘다 담는다
    try:
        plate_size[0]
    except IndexError:
        createFolder(noPlate_src)
        move(xml_src + info_dict["filename"].replace(".jpg", ".xml"),
             noPlate_src + info_dict["filename"].replace(".jpg", ".xml"))
        move(image_src + info_dict["filename"], noPlate_src + info_dict["filename"])
        return
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid Class.", b["class"], class_name_to_id_mapping.keys())
        #Plate객체가 아니라면
        if not class_id == 0:
            # print(info_dict["filename"])
            # print("xmin",b["xmin"])
            # print("xmax", b["xmax"])
            # print("platesize0", plate_size[0])
            #중앙값은 Plate의 왼쪽 위 점만큼 줄여준다.
            b_center_x = (b["xmin"] + b["xmax"]) / 2 - plate_size[0]
            b_center_y = (b["ymin"] + b["ymax"]) / 2 - plate_size[1]
            b_width = (b["xmax"] - b["xmin"])
            b_height = (b["ymax"] - b["ymin"])
            #Plate의 크기(=이미지크기)로 나눠서 비율을 구해준다.
            b_center_x /= plate_size[2]
            b_center_y /= plate_size[3]
            b_width /= plate_size[2]
            b_height /= plate_size[3]

            print_buffer.append(
                "{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
    #txt파일을 만드는 코드
    if ".jpg" in info_dict["filename"]:
        save_file_name = os.path.join(txt_src,info_dict["filename"].replace('jpg', 'txt'))
    else:
        save_file_name = os.path.join(txt_src, info_dict["filename"].replace('jpg', '.txt'))

    print("\n".join(print_buffer),file = open(save_file_name,"w"))

#폴더 만드는 함수
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

if __name__ == '__main__':

    #annotations = xml파일 리스트
    #listdir은 딕셔너리에 있는 파일이름들을 리스트로 반환해주는 함수
    a = 0
    xml_src = src + "labels/src"
    image_src = src + "images/src/"
    annotations = [os.path.join(xml_src, x) for x in os.listdir(xml_src) if x[-3:] == "xml"]

    # xml파일만 있고 jpg파일은 없는 경우 실패 폴더를 만들어서 그쪽으로 옮긴다
    for i in tqdm(annotations, desc="check files"):
        if not os.path.exists(image_src+os.path.basename(i.replace("xml", "jpg"))):
            createFolder(os.path.join(src, "실패"))
            move(i, os.path.join(src, "실패", os.path.basename(i)))
            annotations.remove(i)

    txt_src = src+"labels/src2"
    createFolder(txt_src)
    annotations.sort()
    #xml파일들을 하나씩 txt로 변환
    #tqdm은 실행중인 상태를 표시해주는 상태바가 나오는 함수
    for ann in tqdm(annotations):
        info_dict = extract_info_from_xml(ann)
        convert_to_yolov5(info_dict)
