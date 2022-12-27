import torch
from PIL import Image
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
import wandb

if __name__ == '__main__':

    model = torch.hub.load('ultralytics/yolov5', 'custom', path="C:/Users/user/PycharmProjects/practice/B_best.pt")
    plate_model = torch.hub.load('ultralytics/yolov5', 'custom', path="C:/Users/user/PycharmProjects/practice/P_best.pt")

    img_link = ["C:/Users/user/Documents/B/images/src/2-02-다-2053.jpg"]
    crop_img_link = ['C:/Users/user/Documents/B_train/images/val/2-02-다-2053.jpg']

    result1 = plate_model(img_link)
    result2 = model(crop_img_link)

    img = Image.open("C:/Users/user/Documents/B/images/src/2-02-다-2053.jpg")
    crop_img = Image.open("C:/Users/user/Documents/B_train/images/val/2-02-다-2053.jpg")

    f = open("a.txt", "w")
    f.write(str(result1.pandas().xyxy[0]))
    f.close()


    f = open("b.txt", "w")
    f.write(str(result2.pandas().xyxy[0]))
    f.close()

    f = open("a.txt", "r")
    line = f.readline()
    line = f.readline()
    plate = line.split(" ")
    while "" in plate:
        plate.remove("")

    f.close()


    info_list = []
    f = open("b.txt", "r")

    while True:
        line = f.readline()
        if not line: break
        line = line.replace("\n", "").split(" ")
        info_list.append(line)
    f.close()
    for list in info_list:
        while "" in list:
            list.remove("")

    for list in info_list:
        print(list)
    root = Element("annotation")
    folder = Element("folder")
    folder.text = "iamges"
    root.append(folder)

    filename = Element("filename")
    filename.text = os.path.basename(img_link[0])
    root.append(filename)

    path = Element("path")
    path.text = img_link[0]
    root.append(path)

    size = Element("size")
    root.append(size)

    sub_width = SubElement(size, "width")
    w, h = img.size
    sub_width.text = w
    sub_height = SubElement(size, "height")
    sub_height.text = h


    # results.show()
    # print(results.pandas().xyxy[0])

