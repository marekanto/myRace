# debugged: angle, explosion
# dev
import pygame, sys, math, time
from pygame.locals import *
import numpy as np
import cv2 as cv
import imutils
import time
import os
from tkinter import *
from tkinter import messagebox

pygame.init()
# define the lower and upper boundaries of the "blue" object in the HSV color space
# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
blueLower = np.array([53, 187, 0])
blueUpper = np.array([180, 255, 255])
bg = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

ww = pygame.display.Info().current_w
wh = pygame.display.Info().current_h

pygame.mixer.init()
channel1 = pygame.mixer.Channel(0)  # argument must be int
channel2 = pygame.mixer.Channel(1)

music = pygame.mixer.Sound("Teenage_Crime.wav")
music.set_volume(0.0)
channel1.play(music)

pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)

window = pygame.display.set_mode((1600, 900))
# pygame.display.set_caption("MyRace")
window.fill(bg)
font = pygame.font.SysFont("comicsansms", 72)

text = font.render("Hello, World", True, (0, 128, 0))
clock = pygame.time.Clock()
done = False

# apply it to text on a label
label = myfont.render("Python and Pygame are Fun!", 1, blue)
# put the label object on the screen at point x=100, y=100
window.blit(label, (100, 100))
infoX = 1365
infoY = 600
font = pygame.font.Font('freesansbold.ttf', 18)
text1 = font.render('0..9 - Change Mutation', True, (255,255,255))
text2 = font.render('LMB - Select/Unselect', True, (255,255,255))

stretch = []
# stretch.append(pygame.image.load("bla_1.png"))
a = 1
a_counter = 6

while a == 1:
    try:
        exec("stretch.append(pygame.image.load('track_" + str(a_counter) + ".png'))")
    except:
        a = 0
    a_counter += 1

c_road = (100, 100, 100, 255)
c_fence = (255, 5, 5, 255)
c_finish = (255, 255, 5, 255)

counter = 0

startTime = time.time()

player_1 = pygame.Rect(100, 165, 20, 20)
image_1 = pygame.image.load("blue_small_rotated.png")

explosion = pygame.image.load("explosion.png")

pressed_1 = "false"
pressed_1_l = "false"
pressed_1_r = "false"
pressed_1_b = "false"  # Back

bew_counter_1 = 0
winkel_1 = 0
destroy_1 = 0
count_destr_1 = 0

#  player 1 variables


mvsp = 10
winkel_ch = 4  # change angle

clock = pygame.time.Clock()
fps = 50
time_ = 0

# pygame.mixer.music.play()

##########
x = 1
while x == 1:
    if count_destr_1 == 1:
        player_1.left = 100
        player_1.top = 165

    # Spieler 1
    if count_destr_1 == 0:
        # print(1)
        if pressed_1 == "true" and bew_counter_1 < mvsp:
            bew_counter_1 += 0.25
        if pressed_1_b == "true":
            bew_counter_1 -= 0.25

        if pressed_1_l == "true" and bew_counter_1 > 2:
            winkel_1 -= winkel_ch
        elif pressed_1_l == "true" and bew_counter_1 < -2:
            winkel_1 += winkel_ch

        if pressed_1_r == "true" and bew_counter_1 > 2:
            winkel_1 += winkel_ch
        elif pressed_1_r == "true" and bew_counter_1 < -2:
            winkel_1 -= winkel_ch

        if pressed_1 == "false" and bew_counter_1 > 0:
            bew_counter_1 -= 0.25
        if pressed_1_b == "false" and bew_counter_1 < 0:
            bew_counter_1 += 0.25

        b_1 = math.cos(
            math.radians(winkel_1)) * bew_counter_1  # Berechnet die Länge der am winkel_1 anliegenden Kathete.
        # fisch.top += b
        # print("b = " + str(b))
        a_1 = math.sin(math.radians(winkel_1)) * bew_counter_1
        player_1.left += round(b_1)
        player_1.top += round(a_1)

        image_1_neu = pygame.transform.rotate(image_1, winkel_1 * -1)

    else:
        count_destr_1 -= 1

    for event in pygame.event.get():

        if event.type == QUIT:
            # pygame.quit()
            x = 0
            # sys.exit()

        if event.type == KEYDOWN:
            if event.key == pygame.K_x:
                exec(open("./nnCarGame.py").read())
            if event.key == pygame.K_c:
                # Staring the camera
                video = cv.VideoCapture(0)

                # allow the camera or video file to warm up
                time.sleep(2.0)
                initial = True
                flag = False
                current_key_pressed = set()
                circle_radius = 30

                # Defining window boundaries for each logically divided region
                windowSize = 80
                windowSize2 = 100

                lr_counter = 0

                # keep looping
                while True:
                    keyPressed = False
                    keyPressed_lr = False

                    # grab the current frame
                    ret, frame = video.read()

                    # My video frame was flipped horizontally. If your video is not flipped by default you can ommit this
                    frame = cv.flip(frame, 1)
                    #     ret, frame = vid.read()
                    #     # flip=cv.flip(frame,1)

                    # resize the frame, blur it, and convert it to the HSV color space
                    frame = imutils.resize(frame, width=600)
                    frame = imutils.resize(frame, height=300)

                    # storing height and width in varibles
                    height = frame.shape[0]
                    width = frame.shape[1]

                    blurred = cv.GaussianBlur(frame, (11, 11), 0)
                    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

                    # crteate a mask for the blue color and perform opening and closing to remove any small
                    # blobs left in the mask
                    mask = cv.inRange(hsv, blueLower, blueUpper)
                    kernel = np.ones((5, 5), np.uint8)
                    # inspired by https://pythonprogramming.net/morphological-transformation-python-opencv-tutorial/
                    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
                    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

                    # find contours in the mask and initialize the current
                    # (x, y) center of the blue object
                    # divide the frame into seperate halves so that we can have one half control the turning/steering
                    # and other half control the forward and reverse.
                    up_mask = mask[0:height // 2, 0:width, ]
                    down_mask = mask[height // 2:height, width // 4:3 * width // 4, ]

                    # find the contours(blue object's boundary) in the left and right frame to find the center of the object
                    # syntax: (img,mode,method)
                    cnts_up = cv.findContours(up_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                    cnts_up = imutils.grab_contours(cnts_up)
                    center_up = None

                    cnts_down = cv.findContours(down_mask.copy(), cv.RETR_EXTERNAL,
                                                cv.CHAIN_APPROX_SIMPLE)
                    cnts_down = imutils.grab_contours(cnts_down)
                    center_down = None

                    # only proceed if at least one contour was found
                    if len(cnts_up) > 0:
                        # find the largest contour in the mask, then use
                        # it to compute the minimum enclosing circle and centroid
                        c = max(cnts_up, key=cv.contourArea)
                        # find circle of minimum area eclosing a 2D point set
                        ((x, y), radius) = cv.minEnclosingCircle(c)
                        # The function cv2.moments() gives a dictionary of all moment values calculated.
                        # Moments can be used to calculate COM,area,centroid,etc
                        M = cv.moments(c)
                        # find the center from the moments 0.000001 is added to the denominator so that divide by
                        # zero exception doesn't occur
                        center_up = (int(M["m10"] / (M["m00"] + 0.000001)), int(M["m01"] / (M["m00"] + 0.000001)))

                        # only proceed if the radius meets a minimum size
                        if radius > circle_radius:
                            # draw the circle and centroid on the frame,
                            cv.circle(frame, (int(x), int(y)), int(radius),
                                      (0, 255, 255), 2)
                            cv.circle(frame, center_up, 5, (0, 0, 255), -1)

                            # TOP LEFT is "A" key pressed and TOP RIGHT is for "D" key pressed
                            # the window size is kept 160 pixels in the center of the frame(80 pixels above the center and 80 below)
                            if center_up[0] < (width // 2 - windowSize // 2):
                                pressed_1_l = "true"
                                print('left turn')
                                # cv2.putText(frame,'LEFT',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                                # PressKey(A)
                                current_key_pressed.add("A")
                                keyPressed = True
                                keyPressed_lr = True
                            elif center_up[0] > (width // 2 + windowSize // 2):
                                pressed_1_r = "true"
                                # cv2.putText(frame,'RIGHT',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                                # PressKey(D)
                                print('right turn')
                                current_key_pressed.add("D")
                                keyPressed = True
                                keyPressed_lr = True

                    # only proceed if at least one contour was found
                    if len(cnts_down) > 0:
                        c2 = max(cnts_down, key=cv.contourArea)
                        ((x2, y2), radius2) = cv.minEnclosingCircle(c2)
                        M2 = cv.moments(c2)
                        center_down = (int(M2["m10"] / (M2["m00"] + 0.000001)), int(M2["m01"] / (M2["m00"] + 0.000001)))
                        center_down = (center_down[0] + width // 4, center_down[1] + height // 2)

                        # only proceed if the radius meets a minimum size
                        if radius2 > circle_radius:
                            # draw the circle and centroid on the frame,
                            cv.circle(frame, (int(x2) + width // 4, int(y2) + height // 2), int(radius2),
                                      (0, 255, 255), 2)
                            cv.circle(frame, center_down, 5, (0, 0, 255), -1)

                            # Upper half of bottom half is "W" key pressed and bottom part of bottom half is for "s" key pressed
                            if (height // 2) < center_down[1] < ((3 * height) // 4) and (width // 4) < center_down[
                                0] < ((3 * width) // 4):
                                pressed_1 = "true"
                                # cv2.putText(frame,'UP',(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                                # PressKey(W)
                                keyPressed = True
                                print('up')
                                current_key_pressed.add("W")
                                pressed_1 = "true"
                            elif center_down[1] > ((3 * height) // 4 + 20) and (width // 4) < center_down[0] < (
                                    (3 * width) // 4):
                                pressed_1_b = "true"
                                # cv2.putText(frame,'DOWN',(200,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                                # PressKey(S)
                                keyPressed = True
                                print('down turn')
                                current_key_pressed.add("S")
                        if not keyPressed_lr and (("A" in current_key_pressed) or ("D" in current_key_pressed)):
                            if "A" in current_key_pressed:
                                pressed_1_l = "false"
                                current_key_pressed.remove("A")
                            elif "D" in current_key_pressed:
                                pressed_1_r = "false"
                                current_key_pressed.remove("D")

                        key = cv.waitKey(1) & 0xFF

                        # if the 'q' key is pressed, stop the loop
                        if key == ord("q"):
                            break
                    if count_destr_1 == 0:
                        # print(1)
                        if pressed_1 == "true" and bew_counter_1 < mvsp:
                            bew_counter_1 += 0.25
                        if pressed_1_b == "true":
                            bew_counter_1 -= 0.25

                        if pressed_1_l == "true" and bew_counter_1 > 2:
                            winkel_1 -= winkel_ch
                        elif pressed_1_l == "true" and bew_counter_1 < -2:
                            winkel_1 += winkel_ch

                        if pressed_1_r == "true" and bew_counter_1 > 2:
                            winkel_1 += winkel_ch
                        elif pressed_1_r == "true" and bew_counter_1 < -2:
                            winkel_1 -= winkel_ch

                        if pressed_1 == "false" and bew_counter_1 > 0:
                            bew_counter_1 -= 0.25
                        if pressed_1_b == "false" and bew_counter_1 < 0:
                            bew_counter_1 += 0.25

                        b_1 = math.cos(
                            math.radians(
                                winkel_1)) * bew_counter_1  # Berechnet die Länge der am winkel_1 anliegenden Kathete.
                        # fisch.top += b
                        # print("b = " + str(b))
                        a_1 = math.sin(math.radians(winkel_1)) * bew_counter_1
                        player_1.left += round(b_1)
                        player_1.top += round(a_1)

                        image_1_neu = pygame.transform.rotate(image_1, winkel_1 * -1)

                    else:
                        count_destr_1 -= 1
                    window.fill((0, 0, 0))
                    window.blit(stretch[counter], (0, 0))

                    if count_destr_1 == 0:
                        try:
                            if not window.get_at((player_1.left + 10, player_1.top + 10)) == c_road:
                                #    print(window.get_at(((player_1.left + 10, player_1.top + 10))))
                                #    print("Crash")
                                if bew_counter_1 > 3:
                                    bew_counter_1 = 2
                                if bew_counter_1 < -3:
                                    bew_counter_1 = -2
                                    # print("Spieler 1\n")

                            if window.get_at((player_1.left + 10, player_1.top + 10)) == c_fence:
                                destroy_1 = 1

                            if window.get_at((player_1.left + 10, player_1.top + 10)) == c_finish:
                                destroy_1 = 1

                        except:
                            destroy_1 = 1

                        if destroy_1 == 0:
                            window.blit(image_1_neu, player_1)

                    else:
                        window.blit(explosion, player_1)

                    if destroy_1 == 1:
                        window.blit(explosion, player_1)
                        pygame.display.update()
                        # crash = pygame.mixer.Sound('crash.wav')
                        # crash.set_volume(1.0)
                        # channel2.play(crash)
                        destroy_1 = 0
                        winkel_1 = 0
                        # time.sleep(0.5)
                        count_destr_1 = 25
                        player_1.left = 100
                        player_1.top = 165
                        pressed_1 = "false"
                        pressed_1_l = "false"
                        pressed_1_r = "false"
                        pressed_1_b = "false"

                    pygame.display.update()

                    # time_ += 1
                    clock.tick(fps)

                    # show the frame to our screen
                    frame_copy = frame.copy()

                    # draw box for left (A)
                    frame_copy = cv.rectangle(frame_copy, (0, 0), (width // 2 - windowSize // 2, height // 2),
                                              (255, 255, 255), 1)
                    cv.putText(frame_copy, 'LEFT', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

                    # draw box for left (D)
                    frame_copy = cv.rectangle(frame_copy, (width // 2 + windowSize // 2, 0), (width - 2, height // 2),
                                              (255, 255, 255), 1)
                    cv.putText(frame_copy, 'RIGHT', (300, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

                    # draw box for left (W)
                    frame_copy = cv.rectangle(frame_copy, (width // 4, (height // 2) + 5),
                                              (3 * width // 4, 3 * height // 4), (255, 255, 255), 1)
                    cv.putText(frame_copy, 'UP', (width // 4, (height // 2) + 33), cv.FONT_HERSHEY_SIMPLEX, 1,
                               (255, 255, 255))

                    # draw box for left (S)
                    frame_copy = cv.rectangle(frame_copy, (width // 4, ((3 * height) // 4) + 5),
                                              (3 * width // 4, height), (255, 255, 255), 1)
                    cv.putText(frame_copy, 'DOWN', ((3 * width // 4) - 100, (height // 2) + 108),
                               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

                    # display final frame
                    cv.imshow("Frame", frame_copy)

                    # We need to release the pressed key if none of the key is pressed else the program will keep on sending
                    # the presskey command
                    # if not keyPressed and len(current_key_pressed) != 0:
                    #                         for key in current_key_pressed:
                    #                             current_key_pressed.remove(key)
                    #                         current_key_pressed = set()
                    #                     #to release keys for left/right with keys of up/down remain pressed



                video.release()
                # close all windows
                cv.destroyAllWindows()

            if event.key == K_ESCAPE:
                x = 0

            if event.key == K_RETURN:
                counter += 1
                player_1.left = 100
                player_1.top = 165
                winkel_1 = 0

                winkel_2 = 0

                if counter >= len(stretch):
                    counter = 0

            if event.key == K_UP:
                pressed_1 = "true"
            if event.key == K_LEFT:
                pressed_1_l = "true"
            if event.key == K_RIGHT:
                pressed_1_r = "true"
            if event.key == K_DOWN:
                pressed_1_b = "true"


        if event.type == KEYUP:
            if event.key == K_UP:
                pressed_1 = "false"
            if event.key == K_LEFT:
                pressed_1_l = "false"
            if event.key == K_RIGHT:
                pressed_1_r = "false"
            if event.key == K_DOWN:
                pressed_1_b = "false"

    window.fill((0, 0, 0))
    window.blit(stretch[counter], (0, 0))

    if count_destr_1 == 0:
        try:
            if not window.get_at((player_1.left + 10, player_1.top + 10)) == c_road:
                #    print(window.get_at(((player_1.left + 10, player_1.top + 10))))
                #    print("Crash")
                if bew_counter_1 > 3:
                    bew_counter_1 = 2
                if bew_counter_1 < -3:
                    bew_counter_1 = -2
                    # print("Spieler 1\n")

            if window.get_at((player_1.left + 10, player_1.top + 10)) == c_fence:
                destroy_1 = 1

            if window.get_at((player_1.left + 10, player_1.top + 10)) == c_finish:
                destroy_1 = 1

        except:
            destroy_1 = 1


        if destroy_1 == 0:
            window.blit(image_1_neu, player_1)

    else:
        window.blit(explosion, player_1)



    if destroy_1 == 1:
        window.blit(explosion, player_1)
        pygame.display.update()
        # crash = pygame.mixer.Sound('crash.wav')
        # crash.set_volume(1.0)
        # channel2.play(crash)
        destroy_1 = 0
        winkel_1 = 0
        # time.sleep(0.5)
        count_destr_1 = 25



    pygame.display.update()

    # time_ += 1
    clock.tick(fps)

str(time.time() - startTime)
pygame.quit()
#