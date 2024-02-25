# 手势识别
import cv2
import mediapipe as mp
import time
import math
#import pyttsx3
# 求解二维向量的角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_

# 获取对应手相关向量的二维角度,根据角度确定手势
def hand_angle(hand_):
    angle_list = []
    # 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    # 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # 无名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list

# 二维约束的方法定义手势
def h_gesture(angle_list):
    thr_angle = 140.  # 手指闭合则大于这个值（大拇指除外）
    thr_angle_s = 20.  # 手指张开则小于这个值(大拇指除外）
    thr_angle_thumb = 80.  # 大拇指闭合则大于这个值
    thr_angle_thumb_s = 30.  # 大拇指张开则小于这个值

    gesture_str = "未识别出"
    if 65535. not in angle_list:
        # if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
        #         angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
        #     gesture_str = "0"
        if (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "one"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "2"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle):
            gesture_str = "3"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "4"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "5"
        elif (angle_list[0] < thr_angle_thumb_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "6"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "7"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "8"
        elif (angle_list[0] < thr_angle_thumb) and  (angle_list[0] > thr_angle_thumb_s) and (angle_list[1] > thr_angle_s) and (angle_list[1] < thr_angle ) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "9"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "-"
        elif (angle_list[0] < thr_angle_thumb_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "+"
        elif (angle_list[0] < thr_angle_thumb) and (angle_list[0] > thr_angle_thumb_s)and (angle_list[1] < thr_angle) and (angle_list[1] > thr_angle_s)and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "ok"
        elif (angle_list[0] < thr_angle_thumb_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "*"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "/"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "p"
    return gesture_str

#去掉隔离符
def new_ls(ls):
    l = []
    for i in ls:
        if i != 'p':
            l.append(i)
    return l

#分成数据集和符号集
def separate(ls):
    bit = 0
    res = 0
    digit_ls = []
    sign_ls = []
    for i in range(0, len(ls)):
        if ls[i].isdigit():
            bit += 1
        else:
            num = 0
            for j in range(0, bit):
                num += int(ls[i - j - 1]) * (10 ** j)
            digit_ls.append(num)
            bit = 0
            sign_ls.append(ls[i])
    return digit_ls,sign_ls
    # print(digit_ls,sign_ls)


#计算最终结果
def calculate(numbers,operators):
    # 定义运算符的优先级
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    # 定义栈用于存储数字和操作符
    number_stack = [numbers[0]]
    operator_stack = []
    def apply_operation():
        operator = operator_stack.pop()
        num2 = number_stack.pop()
        num1 = number_stack.pop()

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = num1 / num2

        number_stack.append(result)

    for i in range(1, len(numbers)):
        operator = operators[i - 1]
        number = numbers[i]

        if operator == '=':
            break

        # 处理运算符优先级
        while operator_stack and precedence[operator_stack[-1]] >= precedence[operator]:
            apply_operation()

        operator_stack.append(operator)
        number_stack.append(number)

    # 执行剩余的操作
    while operator_stack:
        apply_operation()

    result = number_stack[0]
    return result
    # print("计算结果:", result)


#def speak(text):
#    engine = pyttsx3.init()
#    engine.setProperty('rate',250)

 #   engine.say(text)
  #  engine.runAndWait()


def detect():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)
    cap = cv2.VideoCapture(0)
    while True:
        time.sleep(0.1)
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        #判断手势
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_local = []
                #计算每一个点的坐标
                for i in range(21):
                    x = hand_landmarks.landmark[i].x * frame.shape[1]
                    y = hand_landmarks.landmark[i].y * frame.shape[0]
                    hand_local.append((x, y))
                #通过计算得到的坐标判断手势
                if hand_local:
                    angle_list = hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)
                    #print(angle_list)
                    print(f'{gesture_str},{type(gesture_str)}')
                    #speak(gesture_str)
                    if gesture_str != '=':
                        # time.sleep(1)
                        if gesture_str == "Unknown":
                            break
                        elif gesture_str != yunsuan[-1]:
                            yunsuan.append(gesture_str)
                    if gesture_str == "=":
                        yunsuan.append(gesture_str)
                        new_l = new_ls(yunsuan)
                        number,operator=separate(new_l)
                        res = calculate(number,operator)


                        #print("运算结果：",res)

                       # print(res[0])


                        return 0
                    cv2.putText(frame, gesture_str, (50, 100), 0, 1.3, (0, 0, 255), 2)

        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    yunsuan = ['p']
    detect()

