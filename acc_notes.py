from tosvg import *
from midi2np import *
import cairosvg
from math import ceil
import ffmpeg

def img_seq(midi_file,title='video',fps=30):
    lst = read_midi(midi_file)
    acc = svg()
    time = [l.time for l in lst]
    fn = ceil(time[-1])*fps
    frames = [0]*fn
    j = 0
    for i in range(fn):
        frames[i]=j
        if i/30 > time[j+1]:
            j += 1
            try:
                time[j+1]
            except:
                j -= 1
    for i in range(fn):
        if lst[frames[i]].play == 1:
            try:
                inpt,action = acc.find_notes(lst[frames[i]].note_num)
            except Exception as e: print('The piece cannot be performed on the chosen Accordeon')
            for ins in inpt:
                acc.note_action(ins[0],ins[1],act=action)
        acc.export(i)
        cairosvg.svg2png(url=f'./__pycache__/acc-{i:04d}.svg',write_to=f'./__pycache__/acc-{i:04d}.png',output_width=800,output_height=2000)
    ffmpeg.input('./__pycache__/acc*.png',pattern_type='glob', framerate=fps).output(f'./pre_videos/pre-{title}.mp4').run()
    

    

# xml = acc.export()

# open('acc.svg','w').write(xml)

# cairosvg.svg2png(url='acc.svg',write_to=r'./__pycache__/acc.png',output_width=800,output_height=2000)

notes = ['C','D♭','D','E♭','E','F','G♭','G','A♭','A','B♭','B']
C4 = 60

def note2num(note):
    return notes.index(note[:-1])+(int(note[-1])-4)*12+C4

def num2note(num):
    return notes[(num-C4)%12]+str((num-C4)//12+4)

# img_seq('santo.mid','santo')
