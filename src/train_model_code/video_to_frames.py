# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 19:01:01 2018

@author: Gerardo Cervantes
"""


import cv2

#video_path is a path to the video file
#output_image_dir is the path to the directory where it will save all the images
#img_extension is file extension it should output the image in, for example: .png, .jpg, .gif 
#num_frames_to_skip means it should skip this many frames until saving another frame, if 1 then will save every frame
def save_video_frames(video_path, output_image_dir, img_extension, num_frames_to_skip):
    vidcap = cv2.VideoCapture(video_path)
    
    if vidcap == None:
        print('Video could not be read')
    
    has_next_frame = True
    i = 0
    while has_next_frame:
        
        has_next_frame, image = vidcap.read()
        is_nth_frame = i % num_frames_to_skip == 0
        
        if is_nth_frame:
            frame_output_path = output_image_dir + '/' + str(i) + img_extension
            cv2.imwrite(frame_output_path, image) #Save image
        i += 1
  
    
if __name__ == "__main__":
    img_extension = '.png'
    output_image_dir = r'E:\MarioStarClassifier\viro14421'
    video_path = r'E:\MarioStarClassifier\videos\viro14421.mp4'
    num_frames_to_skip = 60
    save_video_frames(video_path, output_image_dir, img_extension, num_frames_to_skip)
      
      
