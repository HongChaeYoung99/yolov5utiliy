#train, test, val 3개의 폴더로 나눠담는 코드
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

#폴더 생성 함수
#폴더가 이미 있으면 만들지않고 없으면 만든다.
def createFolder(directory):
    try:
        # 폴더가 없는가?
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
#데이터를 train과 test로 나눠서 담는 함수
def move_files_to_folder(list_of_files, destination_folder):
    for f in tqdm(list_of_files):
        try:
            # 복사할 위치 폴더와 파일이름을 합쳐 경로를 만든다.
            destination = os.path.join(destination_folder, os.path.basename(f))
            # 파일 복사
            shutil.copy(f, destination)
        except:
            print(f)
            assert False

if __name__== '__main__':
    #파일 들어있는 폴더
    src = "C:/Users/Minji/Documents/people_counting"
    image_src = src + "/images/src"
    txt_src = src + "/labels/src2"
    # 분리해서 담을 이미지 파일 리스트
    images = [os.path.join(image_src, x) for x in os.listdir(image_src) if x[-3:] == "jpg"]
    # 분리해서 담을 라벨 파일 리스트
    annotations = [os.path.join(txt_src, x) for x in os.listdir(txt_src) if x[-3:] == "txt"]

    images.sort()
    annotations.sort()
    # 2개의 파일리스트로 나눠 담아두기
    train_images, val_test_images = train_test_split(images, test_size=0.2, random_state=1)
    val_images, test_images = train_test_split(val_test_images, test_size=0.5, random_state=1)
    train_annotations, val_test_annotations = train_test_split(annotations, test_size=0.2, random_state=1)
    val_annotations, test_annotations = train_test_split(val_test_annotations, test_size=0.5, random_state=1)


    train_image_src = src + '/images/train'
    test_image_src = src + '/images/test'
    val_image_src = src + "/images/val"
    train_txt_src = src + '/labels/train'
    test_txt_src = src + '/labels/test'
    val_txt_src = src + '/labels/val'
    # 폴더 생성
    createFolder(train_image_src)
    createFolder(test_image_src)
    createFolder(val_image_src)
    createFolder(train_txt_src)
    createFolder(test_txt_src)
    createFolder(val_txt_src)
    # 각각 폴더로 나눠 복사하기
    move_files_to_folder(train_images, train_image_src)
    move_files_to_folder(test_images, test_image_src)
    move_files_to_folder(val_images, val_image_src)
    move_files_to_folder(train_annotations, train_txt_src)
    move_files_to_folder(test_annotations, test_txt_src)
    move_files_to_folder(val_annotations, val_txt_src)

    # 복사된 파일 리스트
    train_image_list = os.listdir(train_image_src)
    test_image_list = os.listdir(test_image_src)
    val_image_list = os.listdir(val_image_src)
    train_labels_list = os.listdir(train_txt_src)
    test_lables_list = os.listdir(test_txt_src)
    val_labels_list = os.listdir(val_txt_src)
    # 개수 확인
    print('이미지 개수: ', len(images))
    print('train 폴더로 이동할 예정인 이미지 개수: ', len(train_images))
    print('train 폴더 이미지 개수: ', len(train_image_list))
    print('test 폴더로 이동할 예정인 이미지 개수: ', len(test_images))
    print('test 폴더 이미지 개수: ', len(test_image_list))
    print('val 폴더로 이동할 예정인 이미지 개수: ', len(val_images))
    print('val 폴더 이미지 개수: ', len(val_image_list))
    print()
    print('라벨 개수: ', len(annotations))
    print('train 폴더로 이동할 예정인 라벨 개수: ', len(train_annotations))
    print('train 폴더 라벨 개수: ', len(train_labels_list))
    print('test 폴더로 이동할 예정인 라벨 개수: ', len(test_annotations))
    print('test 폴더 라벨 개수: ', len(test_lables_list))
    print('val 폴더로 이동할 예정인 라벨 개수: ', len(val_annotations))
    print('val 폴더 라벨 개수: ', len(val_labels_list))