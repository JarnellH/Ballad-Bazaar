import numpy as np
import moviepy as movie
from moviepy.editor import *
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout


clip1 = VideoFileClip("mrBeast.mp4")

clip2 = VideoFileClip("mrBeast.mp4")

#useful_clip1 = clip1.copy()
#useful_clip2 = clip2.copy()


#useful_clip1 = useful_clip1.fx(fadeout, 3)
#useful_clip2 = useful_clip2.fx(fadein, 3)

clip1 = clip1.fx(fadeout, 3)
clip2 = clip2.fx(fadein, 3)



clipArray = [clip1, clip2]


fullMovie = concatenate_videoclips(clipArray)

fullMovie.write_videofile("WORK.mp4")


#TODO: Process mp4 files and stitch them together cohesively
#keep in the mind the lengths of the files. Typically want them to be 11 secs each 
#after processing the first file you then stitch them together  **try to get the last frame of the first into the first frame of the second if possible**
#and finally produce a new mp4 file which contains the combined frames  // Take in MP4 file and store the bytes in an array 

class VideoStitch:

    #clips will be the same resolution and size so visual synchronization shouldn't be a problem
    def combine_clips(self , *args):
        #could possibly be hardcoded to 4 or 5
        clip_array = []

        for mp4_file in args:

            clip = VideoFileClip(mp4_file)
            clip_array.append(clip)
        
        fullMovie = concatenate_videoclips(clip_array)
        fullMovie.write_videofile("combined_clips.mp4")


    #If I cant get the video transition thing to work Ill have to make one from scratch 
    # look at the pixels from the video and choose a color to make the transition layer (fade effect)       
