import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

def extract_info_from_xml(xml_file):
    #파일 열기
    f=open(xml_file,'r', encoding="UTF-8" )
    xml_text = f.read()
    #xml파일 읽을 준비
    root=ET.fromstring(xml_text)
    f.close()
    # root = ET.parse(xml_file).getroot()

    info_dict = {}
    info_dict['bboxes'] = [] #object들 넣을 곳

    for elem in root:
        if elem.tag == "object":
            for subelem in elem:
                if subelem.tag == "name":
                    info_dict["class"] = subelem.text

    return info_dict
if __name__ == '__main__':
    src = 'C:/Users/user/Documents/1차_4000장_11종/labels/src'
    annotations = [os.path.join(src, x) for x in os.listdir(src) if x[-3:] == "xml"]
    object = {"sedan" : 0, "SUV/RV" : 0, "small_bus" : 0, "large_bus" : 0, "small_truck" : 0, "large_truck" : 0,
              "Car_ETC" : 0, "person" : 0, "PM" : 0, "motorcycle" : 0, "bicycle" : 0}
    object_count = [0]
    for ann in tqdm(annotations):
        info_dict = extract_info_from_xml(ann)
        if info_dict["class"] == "sedan":
            object["sedan"] += 1
        elif info_dict["class"] == "SUV/RV":
            object["SUV/RV"] += 1
        elif info_dict["class"] == "small_bus":
            object["small_bus"] += 1
        elif info_dict["class"] == "large_bus":
            object["large_bus"] += 1
        elif info_dict["class"] == "small_truck":
            object["small_truck"] += 1
        elif info_dict["class"] == "large_truck":
            object["large_truck"] += 1
        elif info_dict["class"] == "Car_ETC":
            object["Car_ETC"] += 1
        elif info_dict["class"] == "person":
            object["person"] += 1
        elif info_dict["class"] == "PM":
            object["PM"] += 1
        elif info_dict["class"] == "motorcycle":
            object["motorcycle"] += 1
        elif info_dict["class"] == "bicycle":
            object["bicycle"] += 1
    for o in object:
        print(o, " : ", object[o])
