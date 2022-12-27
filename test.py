#crop한 이미지 좌표 맞게 추출됐는지 확인하는 코드
import os
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

        plotted_image.text((x0, y0+10),str(obj_cls) )

    plt.imshow(np.array(image))
    plt.show()
if __name__ == '__main__':
    class_name_to_id_mapping = {'Plate': 0, 'N_1': 1, 'N_2': 2, 'N_3': 3, 'N_4': 4, 'N_5': 5, 'N_6': 6, 'N_7': 7,
                                'N_8': 8,
                                'N_9': 9, 'S_노': 10, 'S_러': 11, 'S_마': 12, 'S_로': 13, 'S_소': 14, 'S_다': 15, 'S_나': 16,
                                'S_거': 17, 'S_두': 18, 'S_서': 19, 'S_오': 20, 'S_조': 21, 'S_더': 22, 'S_너': 23, 'S_모': 24,
                                'S_부': 25, 'S_수': 26, 'S_무': 27, 'S_우': 28, 'S_주': 29, 'S_가': 30, 'S_어': 31, 'S_고': 32
        , 'S_보': 33, 'S_구': 34, 'S_버': 35, 'S_라': 36, 'S_머': 37, 'S_도': 38, 'S_저': 39, 'S_루': 40, 'S_누': 41, 'N_0': 42}

    class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))
    annotaion_file = "C:/Users/user/Documents/test/2-00-거-3652.txt"
    # image1 = Image.open("C:/Users/user/Documents/test/2-00-거-3652.jpg")
    # croppedImage = image1.crop((520,845,701,936))
    # os.remove("C:/Users/user/Documents/test/2-00-거-3652.jpg")
    # croppedImage.save("C:/Users/user/Documents/test/2-00-거-3652.jpg")
    with open(annotaion_file, 'r' ) as file:
        #['0 0.502 0.764 0.194 0.060', ''] 이렇게 들어가있어서 마지막꺼 제거하기 위해 [:-1]
        annotation_list = file.read().split("\n")[:-1]
        annotation_list = [x.split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x ] for x in annotation_list]

        image_file = annotaion_file.replace("txt","jpg")
        assert os.path.exists(image_file)

        image = Image.open(image_file)

        plot_bounding_box(image, annotation_list)