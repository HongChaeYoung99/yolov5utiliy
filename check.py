#Plate로 자르지 않은 사진 좌표 맞게 추출했는지 확인하는 코드
import torch
# from IPython.display import Image  # for displaying images
import os
import random
import shutil
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt


def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size

    plotted_image = ImageDraw.Draw(image)

    #[[0.    0.605 0.665 0.191 0.062]] 이 모양으로 됨
    transformed_annotations = np.copy(annotations)

    transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
    transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h

    transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
    transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
    transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
    transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]

    print(transformed_annotations)
    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        print(ann)
        #왼쪽위 모서리, 오른쪽아래 모서리
        plotted_image.rectangle(((x0, y0), (x1, y1)))

        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])

    plt.imshow(np.array(image))
    plt.show()


if __name__ == '__main__':
    annotations = [os.path.join('dataset/labels/src2', x) for x in os.listdir('dataset/labels/src2') if x[-3:] == "txt"]
    class_name_to_id_mapping = {'Plate': 0}
    class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))
    annotaion_file = random.choice(annotations)
    with open(annotaion_file, 'r') as file:
        #['0 0.502 0.764 0.194 0.060', ''] 이렇게 들어가있어서 마지막꺼 제거하기 위해 [:-1]
        annotation_list = file.read().split("\n")[:-1]
        annotation_list = [x.split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x ] for x in annotation_list]

        image_file = annotaion_file.replace("labels/src2","images/src").replace("txt","jpg")
        assert os.path.exists(image_file)

        image = Image.open(image_file)

        plot_bounding_box(image, annotation_list)