import cv2, os
import numpy as np
import moviepy.editor as mpy

background = cv2.imread('./Malibu.jpg')
bg_width = background.shape[1]
bg_height = background.shape[0]
ratio = 360 / bg_height

background = cv2.resize(background, (int(bg_width * ratio), 360))

cv2.imshow('gt' ,background)

folder = './cat'
images = []
fliped_images = []
for i in range(180):
    img = cv2.imread(f'./cat/cat_{i}.png')
    img_flip = cv2.flip(img, 1)
    img_flip = cv2.imread(img_flip)

    foreground = np.logical_or(img[:,:,1] < 180, img[:,:,0]>150)
    nonzero_x, nonzero_y = np.nonzero(foreground)
    nonzero_cat_values = img[nonzero_x, nonzero_y, :]

    new_frame = background.copy()
    new_frame [nonzero_x, nonzero_y, :] = nonzero_cat_values
    # new_frame = new_frame[:,:,[2,1,0]],

    images.append(new_frame)


# new_frame = background.copy()
# new_frame [nonzero_x, nonzero_y, :] = nonzero_cat_values
# new_frame = cv2.cvtColor(new_frame[:,:,[2,1,0]], cv2.COLOR_RGB2BGR)



clip = mpy.ImageSequenceClip(images, fps=25)
audio = mpy.AudioFileClip('./selfcontrol_part.wav').set_duration(clip.duration)
clip = clip.set_audio(audioclip = audio)
clip.write_videofile('demo.mp4', codec='libx264')