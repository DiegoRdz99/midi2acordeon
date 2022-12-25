from acc_notes import *
import os
import subprocess

midis = [fil[:-4] for fil in os.listdir(os.getcwd()+'/midis') if fil[-4:]=='.mid']
midis = ['porque_te_amo_Bb']
# print(midis)
for midi in midis:
    img_seq(midi_file=f'./midis/{midi}.mid',title=midi,ac_type='G')
    subprocess.Popen(['rm','-r','./__pycache__/*'])
    subprocess.Popen(['ffmpeg','-i',f'./pre_videos/pre-{midi}.mp4','-i',f'./pre_videos/{midi}.mp3',f'./videos/{midi}.mp4'])