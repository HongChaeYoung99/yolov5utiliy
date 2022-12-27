import numpy as np
import torch
import os
import cv2
# from IoU import intersection_over_union


class_id_to_name_mapping = {0: "sedan", 1: "SUV/RV", 2: "small_bus", 3: "large_bus", 4: "small_truck"
                            , 5: "large_truck", 6: "Car_ETC", 7: "person", 8: "PM", 9: "motorcycle", 10: "bicycle"}


if __name__ == '__main__':
    model = torch.hub.load('ultralytics/yolov5', 'custom', path="C:/Users/user/PycharmProjects/practice/smart_best.pt")
    src = "Z:/06. Deep Learning 데이터셋/Dataset/스마트교차로/02. 학습데이터/1차_4000장_11종/images/test"
    img_links = [os.path.join(src, x) for x in os.listdir(src) if x[-3:] == "jpg"]

    for img in img_links:
        # fromfile() : 텍스트나 이진 파일 데이터에서 배열을 생성한다.
        cv_img = np.fromfile(img, np.uint8)
        # 1D-array인 encoded_img를 3D-array로 만들어준다.
        # cv2.imread() 함수에 두 번째 파라미터로 cv2.IMREAD_COLOR를 넣어주면 BGR 방식으로 이미지를 읽습니다. cv2.IMREAD_UNCHANGED인 경우 이미지가 알파 채널을 가지고 있는 경우 BGRA 방식으로 읽습니다.
        cv_img = cv2.imdecode(cv_img, cv2.IMREAD_COLOR)
        # BGR 색상 이미지를 RGB 색상 이미지로 변환
        cv_RGB_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        h, w, c = cv_img.shape

        result = model(cv_RGB_img, size=256)
        df_result = result.pandas().xyxy[0]

        list_label = [] #클래스번호
        list_box = [] #좌표값
        list_score = [] #confidence값
        list_cname = [] #클래스이름

        for idx, elem in df_result.iterrows():
            f_xmin = elem["xmin"]
            f_ymin = elem["ymin"]
            f_xmax = elem["xmax"]
            f_ymax = elem["ymax"]

            f_Pred = elem["confidence"]
            nLabel = elem["class"] #class넘버
            clsName = class_id_to_name_mapping[nLabel]

            xmin = int(f_xmin)
            ymin = int(f_ymin)
            xmax = int(f_xmax)
            ymax = int(f_ymax)

            list_label.append(nLabel)  # class
            list_box.append([xmin, ymin, xmax, ymax])
            list_score.append(f_Pred)  # confidence
            list_cname.append(clsName)  # class이름

        conf_thr = 0.5
        iou_thr = 0.2

        rst_nms_label = []
        rst_nms_box = []
        rst_nms_score = []
        rst_nms_cname = []

        list_rect_box = []

        for elem_box in list_box:
            xmin = elem_box[0]
            ymin = elem_box[1]
            xmax = elem_box[2]
            ymax = elem_box[3]

            list_rect_box.append([xmin, ymin, xmax - xmin, ymax - ymin]) #{xmin, ymin, 너비, 높이}
            # 노이즈 제거, 같은 물체에 대한 박스가 많은 것을 제거
        list_nms_idx = cv2.dnn.NMSBoxes(list_rect_box, list_score, conf_thr, iou_thr)

        if len(list_nms_idx) > 0:
            for idx in list_nms_idx.flatten():
                rst_nms_label.append(list_label[idx])
                rst_nms_box.append(list_box[idx]) #[xmin, ymin, xmax, ymax]
                rst_nms_score.append(list_score)
                rst_nms_cname.append(list_cname[idx])











# def nms(bboxes, iou_threshold, threshold, box_format='corners'):
#     assert type(bboxes) == list
#
#     bboxes = [box for box in bboxes if box[1] > threshold]
#
#     bboxes = sorted(bboxes, key=lambda x : x[1], reverse=True)
#     bboxes_after_nmn = []
#
#     while bboxes:
#         #제일 iou값이 큰걸 넣는다
#         chosen_box = bboxes.pop(0)
#         #클래스가 같지 않으면 다시 넣는다.
#         bboxes = [box for box in bboxes if box[0] != chosen_box[0]
#                   or intersection_over_union(torch.tensor(chosen_box[2:]),
#                                              torch.tensor(box[2:]),
#                                              box_format=box_format) < iou_threshold]
#
#         bboxes_after_nmn.append(chosen_box)
#
#         return bboxes_after_nmn
