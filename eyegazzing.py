import cv2
import numpy as np
import dlib
from math import hypot
import pyglet
import time



sound = pyglet.media.load('audio/press.wav', streaming=False)
left = pyglet.media.load('audio/left.wav', streaming=False)
right = pyglet.media.load('audio/right.wav', streaming=False)


cap = cv2.VideoCapture(0)
board = np.zeros((500, 500), np.uint8)
board[:] = 255

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

keyboard = np.zeros((600, 752, 3), np.uint8)

keys_set_1 = {0: "Q", 1:"W", 2: "E", 3:"R", 4: "T", 5: "A", 6:"S", 7: "D", 8:"F", 9: "G", 10: "Z", 11: "X", 12: "C", 13: "V", 14: "<"}
keys_set_2 = {0: "Y", 1:"U", 2: "I", 3:"O", 4: "P", 5: "H", 6:"J", 7: "K", 8:"L", 9: "_", 10: "V", 11: "B", 12: "N", 13: "M", 14: "<"}

def buttons(letter_index, text, letter_light):
    if letter_index == 0:
        x =0
        y = 0
    elif letter_index == 1:
        x = 150
        y = 0
    elif letter_index == 2:
        x = 300
        y = 0
    elif letter_index == 3:
        x = 450
        y = 0
    elif letter_index == 4:
        x = 600
        y = 0
    elif letter_index == 5:
        x = 0
        y = 150
    elif letter_index == 6:
        x = 150
        y = 150
    elif letter_index == 7:
        x = 300
        y = 150
    elif letter_index == 8:
        x = 450
        y = 150
    elif letter_index == 9:
        x = 600
        y = 150
    elif letter_index == 10:
        x = 0
        y = 300
    elif letter_index == 11:
        x = 150
        y = 300
    elif letter_index == 12:
        x = 300
        y = 300
    elif letter_index == 13:
        x = 450
        y = 300
    elif letter_index == 14:
        x = 600
        y = 300
    
    
    width = 150
    height = 150
    font_th = 3
    border_color = (153,158, 9)
    if letter_light is True:
        cv2.rectangle(keyboard, (x + font_th, y + font_th), (x + width-font_th, y + height-font_th), border_color, -1)
    else:
        cv2.rectangle(keyboard, (x + font_th, y + font_th), (x + width-font_th, y + height-font_th), border_color, font_th)
     
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10 
    th = 3
    letter_color = (121, 110, 9)
    text_size = cv2.getTextSize(text, font, font_scale, th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font, font_scale,letter_color, th)

for i in range(15): 
    if i == 5:
        light = True
    else:
        light = False
        
    buttons(i, keys_set_1[i], light)

#//////////////////////////////////////////////////////////////////////////////////////////////

def midpoint(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


#////////////////////////////////////////////////////////////////////////////////////////////
def get_blinking_ratio(eye_points, facial_landmarks):
    
        left_point = (landmarks.part(eye_points[0]).x, landmarks.part(eye_points[0]).y)
    
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[1]))
        
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        
        #hor_line = cv2.line(frame, left_point, right_point, (0, 0 ,255), 2)
        
        #ver_line = cv2.line(frame, center_top, center_bottom, (0, 0 ,255), 2)
        
        hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        
        ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        
        ratio = hor_line_length/ver_line_length 
    
        
        return ratio
        
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
   

def get_gaze_ratio(eye_points, facial_landmarks):
    
        
        left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                  (facial_landmarks.part(eye_points[0]).x,   facial_landmarks.part(eye_points[0]).y),
                                  (facial_landmarks.part(eye_points[0]).x,   facial_landmarks.part(eye_points[0]).y),
                                  (facial_landmarks.part(eye_points[0]).x,   facial_landmarks.part(eye_points[0]).y),
                                  (facial_landmarks.part(eye_points[1]).x,   facial_landmarks.part(eye_points[1]).y),
                                  (facial_landmarks.part(eye_points[2]).x,   facial_landmarks.part(eye_points[2]).y)], np.int32)
        cv2.polylines(frame, [left_eye_region], True, (0, 255, 0), 2)
       
        height, width, _ = frame.shape
        
        mask = np.zeros((height, width), np.uint8)
        
      
        
        cv2.polylines(mask, [left_eye_region], True, 255 , 2)
        cv2.fillPoly(mask, [left_eye_region], 255)
        
        eye = cv2.bitwise_and(gray_scale, gray_scale, mask=mask)
        
        min_x = np.min(left_eye_region[:,0])
        
        max_x = np.max(left_eye_region[:,0])
        
        min_y = np.min(left_eye_region[:,1])
        
        max_y = np.max(left_eye_region[:,1])
        
        gray_eye = eye[min_y: max_y, min_x: max_x]
        
       
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
        
        height, width = threshold_eye.shape
        
        left_side_threshold = threshold_eye[0: height, 0: int(width/2)]
        left_side_white = cv2.countNonZero(left_side_threshold)
        
        right_side_threshold = threshold_eye[0: height, int(width/2): width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        
        
        if left_side_white == 0:
            gaze_ratio = 1
        elif right_side_white == 0:
            gaze_ratio = 3
        else:
            gaze_ratio = left_side_white / right_side_white
        
        return gaze_ratio
      
    

#//////////////////////////////////////////////////////////////////////////////////////

font = cv2.FONT_HERSHEY_PLAIN

frames = 0
letter_index = 0
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
#select_keyboard_menu = True
#keyboard_selection_frames = 0

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    keyboard[:] = (0, 0, 0)
    frames += 1
    new_frame = np.zeros((500, 500, 3), np.uint8)
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #draw a white space bar
    #frame [rows - 50: rows, 0: cols] = (255, 255, 255)
    
    #if select_keyboard_menu is True:
        #draw menu()
    #if keyboard_selected = "left":
     #  keys_set  = keys_set_1 
    #lse:
     #  keys_set = keys_set_2
    
    active_letter = keys_set_1[letter_index]
    
    faces = detector(gray_scale)
    
    for face in faces:
        
        landmarks = predictor(gray_scale,face)
       
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        
        blinking_ratio = (right_eye_ratio + left_eye_ratio) / 2
        
        if blinking_ratio > 3:
            
            cv2.putText(frame, "Blinking", (50, 150), font, 3, (0, 0, 255), 3)
            blinking_frames += 1
            frames -= 1
            
            if blinking_frames == 5:
                text += active_letter
                sound.play()
                time.sleep(1)
        else:
            blinking_frames = 0
            
            
        
        #gaze detection ratio
        
        gaze_ratio_left_eye = get_gaze_ratio(([36, 37, 38, 39, 40, 41]), landmarks)
        gaze_ratio_right_eye = get_gaze_ratio(([42, 43, 44, 345, 46, 47]), landmarks)
        gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye)/2
        
        if gaze_ratio <= 1:
            cv2.putText(frame, "Right", (50, 100), font, 2, (0, 255, 0), 2)
            #new_frame[:] = (0, 0, 255)
            keyboard_selected = "right"
            if keyboard_selected != last_keyboard_selected:
                #right.play()
                #time.sleep(1)
                last_keyboard_selected = keyboard_selected
        else:
            #new_frame[:] = (0, 255, 0)
            cv2.putText(frame,"Left", (50, 100), font, 2, (0, 255, 0), 2)
            keyboard_selected = "left"
            #left.play()
            #time.sleep(1)
            last_keyboard_selected = keyboard_selected
     
        if frames == 10:
            letter_index += 1
            frames = 0
        if letter_index == 15:
            letter_index = 0
    for i in range(15): 
            if i == letter_index:
                light = True
            else:
                light = False
            
            buttons(i, keys_set_1[i], light)       
      
    cv2.putText(board, text, (10, 100), font,3, 4, 0, 3)
    cv2.imshow("Default Wiondow", frame)
    #cv2.imshow("New Frame", new_frame)
    cv2.imshow("Virtual Keyboard", keyboard)
    cv2.imshow("White Board", board)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()