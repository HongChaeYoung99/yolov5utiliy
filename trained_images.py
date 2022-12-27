#이미지 Plate로 crop하는 코드
from PIL import Image
import os
from tqdm import tqdm

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def isEmpty(dictionary):
   for element in dictionary:
     if element:
       return True
     return False


if __name__== '__main__':
    #크롭된 이미지 넣을 폴더 위치
    dir = "C:/Users/user/Documents/B/images/crop"
    createFolder(dir)
    sizes = []
    imgs_link = []

    #이미지 파일 있는 폴더 주소
    # image_dir = "C:/Users/user/PycharmProjects/practice/dataset/images/test/"
    image_dir = "C:/Users/user/Documents/B/images/src"
    #txt파일 있는 폴더 주소
    txt_dir = 'C:/Users/user/Documents/B/labels/src3'

    # glob는 파일들의 리스트를 뽑을 때 사용
    # for filename in glob.glob('C:/Users/user/PycharmProjects/practice/dataset/images/test/' + "*.jpg"):
    #     imgs_link.append(filename)
    annotations = [os.path.join(txt_dir, x) for x in os.listdir(txt_dir) if x[-3:] == "txt"]
    for txtname in tqdm(annotations):
        #detect.py 돌려서 나온 label폴더속 txt 파일 열기
        f = open(txtname, "r")
        line = f.readline() #좌표 읽기
        f.close()
        line = line.split(" ") #공백으로 split
        sizes.append(line)

        # plate가 인식된 이미지들의 이름을 만들어서 리스트에 담아둔다.
        image_name = os.path.join(image_dir, os.path.basename(txtname).replace("txt", "jpg"))
        imgs_link.append(image_name)

    for i in tqdm(range(0, len(sizes))):
        image1 = Image.open(imgs_link[i]) #이미지를 연다
        w, h = image1.size #이미지 사이즈를 넣는다

        #왼쪽 위 오른쪽 아래 좌표 구하는 식
        sizes[i][1] = float(sizes[i][1]) * w
        sizes[i][2] = float(sizes[i][2]) * h
        sizes[i][3] = float(float(sizes[i][3]) * w)
        sizes[i][4] = float(sizes[i][4]) * h

        left = float(sizes[i][1]) - float(sizes[i][3]) / 2.0
        top = float(sizes[i][2]) - float(sizes[i][4]) / 2.0
        right = float(sizes[i][1]) + float(sizes[i][3])/2.0
        bottom = float(sizes[i][2]) + float(sizes[i][4]) / 2.0
        area = (left, top, right, bottom)
        croppedImage = image1.crop(area) #이미지 크롭

        #만들어둔 폴더에 이미지 저장
        croppedImage.save(os.path.join(dir, os.path.basename(imgs_link[i])))