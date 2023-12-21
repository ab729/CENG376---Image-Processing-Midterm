import cv2, os
import numpy as np
import moviepy.editor as mpy

background = cv2.imread('./Malibu.jpg')



ratio = 360/background.shape[0]
bg = cv2.resize(background, (int(background.shape[1] * ratio), 360))
bg = cv2.flip(bg, 1)
# bg = cv2.resize(background, (0,0), fx=0.4, fy=0.5)

final_form = []
for i in range(180):
    img_Path = f'./cat/cat_{i}.png'
    img = cv2.imread(img_Path)
    fliped_image = cv2.flip(img, 1)


    foreground = np.logical_or(img[:,:,1] < 180, img[:,:,0]>150)
    nonzero_x,nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = img[nonzero_x, nonzero_y,:]

    foreground_1 = np.logical_or(fliped_image[:,:,1] < 180, fliped_image[:,:,0]>150)
    nonzero_x1,nonzero_y1 = np.nonzero(foreground_1)
    nonzero_cat_values_flipped = fliped_image[nonzero_x1, nonzero_y1,:]
    
    
    new_frame = bg.copy()
    new_frame[nonzero_x, nonzero_y, :] = nonzero_cat_values
    # new_frame[nonzero_x1, nonzero_y1, :] = nonzero_cat_values_flipped

    fliped_frame = cv2.flip(new_frame, 1)
    fliped_frame[nonzero_x, nonzero_y, :] = nonzero_cat_values
    fliped_frame = cv2.cvtColor(fliped_frame, cv2.COLOR_RGB2BGR)

    final_form.append(fliped_frame)



    # img = cv2.cvtColor(img_Path, cv2.COLOR_RGB2HSV)
    # img = cv2.imshow('hsv', img)
clip = mpy.ImageSequenceClip(final_form, fps=25)
audio = mpy.AudioFileClip('./selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip = audio)
clip.write_videofile('part1.mp4', codec='libx264')