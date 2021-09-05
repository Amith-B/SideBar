import tkinter as tk
import os,sys
import time
from PIL import Image,ImageTk
import threading
from tkinter.ttk import Progressbar, Style, Scale
from tkcolorpicker import askcolor
from tkinter import filedialog
import psutil as ps
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import tkinter.ttk as ttk
from mutagen import File
import mutagen
from mutagen import mp3
import random
import pygame
import io


right=True
app=None
alpha=.9
bgr='#2C3952'
t=None
run=True
dw=307
dh=824
shuffle=False
song='Select Song'+' '*37
prsntname=song[:42]
s=None
mute=False
dire=None
loc=None
musiclist=None
songnum=None
playing=False
d=dict()
c=0
v=1.0
tv=None
thread=None
hr=0
minit=0
sec=0
totsec=0
totmin=0
tothr=0
pt=0000
totv=None
songinfo=None
totlength=None
timeslider=None
pre=0
songlabel=None
playv=None
i=0
volinfo=None
prevol=1.0
shuffle=False
prelist=list()
live=True
dircontent=None
prevol=1.0
'''----------------------------------------netspeed below--------------------------------'''
speedUp=None
speedDown=None
interface=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)][0]
interface_list_at_startup=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
xpos,ypos=0,0
cntnt=''
oldcnt=''

if(len(interface)==0):
    os._exit(0)


if(os.path.exists('C:\\ProgramData\\SideBar\\netinterfacedata.log')):
    with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','r') as f:
       line=str(f.readline()).strip()
       interfacelist=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
       if(line in interfacelist):
           if(ps.net_if_stats()[interface].isup):
               interface=line
           else:
               interface=interfacelist[0]
       else:
           interface=interfacelist[0]

'''----------------------------------------netspeed above------------------------------------'''


try:
    if(os.path.exists('C:\\ProgramData\\SideBar\\sidebardata.log')):
        with open('C:\\ProgramData\\SideBar\\sidebardata.log','r') as f:
            bgr=str(f.readline()).strip()
    else:
        if(os.path.exists('C:\\ProgramData\\SideBar')):
            with open('C:\\ProgramData\\SideBar\\sidebardata.log','w+') as f:
                f.write(bgr)
        else:
            os.mkdir('C:\\ProgramData\\SideBar')
            with open('C:\\ProgramData\\SideBar\\sidebardata.log','w+') as f:
                f.write(bgr)

except:
    pass

try:
    if(os.path.exists('C:\\ProgramData\\SideBar\\position.log')):
        with open('C:\\ProgramData\\SideBar\\position.log','r') as f:
            if(str(f.readline()).strip()=='right'):
                right=True
            else:
                right=False
except:
    pass
try:
    if(os.path.exists('C:\\ProgramData\\SideBar\\notes.txt')):
        with open('C:\\ProgramData\\SideBar\\notes.txt','r') as f:
            cntnt=f.read()
except:
    pass
try:
    if(os.path.exists('C:\\ProgramData\\SideBar\\mute.txt')):
        with open('C:\\ProgramData\\SideBar\\mute.txt','r') as f:
            if(str(f.readline()).strip()=='true'):
                mute=True
            else:
                mute=False
except:
    pass

def on_closing():
    global app,run,live
    run=False
    pygame.mixer.music.stop()
    live=False
    app.destroy()
    os._exit(0)

def on_hover():
    global app
    step=16
    if(right):
        pass
    else:
        step=-step
    for x in reversed(range(int(xhover),int(xleave),step)):
        time.sleep(0.001)
        app.geometry('%dx%d+%d+%d' % (ws, hs, x, y))
    app.geometry('%dx%d+%d+%d' % (ws, hs, xhover, y))

def on_leave():
    global app
    step=16
    if(right):
        pass
    else:
        step=-step
    for x in range(int(xhover),int(xleave),step):
        time.sleep(0.001)
        app.geometry('%dx%d+%d+%d' % (ws, hs, x, y))
    app.geometry('%dx%d+%d+%d' % (ws, hs, xleave, y))

def start_hovereffect(event):
    t = threading.Thread(target=on_hover, args=())
    t.daemon = True
    t.start()

def start_leaveeffect(event):
    t = threading.Thread(target=on_leave, args=())
    t.daemon = True
    t.start()
    
def choosecolor():
    global bgr,iconUp,iconDown,speedUp,speedDown,iconTotal,totalUsage,playlabel,prevbut,playbut,nextbut,shufbut,musiclist,backbut,locbut,time_elapsed,total_time,songlabel
    value=askcolor(bgr, app)[1]
    if(not (value is None)):
        bgr=value
        for w in widgetlist:
            w.configure(background=bgr)
        stylescale.configure('TScale',background=bgr)
        if(os.path.exists('C:\\ProgramData\\SideBar')):
            with open('C:\\ProgramData\\SideBar\\sidebardata.log','w+') as f:
                f.write(bgr)
        else:
            os.mkdir('C:\\ProgramData\\SideBar')
            with open('C:\\ProgramData\\SideBar\\sidebardata.log','w+') as f:
                f.write(bgr)

def bar():
    global app,combo,speedUp,speedDown,run,oldcnt,interface,interface_list_at_startup,s,note,autosavelabel
    up=0
    down=0
    notetime=0
    try:
        while(run):
            time.sleep(1)
            notetime+=1
            autosavelabel.configure(text='Auto Save in: '+str(31-notetime)+'Sec')
            if(notetime>30):
                notetime=0
                app.wm_attributes('-topmost', 1)
                try:
                    cntnt=note.get("1.0", 'end-1c')
                    if(not (cntnt=='')):
                        if(not oldcnt==cntnt):
                            with open('C:\\ProgramData\\SideBar\\notes.txt','w+') as f:
                                f.write(cntnt)
                                autosavelabel.configure(text='Saved!')
                                oldcnt=cntnt
                        else:
                            autosavelabel.configure(text='No Changes(not saved)!')
                except:
                    pass
            try:
                bp=ps.sensors_battery().percent
                progress['value'] = bp
                s.configure("LabeledProgressbar",text=" {0}%".format(bp))
                if(ps.sensors_battery().power_plugged):
                    s.configure("LabeledProgressbar",background='#0000c8')
                else:
                    if(bp<20):
                        s.configure("LabeledProgressbar",background='#ff0000')
                    elif(bp<30):
                        s.configure("LabeledProgressbar",background='#ff962a')
                    elif(bp<50):
                        s.configure("LabeledProgressbar",background='#ff8600')
                    elif(bp<60):
                        s.configure("LabeledProgressbar",background='#a3d900')
                    elif(bp<80):
                        s.configure("LabeledProgressbar",background='#00d900')
                    elif(bp<101):
                        s.configure("LabeledProgressbar",background='#009800')
                app.update()
            except:
                pass
            
            try:
                if(interface in list(dict.keys(ps.net_if_stats()))):
                    if(not ps.net_if_stats()[interface].isup):
                        interface_list_new=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
                        previnter=interface
                        interface=list(set(interface_list_new).difference(interface_list_at_startup))[0] if(len(list(set(interface_list_new).difference(interface_list_at_startup)))>0) else interface
                        if(previnter!=interface):
                            combo.set(interface)
                            interface_list_at_startup=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
                            if(os.path.exists('C:\\ProgramData\\SideBar')):
                                with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
                                    f.write(interface)
                            else:
                                os.mkdir('C:\\ProgramData\\SideBar')
                                with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
                                    f.write(interface)
                        continue
                else:
                    interface_list_new=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
                    previnter=interface
                    interface=list(set(interface_list_new).difference(interface_list_at_startup))[0] if(len(list(set(interface_list_new).difference(interface_list_at_startup)))>0) else interface
                    if(previnter!=interface):
                        combo.set(interface)
                        interface_list_at_startup=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
                            
                        if(os.path.exists('C:\\ProgramData\\SideBar')):
                            with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
                                f.write(interface)
                        else:
                            os.mkdir('C:\\ProgramData\\SideBar')
                            with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
                                f.write(interface)
                    continue
                    
                sent=ps.net_io_counters(pernic=True)[interface].bytes_sent
                recv=ps.net_io_counters(pernic=True)[interface].bytes_recv
                total=(sent+recv)/1000
                unitUp=1
                unitDown=1
                unitTotal=1
                upspeed=(sent-up)/1000
                downspeed=(recv-down)/1000
                if(len(str(int(upspeed)))>=4):
                    upspeed=upspeed/1000
                    unitUp=2
                if(len(str(int(downspeed)))>=4):
                    downspeed=downspeed/1000
                    unitDown=2
                if(len(str(int(total)))>=7):
                    total=total/1000000
                    unitTotal=3
                elif(len(str(int(total)))>=4):
                    total=total/1000
                    unitTotal=2
                    
                speedUp.config(text='{0:.2f} {1}/s'.format(upspeed,'KB' if unitUp==1 else 'MB'))
                speedDown.config(text='{0:.2f} {1}/s'.format(downspeed,'KB' if unitDown==1 else 'MB'))
                totalUsage.config(text='{0:.2f} {1}'.format(total,'KB' if unitTotal==1 else 'MB' if unitTotal==2 else 'GB'))
                up=sent
                down=recv
            except:
                pass
    except:
        bp=100
        progress['value'] = bp
        s.configure("LabeledProgressbar",text=" {0}%".format(bp))
        pass

def position():
    global right,app,xhover,xleave
    if(right):
        buttonPosition.configure(text='Right Window')
        right=False
        xhover =-1
        xleave=1-ws
        app.geometry('%dx%d+%d+%d' % (ws, hs, xleave, y))
    else:
        buttonPosition.configure(text='Left Window')
        right=True
        xleave = app.winfo_screenwidth()-2
        xhover=app.winfo_screenwidth()-ws+2
        app.geometry('%dx%d+%d+%d' % (ws, hs, xleave, y))
    if(os.path.exists('C:\\ProgramData\\SideBar')):
        with open('C:\\ProgramData\\SideBar\\position.log','w+') as f:
            if(right):
                f.write('right')
            else:
                f.write('left')
    else:
        os.mkdir('C:\\ProgramData\\SideBar')
        with open('C:\\ProgramData\\SideBar\\position.log','w+') as f:
            if(right):
                f.write('right')
            else:
                f.write('left')



def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def assigninterface(event):
    global interface_list_at_startup,interface
    interface=event.widget.get()
    if(os.path.exists('C:\\ProgramData\\SideBar')):
        with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
            f.write(interface)
    else:
        os.mkdir('C:\\ProgramData\\SideBar')
        with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
            f.write(interface)
    interface_list_at_startup=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]

'''---------------------------------netspeed code above--------------------------------'''

'''----------------------------------music player below-----------------------------'''
def filechooser():
    global loc,dire,dircontent
    dire=filedialog.askdirectory()
    with open('C:\\ProgramData\\SideBar\\dir.txt','w') as f:
        dircontent=f.write(dire)
    dircontent=dire
    wlkfunc(dire)

def autowlk(dire):
    global c,r,d
    d.clear()
    c=0
    thread3=threading.Thread(target=walk,args=(dire,'.mp3'))
    thread3.start()
    
def wlkfunc(dire):
    global c,musiclist,d
    d.clear()
    c=0
    for el in musiclist.get_children():
        musiclist.delete(el)
    thread3=threading.Thread(target=walk,args=(dire,'.mp3'))
    thread3.start()

def walk(dirn,s):
    global d,c,musiclist
    try:
        for i in os.listdir(dirn):
            p=os.path.join(dirn,i)
            if('$RECYCLE.BIN' in p or '\\System Volume Information' in p  or '/System Volume Information' in p):
                pass
            elif(os.path.isfile(p)):
                if(s in str(p)):
                    try:
                        c+=1
                        musiclist.insert("",'end',text=str(c),value=(str(i),),tags = ('odd' if c%2==0 else 'even',))
                        d[i]=p
                    except:
                        pass
            else:
                try:
                    walk(p,s)
                except:
                        pass
        musiclist.bind("<Double-Button-1>",OnDouble)
        musiclist.bind("<Return>",OnDouble)
        '''musiclist.bind("<Down>",OnDown)
        musiclist.bind("<Up>",OnUp)'''
    except Exception as e:
        musiclist.insert("",'end',text="n/a",value=(sre(e)),tags = ('odd',))


def OnDouble(event):
    global song,songnum,songinfo,totlength,pre,d
    pre=0
    widget = event.widget
    song=widget.item(widget.focus())['values'][0]
    collectsonginfoandplay(song)
    
def collectsonginfoandplay(sng):
    global song,songnum,prelist,i,totlength,musiclist
    song=sng
    for index,child in enumerate(musiclist.get_children()):
        if(song==musiclist.item(child)["values"][0]):
            songnum=index
            break
    prelist.append(songnum)
    songid=musiclist.get_children()[songnum]
    musiclist.selection_set(songid)
    musiclist.see(songid)
    songinfo=mutagen.File(d[song])
    totlength=songinfo.info.length
    timeslider.configure(from_=0, to=int(totlength))
    totsec=int(totlength)%60
    totmin=int(totlength)//60
    tothr=totmin//60
    totv.set('%02d:%02d:%02d'%(tothr,totmin,totsec))
    i=0
    play(d[song])


def playorpause():
    if playing is False:
        continu()
    else:
        pause()


def play(song):
    global playing,playbut,pauimg,thread,playlabel,t,artimg,v
    #pygame.init()
    try:
        pygame.mixer.quit()
        mp = mp3.MP3(song)
        pygame.mixer.init(frequency=mp.info.sample_rate)
        clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(v)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        albumart(song)
        playlabel.config(image=artimg)
        playing=True
        playbut.config(image=pauimg)
    except Exception as e:
        pass


def albumart(song):
    global artimg
    file = File(song)
    try:
        artwork = file.tags['APIC:'].data
        with open('C:\\ProgramData\\SideBar\\image.jpg', 'wb') as im:
            im.write(artwork)
        img=Image.open('C:\\ProgramData\\SideBar\\image.jpg')
        img.resize((int(ws*(150/dw)),int(ws*(150/dw)))).save('C:\\ProgramData\\SideBar\\art.png')
        artimg = tk.PhotoImage(file="C:\\ProgramData\\SideBar\\art.png")
    except:
        try:
            f=File(song)
            s=str(mutagen.File(song).tags)
            n=s[:s.find('data=b')][s.find('APIC:'):]
            n=n[n.find('desc=')+6:]
            n=n[:n.find('\'')]
            artwork=f.tags['APIC:'+n].data
            with open('C:\\ProgramData\\SideBar\\image.jpg', 'wb') as im:
                im.write(artwork)
            img=Image.open('C:\\ProgramData\\SideBar\\image.jpg')
            img.resize((int(ws*(150/dw)),int(ws*(150/dw)))).save('C:\\ProgramData\\SideBar\\art.png')
            artimg = tk.PhotoImage(file="C:\\ProgramData\\SideBar\\art.png")
        except:
            img=Image.open(resource_path("art.png"))
            img.resize((int(ws*(150/dw)),int(ws*(150/dw)))).save('C:\\ProgramData\\SideBar\\art.png')
            artimg = tk.PhotoImage(file="C:\\ProgramData\\SideBar\\art.png")


def middleplay(event):
    global totlength,pre,song
    timepos=int((event.x*totlength)/int(ws*(300/dw)))
    timeslider.set(timepos)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(d[song])
    pygame.mixer.music.play()
    pre=timepos
    pygame.mixer.music.set_pos(timepos)

def middlevol(event):
    posy=int((hs*140)/dh)-event.y
    rng=int(int(posy*100)/int((hs*140)/dh))
    v=float('%.1f'%(rng/100))
    vol.set(rng)
    pygame.mixer.music.set_volume(v)
    with open('C:\\ProgramData\\SideBar\\vol.txt','w') as f:
        f.write('vol:'+str(v))

def playtime():
    global tv,hr,minit,sec,pt,timeslider,pre,i,live
    
    while(live):
        try:
            pt=pygame.mixer.music.get_pos()
            if(pt is -1):
                timeslider.set(0)
                sec=0
                minit=0
                hr=0
                if(songnum is not None):
                    i=0
                    time.sleep(.5)
                    if(pygame.mixer.music.get_pos() is -1):
                        nextsong()
            else:
                pt=str(pt)
                pt=pt[:-3]
                if(pt is ''):
                    pt='0000'
                pt=int(pt)
                pt+=pre
                timeslider.set(pt)
                sec=pt%60
                minit=pt//60
                hr=minit//60
            pt='%02d:%02d:%02d'%(hr,minit,sec)
            tv.set(pt)
            time.sleep(1)
        except Exception as e:
            time.sleep(.5)
            pass

def continu():
    global playing,playbut,pauimg
    pygame.mixer.music.unpause()
    playing=True
    playbut.config(image=pauimg)
  

def pause():
    global playing,playbut,playimg
    pygame.mixer.music.pause()
    playing=False
    playbut.config(image=playimg)

def nextsong():
    global song,songnum,totlength,songinfo,pre,i,musiclist,d,c,shuffle,prelist,prelistindex
    pre=0
    if(songnum+1>c-1):
        songnum=0
    else:
        songnum+=1
    if(shuffle):
        songnum=random.randint(0,c+1)
        if(songnum in prelist):
            del(prelist[prelist.index(songnum)])
        prelist.append(songnum)
    '''musiclist.activate(songnum)
    musiclist.see(songnum)'''
    songid=musiclist.get_children()[songnum]
    musiclist.selection_set(songid)
    musiclist.see(songid)
    song = musiclist.item(songid)['values'][0]
    songinfo=mutagen.File(d[song])
    totlength=songinfo.info.length
    timeslider.configure(from_=0, to=int(totlength))
    totsec=int(totlength)%60
    totmin=int(totlength)//60
    tothr=totmin//60
    totv.set('%02d:%02d:%02d'%(tothr,totmin,totsec))
    i=0
    play(d[song])

def previoussong():
    global song,songnum,totlength,songinfo,pre,i,musiclist,d,prelist
    pre=0
    if(songnum-1<0):
        songnum=c-1
    else:
        songnum-=1
    if(shuffle):
        if(not prelist):
            songnum=random.randint(0,c+1)
        else:
            del(prelist[(len(prelist)-1)])
            if(not prelist):
                songnum=random.randint(0,c+1)
                prelist=[songnum]
            else:
                songnum=prelist[(len(prelist)-1)]
    '''musiclist.activate(songnum)
    musiclist.see(songnum) '''
    songid=musiclist.get_children()[songnum]
    musiclist.selection_set(songid)
    musiclist.see(songid)
    song = musiclist.item(songid)['values'][0]
    songinfo=mutagen.File(d[song])
    totlength=songinfo.info.length
    timeslider.configure(from_=0, to=int(totlength))
    totsec=int(totlength)%60
    totmin=int(totlength)//60
    tothr=totmin//60
    totv.set('%02d:%02d:%02d'%(tothr,totmin,totsec))
    i=0
    play(d[song])


def muteorunmute():
    global mute,prevol,v,audio,theme,colrlst
    try:
        if(mute):
            v=prevol
            pygame.mixer.music.set_volume(v)
            vol.set(v*100)
            mutebut.configure(image=soundimg)
            mute=False
            with open('C:\\ProgramData\\SideBar\\mute.txt','w') as f:
                f.write('false')
        else:
            prevol=v
            v=0.0
            pygame.mixer.music.set_volume(v)
            mutebut.configure(image=muteimg)
            vol.set(v*100)
            mute=True
            with open('C:\\ProgramData\\SideBar\\mute.txt','w') as f:
                f.write('true')
    except:
        pass

def initMixer():
    BUFFER = 3072
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)


def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan


def volscroll(event):
    global v,vol
    if(event.delta<0 and (v-0.1 < 0.0) is False):
        voldecrease()
    elif(event.delta>0 and (v+0.1 > 1.0)is False):
        volincrease()
    
def volincrease():
    global v,vol
    v=float('%.1f'%(v))
    if(not v>1.0):
        v+=0.1
        v=float('%.1f'%(v))
        pygame.mixer.music.set_volume(v)
        vol.set(v*100)
        with open('C:\\ProgramData\\SideBar\\vol.txt','w') as f:
            f.write('vol:'+str(v))

def voldecrease():
    global v,vol
    v=float('%.1f'%(v))
    if(not v<0.0):
        v-=0.1
        v=float('%.1f'%(v))
        pygame.mixer.music.set_volume(v)
        vol.set(v*100)
        with open('C:\\ProgramData\\SideBar\\vol.txt','w') as f:
            f.write('vol:'+str(v))

def namedisp():
    global prsntname,song,i,live
    i=0
    try:
        while(live):
            name=song
            prsntname=name[i:]
            i+=1
            playv.set(prsntname)
            if(i is len(name)-1):
                i=0
            time.sleep(0.5)
    except:
        pygame.mixer.music.stop()


def searchmusic():
    global search,musiclist,c,d,backbut,r,loc,locbut,d,refreshbut,nety
    for el in musiclist.get_children():
        musiclist.delete(el)
    searchkey=search.get().lower()
    backbut.place(x=int(ws*(205/dw)),y=nety+int(hs*(405/dh)))
    locbut.place(x=int(ws*(235/dw)),y=nety+int(hs*(405/dh)))
    refreshbut.place(x=int(ws*(265/dw)),y=nety+int(hs*(405/dh)))
    c=0
    for i in d:
        if(searchkey in i.lower()):
            c+=1
            musiclist.insert("",'end',text=str(c),value=(str(i),),tags = ('odd' if c%2==0 else 'even',))

def backlist():
    global dircontent,locbut,d,refreshbut,nety
    if(os.path.isdir(dircontent)):
        wlkfunc(dircontent)
        backbut.place(x=ws,y=nety+int(hs*(405/dh)))
        locbut.place(x=int(ws*(205/dw)),y=nety+int(hs*(405/dh)))
        refreshbut.place(x=int(ws*(235/dw)),y=nety+int(hs*(405/dh)))
        
def refresh():
    global d
    if(os.path.isdir(dircontent)):
        wlkfunc(dircontent)


def shufflesong():
    global shuffle
    if(shuffle is False):
        shuffle=True
        shufbut.configure(image=shuffleimg)
        with open('C:\\ProgramData\\SideBar\\shuf.txt','w') as f:
            f.write('shuffle:1')
    else:
        shuffle=False
        shufbut.configure(image=shuffleoffimg)
        with open('C:\\ProgramData\\SideBar\\shuf.txt','w') as f:
            f.write('shuffle:0')

def clear_entry(event, entry):
    entry.delete(0, tk.END)


if(os.path.exists('C:\\ProgramData\\SideBar\\dir.txt')):
    with open('C:\\ProgramData\\SideBar\\dir.txt','r') as f:
        dircontent=f.readline()

if(os.path.exists('C:\\ProgramData\\SideBar\\vol.txt')):
    with open('C:\\ProgramData\\SideBar\\vol.txt','r') as f:
        volinfo=f.readline()
else:
    volinfo='vol:1.0'

if(os.path.exists('C:\\ProgramData\\SideBar\\shuf.txt')):
    with open('C:\\ProgramData\\SideBar\\shuf.txt','r') as f:
        shufinfo=f.readline()
        if('shuffle' in shufinfo):
            if(shufinfo[8] is '1'):
                shuffle=True
            else:
                shuffle=False

'''---------------------------------music player above---------------------------'''
def showFrame1():
    global fr,fr2
    t = threading.Thread(target=moveright, args=())
    t.daemon = True
    t.start()
    
def showFrame2():
    global fr,fr2
    t = threading.Thread(target=moveleft, args=())
    t.daemon = True
    t.start()
def moveright():
    global fr,fr2
    for i in range(0,int(ws),16):
        fr.place(x=-int(ws)+i,y=int(hs*(25/dh)))
        fr2.place(x=i,y=int(hs*(25/dh)))
        time.sleep(.001)
    fr.place(x=0,y=int(hs*(25/dh)))
    fr2.place(x=int(ws),y=int(hs*(25/dh)))
def moveleft():
    global fr,fr2
    for i in range(0,int(ws),16):
        fr.place(x=-i,y=int(hs*(25/dh)))
        fr2.place(x=int(ws)-i,y=int(hs*(25/dh)))
        time.sleep(.001)
    fr.place(x=-int(ws),y=int(hs*(25/dh)))
    fr2.place(x=0,y=int(hs*(25/dh)))


app=tk.Tk()


ws = app.winfo_screenwidth()*(20/100)
hs = app.winfo_screenheight()-40
if(right):
    xleave = app.winfo_screenwidth()-2
    xhover=app.winfo_screenwidth()-ws+2
else:
    xhover =-1
    xleave=2-ws
y = -1
app.geometry('%dx%d+%d+%d' % (ws, hs, xleave, y))
mainfr=tk.Frame(app,background='black',height = hs, width =ws)

mainfr.pack()
mainfr.bind("<Enter>",start_hovereffect )
mainfr.bind("<Leave>",start_leaveeffect )

if(bgr is ""):
    bgr='#000000'
try:
    fr=tk.Frame(mainfr,background=bgr,height = hs, width =ws)
except:
    bgr='#000000'
    fr=tk.Frame(mainfr,background=bgr,height = hs, width =ws)
fr.place(x=0,y=int(hs*(25/dh)))

buttonClose = tk.Button(mainfr,text='X' ,background='red',height = int(hs*(1/dh)), width =int(ws*(5/dw)),borderwidth=0,command =on_closing,font='Helvetica %d bold'%(int(ws*(10/dw))),state=tk.DISABLED)
#buttonClose.pack(side="right")
buttonClose.place( x =2, y = 0)
buttonClose.bind("<Enter>", lambda event: buttonClose.config(state=tk.NORMAL))
buttonClose.bind("<Leave>", lambda event: buttonClose.config(state=tk.DISABLED))


buttonColor = tk.Button(mainfr,text='Color' ,foreground='white',background='black',height = int(hs*(1/dh)), width =int(ws*(6/dw)),borderwidth=0,command =choosecolor,font='Helvetica %d bold'%(int(ws*(9/dw))))
#buttonClose.pack(side="right")
buttonColor.place( x =int(ws*(50/dw)), y = 0)
buttonColor.bind("<Enter>", lambda event: buttonColor.config(background='white',foreground='black'))
buttonColor.bind("<Leave>", lambda event: buttonColor.config(background='black',foreground='white'))

buttonPosition = tk.Button(mainfr ,foreground='white',background='black',height = int(hs*(1/dh)), width =int(ws*(13/dw)),borderwidth=0,command =position,font='Helvetica %d bold'%(int(ws*(9/dw))))
#buttonClose.pack(side="right")
buttonPosition.place( x =int(ws*(100/dw)), y = 0)
buttonPosition.bind("<Enter>", lambda event: buttonPosition.config(background='white',foreground='black'))
buttonPosition.bind("<Leave>", lambda event: buttonPosition.config(background='black',foreground='white'))


tab1=tk.Button(fr,text='Tab1',foreground='white',background='red',height = int(hs*(1/dh)), width =int(ws*(6/dw)),borderwidth=0,font='Helvetica %d bold'%(int(ws*(9/dw))))
tab1.place(x =int(ws*(50/dw)), y = 2)
tab2=tk.Button(fr,text='Tab2',command=showFrame2,foreground='white',background='black',height = int(hs*(1/dh)), width =int(ws*(6/dw)),borderwidth=0,font='Helvetica %d bold'%(int(ws*(9/dw))))
tab2.place(x =int(ws*(100/dw)), y = 2)
fr2=tk.Frame(mainfr,width=ws,height=hs)
fr2.place(x=ws,y=int(hs*(25/dh)))
fr2.configure(background=bgr)
tab1=tk.Button(fr2,text='Tab1',command=showFrame1,foreground='white',background='black',height = int(hs*(1/dh)), width =int(ws*(6/dw)),borderwidth=0,font='Helvetica %d bold'%(int(ws*(9/dw))))
tab1.place(x =int(ws*(50/dw)), y = 2)
tab2=tk.Button(fr2,text='Tab2',foreground='white',background='red',height = int(hs*(1/dh)), width =int(ws*(6/dw)),borderwidth=0,font='Helvetica %d bold'%(int(ws*(9/dw))))
tab2.place(x =int(ws*(100/dw)), y = 2)

'''note=ScrolledText(fr2,background='yellow',width=int((ws*30)/dw),height=int((hs*25)/dh),font='Helvetica %d'%(int(ws*(12/dw))))
note.place(x=0,y=int(hs*(40/dh)))
note.insert(tk.INSERT, cntnt)'''

autosavelabel = tk.Label(fr2 ,text = "Auto Save in: 0Sec",background='black',foreground='white',font='Helvetica %d bold'%(int(ws*(12/dw))))
autosavelabel.place(x=0,y=int(hs*(40/dh)))

notefr=tk.Frame(fr2,background=bgr)
note=ScrolledText(notefr,background='yellow',font='serif %d bold'%(int(ws*(10/dw))))
note.pack()
notefr.pack()
notefr.place(x=0,y=int(hs*(80/dh)),width=ws,height=hs-int(hs*(80/dh)))
note.insert(tk.INSERT, cntnt)




if(right):
    buttonPosition.configure(text='Left Window')
else:
    buttonPosition.configure(text='Right Window')

app.wm_attributes('-alpha',alpha)
app.wm_attributes('-topmost', 1)
app.resizable(0, 0)
app.overrideredirect(1)
app.protocol("WM_DELETE_WINDOW", on_closing)


s = Style(fr)
s.layout("LabeledProgressbar",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])

l1 = tk.Label(fr, borderwidth=3, relief="ridge")
l1.place(x =int(ws*(24/dw)), y = int(hs*(40/dh)))
# Progress bar widget 
progress = Progressbar(l1, orient = 'horizontal',length = int(ws*(220/dw)), mode = 'determinate',style="LabeledProgressbar")
progress.pack()
s.configure("LabeledProgressbar", thickness=int(hs*(70/dh)),text=" 0%",foreground='white',background='green',font='Helvetica %d bold'%(int(ws*(38/dw))),troughcolor='black')


'''---------------------------Netspeed--------------------------------'''
#iconsize=30
uppath = resource_path("up.png")
'''photo = tk.PhotoImage(file = uppath)
mpUp = photo.subsample(4,4)'''
iconsize=28
mpUp = Image.open(uppath)
mpUp = mpUp.resize((iconsize,iconsize), Image.ANTIALIAS)
mpUp=ImageTk.PhotoImage(mpUp)

downpath= resource_path("down.png")
'''photo = tk.PhotoImage(file = downpath)
mpDown = photo.subsample(4,4)'''
iconsize=28
mpDown = Image.open(downpath)
mpDown = mpDown.resize((iconsize,iconsize), Image.ANTIALIAS)
mpDown=ImageTk.PhotoImage(mpDown)

totalpath= resource_path("updown.png")
'''photo = tk.PhotoImage(file = totalpath)
mpTotal = photo.subsample(16,16)'''
iconsize=30
mpTotal = Image.open(totalpath)
mpTotal = mpTotal.resize((iconsize,iconsize), Image.ANTIALIAS)
mpTotal=ImageTk.PhotoImage(mpTotal)

netx=int(ws*(30/dw))
nety=int(hs*(140/dh))
iconUp = tk.Label(fr ,text = "Up:",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(7/dw))),image=mpUp)
iconUp.place(x=netx,y=nety)
iconDown = tk.Label(fr ,text = "Down:",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(7/dw))),image=mpDown)
iconDown.place(x=netx,y=nety+int(hs*(50/dh)))
speedUp = tk.Label(fr ,text = "0",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(17/dw))))
speedUp.place(x=netx+int(ws*(40/dw)),y=nety)
speedDown = tk.Label(fr ,text = "0",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(17/dw))))
speedDown.place(x=netx+int(ws*(40/dw)),y=nety+int(hs*(50/dh)))

iconTotal = tk.Label(fr ,text = "Total:",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(7/dw))),image=mpTotal)
iconTotal.place(x=netx,y=nety+int(hs*(100/dh)))
totalUsage= tk.Label(fr ,text = "0",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(17/dw))))
totalUsage.place(x=netx+int(ws*(40/dw)),y=nety+int(hs*(100/dh)))
interface_info = tk.Label(fr ,text = "Interface:",background=bgr,foreground='white',font='Helvetica %d bold'%(int(ws*(12/dw))))
interface_info.place(x=0,y=nety+int(hs*(140/dh)))


combo=ttk.Combobox(fr,values=[""],height=15,state="readonly")
combo.bind('<Button-1>',lambda event:combo.configure(values=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]))
combo.bind("<<ComboboxSelected>>", assigninterface)
combo.set(interface)
combo.place(x=netx+50, y=nety+int(hs*(140/dh)))

'''-----------------------------------music player--------------------------------'''


img=Image.open(resource_path("art.png"))
img.resize((int(ws*(150/dw)),int(ws*(150/dw)))).save('C:\\ProgramData\\SideBar\\art.png')
artimg = tk.PhotoImage(file="C:\\ProgramData\\SideBar\\art.png")

previouspath= resource_path("previous.png")
'''photo = tk.PhotoImage(file = previouspath)
previousimg = photo.subsample(12,12)'''
iconsize=int(ws*(38/dw))
previousimg = Image.open(previouspath)
previousimg = previousimg.resize((iconsize,iconsize), Image.ANTIALIAS)
previousimg=ImageTk.PhotoImage(previousimg)

paupath= resource_path("pause.png")
'''photo = tk.PhotoImage(file = paupath)
pauimg = photo.subsample(17,17)'''
iconsize=int(ws*(40/dw))
pauimg = Image.open(paupath)
pauimg = pauimg.resize((iconsize,iconsize), Image.ANTIALIAS)
pauimg=ImageTk.PhotoImage(pauimg)

playpath= resource_path("play.png")
'''photo = tk.PhotoImage(file = playpath)
playimg = photo.subsample(6,6)'''
playimg = Image.open(playpath)
playimg = playimg.resize((iconsize,iconsize), Image.ANTIALIAS)
playimg=ImageTk.PhotoImage(playimg)

nextpath= resource_path("next.png")
'''photo = tk.PhotoImage(file = nextpath)
nextimg = photo.subsample(12,12)'''
iconsize=int(ws*(38/dw))
nextimg= Image.open(nextpath)
nextimg = nextimg.resize((iconsize,iconsize), Image.ANTIALIAS)
nextimg=ImageTk.PhotoImage(nextimg)

mutepath= resource_path("mute.png")
iconsize=int(ws*(38/dw))
muteimg= Image.open(mutepath)
muteimg = muteimg.resize((iconsize,iconsize), Image.ANTIALIAS)
muteimg=ImageTk.PhotoImage(muteimg)

shuffleoffpath= resource_path("shuffleoff.png")
iconsize=int(ws*(34/dw))
shuffleoffimg= Image.open(shuffleoffpath)
shuffleoffimg = shuffleoffimg.resize((iconsize,iconsize), Image.ANTIALIAS)
shuffleoffimg=ImageTk.PhotoImage(shuffleoffimg)

soundpath= resource_path("sound.png")
iconsize=int(ws*(38/dw))
soundimg= Image.open(soundpath)
soundimg = soundimg.resize((iconsize,iconsize), Image.ANTIALIAS)
soundimg=ImageTk.PhotoImage(soundimg)

shufflepath= resource_path("shuffle.png")
'''photo = tk.PhotoImage(file = shufflepath)
shuffleimg = photo.subsample(8,8)'''
iconsize=int(ws*(34/dw))
shuffleimg = Image.open(shufflepath)
shuffleimg = shuffleimg.resize((iconsize,iconsize), Image.ANTIALIAS)
shuffleimg=ImageTk.PhotoImage(shuffleimg)

backpath= resource_path("back.png")
'''photo = tk.PhotoImage(file = backpath)
backimg = photo.subsample(20,20)'''
iconsize=int(ws*(25/dw))
backimg = Image.open(backpath)
backimg = backimg.resize((iconsize,iconsize), Image.ANTIALIAS)
backimg=ImageTk.PhotoImage(backimg)

filechooserpath= resource_path("choosefolder.png")
'''photo = tk.PhotoImage(file = filechooserpath)
filechooserimg = photo.subsample(20,20)'''
filechooserimg = Image.open(filechooserpath)
filechooserimg = filechooserimg.resize((iconsize,iconsize), Image.ANTIALIAS)
filechooserimg=ImageTk.PhotoImage(filechooserimg)

refreshpath= resource_path("refresh.png")
'''photo = tk.PhotoImage(file = refreshpath)
refreshimg = photo.subsample(26,26)'''
refreshimg = Image.open(refreshpath)
refreshimg = refreshimg.resize((iconsize,iconsize), Image.ANTIALIAS)
refreshimg=ImageTk.PhotoImage(refreshimg)


playlabel=tk.Label(fr,bg=bgr,image=artimg)
playlabel.place(x=0,y=nety+int(hs*(180/dh)))

prevbut = tk.Button(fr,command=previoussong,bg=bgr,borderwidth=0,image=previousimg)
prevbut.place(x=int(ws*(155/dw)),y=nety+int(hs*(180/dh)))

playbut = tk.Button(fr,command=playorpause,bg=bgr,borderwidth=0,image=playimg)
playbut.place(x=int(ws*(153/dw)),y=nety+int(hs*(229/dh)))

nextbut = tk.Button(fr,command=nextsong,bg=bgr,borderwidth=0,image=nextimg)
nextbut.place(x=int(ws*(155/dw)),y=nety+int(hs*(280/dh)))

mutebut = tk.Button(fr,command=muteorunmute,bg=bgr,borderwidth=0,image=soundimg)
mutebut.place(x=int(ws*(210/dw)),y=nety+int(hs*(280/dh)))



shufbut = tk.Button(fr,command=shufflesong,bg=bgr,borderwidth=0,image=shuffleoffimg)
shufbut.place(x=int(ws*(210/dw)),y=nety+int(hs*(180/dh)))

if(shuffle):
    shufbut.configure(image=shuffleimg)

'''sb= tk.Scrollbar()
sb.pack( side = tk.RIGHT, fill=tk.Y )'''

'''--------------------------------------------------------------------'''
ns=6
st = ttk.Style()
st.configure("mystyle.Treeview",background='black',rowheight=int(hs*(((dh-610)/ns)/dh)),font=('Calibri', 12), highlightthickness=0, bd=0) # Modify the font of the body
#style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
st.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders


musiclistframe = tk.Frame(fr)#, width=120, height=10,bd=0)
 
musiclistframe.place(x=-20,y=int(hs*(580/dh)))

musiclist=ttk.Treeview(musiclistframe,height=ns,style="mystyle.Treeview", selectmode='browse',show="tree")
musiclist.pack(side='left')

sb = ttk.Scrollbar(musiclistframe, orient="vertical", command=musiclist.yview)
sb.pack(side='right', fill='y')#place(x=30+200+2, y=0, height=200)

musiclist.configure(yscrollcommand=sb.set)



musiclist["columns"]=("one")
musiclist.column("#0", width=int(ws*(50/dw)), minwidth=int(ws*(50/dw)), stretch=tk.NO)
musiclist.column("one", width=int(ws*(260/dw)), minwidth=50, stretch=tk.YES)

musiclist.tag_configure('odd', background='black',foreground='white')
musiclist.tag_configure('even', background='#10181d',foreground='white')

search=tk.Entry(fr,width=int(ws*(25/dw)),bg='white')
search.place(x=0,y=nety+int(hs*(412/dh)))
search.insert(0,'Search Music')
search.bind("<Button-1>", lambda event: clear_entry(event, search))

searchbut=tk.Button(fr,command=searchmusic,borderwidth=0,width=int(ws*(6/dw)),bg='black',fg='white',text='Search')
searchbut.place(x=int(ws*(155/dw)),y=nety+int(hs*(410/dh)))

backbut=tk.Button(fr,command=backlist,bg=bgr,borderwidth=0,image=backimg)
backbut.place(x=ws,y=nety+int(hs*(405/dh)))

locbut=tk.Button(fr,command=filechooser,borderwidth=0,bg=bgr,image=filechooserimg)
locbut.place(x=int(ws*(205/dw)),y=nety+int(hs*(405/dh)))

refreshbut=tk.Button(fr,command=refresh,borderwidth=0,bg=bgr,image=refreshimg)
refreshbut.place(x=int(ws*(235/dw)),y=nety+int(hs*(405/dh)))

stylescale = Style(fr)
#vol =tk.Scale(fr,borderwidth=0,command=controlvol,showvalue='no',highlightthickness=0,length=140,width=18,bg=bgr,from_ = 100,to = 0,orient = tk.VERTICAL ,resolution = 10)
vol=Scale(fr, orient = 'vertical',length=int((hs*140)/dh),from_=100,to=0,style="TScale")
vol.bind('<MouseWheel>',volscroll)
vol.bind('<Button-1>',middlevol)
vol.place(x=int(ws*(260/dw)),y=nety+int(hs*(185/dh)))
vol.set(100)


#timeslider =tk.Scale(fr,borderwidth=0, bg=bgr,showvalue='no',width=18,highlightthickness=0,length=int(ws*(300/dw)),from_=0, to=100, resolution=1, orient=tk.HORIZONTAL)
timeslider=Scale(fr, orient = 'horizontal',length=ws,from_=0,to=100,style="TScale")
timeslider.bind('<Button-1>',middleplay)
timeslider.place(x=0,y=nety+int(hs*(360/dh)))

stylescale.configure("TScale",background=bgr)

tv = tk.StringVar()
time_elapsed = tk.Label(fr,bg=bgr,fg='white',textvariable=tv)
time_elapsed.place(x=0,y=nety+int(hs*(385/dh)))
tv.set('00:00:00')

totv = tk.StringVar()
total_time = tk.Label(fr,bg=bgr,fg='white',textvariable=totv)
total_time.place(x=int(ws-56),y=nety+int(hs*(385/dh)))
totv.set('00:00:00')


playv = tk.StringVar()
songlabel= tk.Label(fr,fg='white',bg=bgr,font=("bold", 10),textvariable=playv)
songlabel.place(x=0,y=nety+int(hs*(335/dh)))
playv.set(prsntname)

widgetlist=[fr,
            fr2,
            iconUp,
            iconDown,
            speedUp,
            speedDown,
            iconTotal,
            totalUsage,
            playlabel,
            prevbut,
            playbut,
            nextbut,
            interface_info,
            backbut,
            locbut,
            time_elapsed,
            total_time,
            songlabel,
            refreshbut,
            mutebut,
            shufbut,
            notefr]

if(dircontent!=None and os.path.isdir(dircontent)):
    autowlk(dircontent)
   
initMixer()  
try:
    if(volinfo.startswith('vol:')):
        v=float(volinfo[4:])
        pygame.mixer.music.set_volume(v)
        prevol=v
        vol.set(v*100)
except:
    v=1.0
    pygame.mixer.music.set_volume(v)
    vol.set(v*100)


if(mute):
    mutebut.configure(image=muteimg)
    vol.set(0)
    pygame.mixer.music.set_volume(0)

try:
    t = threading.Thread(target=bar, args=())
    t.daemon = True
    t.start()
except:
    pass
try:
    thread1=threading.Thread(target=playtime,args=())
    thread1.start()

    thread2=threading.Thread(target=namedisp,args=())
    thread2.start()
except:
    pygame.mixer.music.stop()


'''-----------------------------------music player--------------------------------'''
app.mainloop()
