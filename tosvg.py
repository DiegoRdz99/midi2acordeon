import numpy as np

class svg():
    def __init__(self,width=80,height=280,ac_type='F',title='acc'):
        self.width = width # width of image
        self.height = height # height of image
        self.keys = [['']*10,['']*11,['']*10] # keys (circles)
        self.reset_xml() # initial conditions (all white)
        self.keys_cl = [] # notes of keys when played closing
        self.keys_op = [] # notes of keys when played opening
        self.ac_type = ac_type # type of accordeon (either F, G, or E, acordón de Fa, Sol o Mi)
        self.title = title # title of exports
        for i in range(3):
            d = 275 - n[i]*25 # Distance from first key to top frame
            for j in range(11):
                try:
                    self.keys[i][j] = circle(cx=25*(i-1),cy=25*(j+1)+d/2-10,r=10) # create circles
                    self.keys_cl.append(key(pitch=note2num(cl[self.ac_type][i][j]),action='',coor=[i,j])) # define keys when closing (pitch and location)
                    self.keys_op.append(key(pitch=note2num(op[self.ac_type][i][j]),action='',coor=[i,j])) # define keys when opening
                except:
                    pass

    def reset_xml(self):
        self.xml = [f'<?xml version="1.0" encoding="UTF-8"?>\n<svg width="{self.width}" height="{self.height}" viewBox="-{self.width/2} 0 {self.width} {self.height}">\n<rect x="-{self.width/2}" width="100%" height="100%" fill="#000000" fill-opacity="0.6"/>'] # svg header
        for i in range(3): # reset initial conditions (all white)
            d = 275 - n[i]*25
            for j in range(11):
                try:
                    self.keys[i][j] = circle(cx=25*(i-1),cy=25*(j+1)+d/2-10,r=10)
                except:
                    pass

    def add_xml(self,string):
        self.xml.append(string)

    def note_action(self,i,j,act): # make a key active (played either opening or closing)
        d = 275 - n[i]*25
        self.keys[i][j] = circle(cx=25*(i-1),cy=25*(j+1)+d/2-10,fill=act_color[act])

    def export(self,num): # join the whole svg file and save it on the pycache folder (number ordered for video export with ffmpeg)
        for i in range(3):
            for j in range(11):
                try:
                    self.add_xml(self.keys[i][j]) # add each key (circle)
                except:
                    pass
        self.add_xml('</svg>') # svg footer
        self.export_string = '\n'.join(self.xml)
        self.reset_xml()
        open(f'./__pycache__/{self.title}-{num:04d}.svg','w').write(self.export_string)
        # return self.export

    def find_notes(self,note_nums): # find the key(s) which produce a certain pitch
        indx = []
        reps = set()
        for note in note_nums: # note pitch given as number
            for key in self.keys_op:
                if note == key.pitch:
                    reps.add(key.pitch)
                    indx.append((key.x,key.y))
        if len(reps) >= len(note_nums): # If all notes are found, export, if not, try with open
            return indx,'out'
        else:   
            indx = []
            reps = set()
            for note in note_nums:
                for key in self.keys_cl:
                    if note == key.pitch:
                        reps.add(key.pitch)
                        indx.append((key.x,key.y))
            if len(reps) >= len(note_nums):
                return indx,'in'
            else:
                return 'Not possible to play'


class key():
    def __init__(self,pitch,action='',coor=[0,0]):
        self.pitch = pitch
        self.action = action
        self.x = coor[0]
        self.y = coor[1]
        self.coor = np.array(coor)

# Constants:
n = [10,11,10]

act_color = {'':'ffffff','in':'3298e6','out':'e63232'}

op = {'F':[['D♭4','G3','B♭3','D4','E4','G4','B♭4','D5','E5','G5'],
['G♭4','A3','C4','E♭4','G4','A4','C5','E♭5','G5','A5','C6'],
['B4','D4','F4','A♭4','C5','D5','F5','A♭5','C6','D6']],

'G':[['E♭4','A3','C4','E4','G♭4','A4','C5','E5','G♭5','A5'],
['A♭4','B3','D4','F4','A4','B4','D5','F5','A5','B5','D6'],
['D♭5','E4','G4','B♭4','D5','E5','G5','B♭5','D6','E6']],

'E':[['C4','G♭3','A3','D♭4','E♭4','G♭4','A4','D♭5','E♭5','G♭5'],
['F4','A♭3','B3','D4','G♭4','A♭4','B4','D5','G♭5','A♭5','B5'],
['B♭4','D♭4','E4','G4','B4','D♭5','E5','G5','B5','D♭6']]
}

cl = {'F':[['B3','F3','A3','C4','F4','A4','C5','F5','A5','C6'],
['E4','F3','B♭3','D4','F4','B♭4','D5','F5','B♭5','D6','F6'],
['D♭5','B♭3','E♭4','G4','B♭4','E♭5','G5','B♭5','E♭6','G6']],

'G':[['D♭4','G3','B3','D4','G4','B4','D5','G5','B5','D6'],
['G♭4','G3','C4','E4','G4','C5','E5','G5','C6','E6','G6'],
['E♭','C4','F4','A4','C5','F5','A5','C6','F6','A6']],

'E':[['B♭3','E3','A♭3','B3','E4','A♭4','B4','E5','A♭5','B5'],
['E♭4','E3','A3','D♭4','E4','A4','D♭5','E5','A5','D♭6','E6'],
['C5','A3','D4','G♭4','A4','D5','G♭5','A5','D6','G♭6']]
}

notes = ['C','D♭','D','E♭','E','F','G♭','G','A♭','A','B♭','B']

C4 = 60

def note2num(note):
    return notes.index(note[:-1])+(int(note[-1])-4)*12+C4
    
def labeled_circle(cx=0,cy=0,r=1,fill='ffffff',stroke='000000',label='',size='8',text_color='000000'):
    circ = circle(cx,cy,r,fill,stroke)
    text = f'<text x="{cx}" y="{cy}" font-size="{size}" fill="#{text_color}" dy="0.3em" text-anchor="middle">{label}</text>'
    return circ+'\n'+text

def circle(cx=0,cy=0,r=10,fill='ffffff',stroke='000000'):
        if stroke!=None:
            return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#{fill}" stroke = "#{stroke}"/>'
        else:
            return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#{fill}" />'
        
def dist(keys:list):
    ks = [k.coor for k in keys]
    return sum(sum(ks**2))                

if __name__ == "__main__":
    test = svg()
    test.export(0)
    # print(test.find_notes([75,80]))