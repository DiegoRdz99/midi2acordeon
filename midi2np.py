import mido
from tosvg import *

class event():
    def __init__(self,note_num,play,time):
        self.note_num = [note_num]
        self.play = 1 if play > 0 else 0
        self.time = time

def read_midi(midi_file):
    mid = mido.MidiFile(midi_file)
    for x in range(len(mid.tracks)):
        # print(mid.tracks[x][0].name)
        if ('Akkordeon' in mid.tracks[x][0].name) or ('Accordion' in mid.tracks[x][0].name):
            T = x
        else:
            print('No accordion found')
    tempo = mid.tracks[T][3].tempo
    lst = [message for message in mid.tracks[T] if message.type == 'note_on' and message.channel==T]
    lst = [event(msg.note,msg.velocity,msg.time) for msg in lst]
    lst[0].time = tiks2sec(lst[0].time,tempo)
    i = 1
    while i<len(lst):
        if lst[i].time == 0:
            lst[i-1].note_num.append(lst[i].note_num[0])
            lst.pop(i)
        else:
            lst[i].time = lst[i-1].time+tiks2sec(lst[i].time,tempo)
            i += 1
    return lst

def tiks2sec(tiks,tempo):
    return tempo*tiks/(480*1e6)

if __name__ == '__main__':
    ls = read_midi('./midis/soy_yo_quien_llega.mid')
    print([l.note_num for l in ls])
    print([l.time for l in ls])