#클래스 종류 추출할 때 쓴 코드
import os

#간단한 코드로 클래스의 종류를 출력한다.
if __name__ == '__main__':
    list = os.listdir("C:/Users/user/Documents/B/labels/src")
    s = set()
    for name in list:
        name = name.split("-")
        s.add("S_"+name[2])

    print(s)