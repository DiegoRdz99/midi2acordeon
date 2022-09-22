from acc_notes import *
import os
import subprocess

midis = [fil[:-4] for fil in os.listdir(os.getcwd()+'/midis') if fil[-4:]=='.mid']
print(midis)
print(len(midis))
for midi in midis:
    img_seq(f'./midis/{midi}.mid',midi)
    subprocess.Popen(['ffmpeg','-i',f'./pre_videos/pre-{midi}.mp4','-i',f'./pre_videos/{midi}.mp3',f'./videos/{midi}.mp4'])