import tkinter as tk
import os,sys
import time
from PIL import Image,ImageTk
import threading
from tkinter.ttk import Progressbar, Style
from tkcolorpicker import askcolor
from tkinter import filedialog
import psutil as ps

import tkinter as tk
from mutagen import File
import mutagen
import random
import pygame



netinterface=None
interbool=False
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

'''----------------------------------------netspeed below--------------------------------'''
speedUp=None
speedDown=None
interface=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)][0]
interface_list_at_startup=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
buttonSelectInterface=None
xpos,ypos=0,0

if(len(interface)==0):
    os._exit(0)


try:
    startupfile=winshell.startup()+sys.argv[0][sys.argv[0].rfind("\\"):]
    if(os.path.exists(startupfile)):
        if(startupfile!=sys.argv[0]):
            currentfile='\"'+sys.argv[0]+'\"'
            destination='\"'+startupfile+'\"'
            os.system('copy '+currentfile+' '+destination)
        else:
            pass
    else:
        currentfile='\"'+sys.argv[0]+'\"'
        destination='\"'+startupfile+'\"'
        os.system('copy '+currentfile+' '+destination)
except:
    pass


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
    global bgr,iconUp,iconDown,speedUp,speedDown,iconTotal,totalUsage,playlabel,prevbut,playbut,nextbut,shufbut,musiclist,searchbut,backbut,locbut,time_elapsed,total_time,songlabel
    bgr=askcolor(bgr, app)[1]
    fr.configure(background=bgr)
    iconUp.configure(background=bgr)
    iconDown.configure(background=bgr)
    speedUp.configure(background=bgr)
    speedDown.configure(background=bgr)
    iconTotal.configure(background=bgr)
    totalUsage.configure(background=bgr)
    playlabel.configure(background=bgr)
    prevbut.configure(background=bgr)
    playbut.configure(background=bgr)
    nextbut.configure(background=bgr)
    vol.configure(background=bgr)
    timeslider.configure(background=bgr)
    if(shuffle):
        shufbut.configure(background='grey')
    else:
        shufbut.configure(background=bgr)
    musiclist.configure(background=bgr)
    searchbut.configure(background=bgr)
    backbut.configure(background=bgr)
    locbut.configure(background=bgr)
    time_elapsed.configure(background=bgr)
    total_time.configure(background=bgr)
    songlabel.configure(background=bgr)
    refreshbut.configure(background=bgr)
    if(os.path.exists('C:\\ProgramData\\SideBar')):
        with open('C:\\ProgramData\\SideBar\\sidebardata.log','w+') as f:
            f.write(bgr)
    else:
        os.mkdir('C:\\ProgramData\\SideBar')
        with open('C:\\ProgramData\\SideBar\\sidebardata.log','w+') as f:
            f.write(bgr)

def bar():
    global speedUp,speedDown,run,interface,interface_list_at_startup,buttonSelectInterface,s
    up=0
    down=0
    try:
        while(run):
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
                            buttonSelectInterface.config(text=interface[0])
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
                        buttonSelectInterface.config(text=interface[0])
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
            time.sleep(1)
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



def getnetinterface():
    global buttonSelectInterface,interface,bgr,interface_list_at_startup,hs,ws,netinterface,interbool
    
    w=int(ws*(175/dw))
    h=int(hs*(30/dh))
    x,y=xhover,int(hs*(350/dh))
    netinterface = tk.Tk()
    interbool=True
    netinterface.title("Select Network Interface")
    netinterface.geometry('%dx%d+%d+%d' % (w, h, x, y))
    netinterface.wm_attributes('-alpha',alpha)
    netinterface.wm_attributes('-topmost', 1)

    var = tk.StringVar(netinterface)
    var.set("Select Network Interface")

    def grab_and_assign(event):
       global buttonSelectInterface,interface,bgr,interface_list_at_startup
       chosen_option = var.get()
       interface=chosen_option
       if(os.path.exists('C:\\ProgramData\\SideBar')):
           with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
               f.write(interface)
       else:
           os.mkdir('C:\\ProgramData\\SideBar')
           with open('C:\\ProgramData\\SideBar\\netinterfacedata.log','w+') as f:
               f.write(interface)
       buttonSelectInterface.config(text=interface)
       interface_list_at_startup=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
       netinterface.destroy()
       interbool=False
    lst=[itf for itf in list(dict.keys(ps.net_if_stats())) if(ps.net_if_stats()[itf].isup)]
    drop_menu = tk.OptionMenu(netinterface, var,*lst, command=grab_and_assign)
    drop_menu.config(bg=bgr,fg='white')
    drop_menu.grid(row=0, column=0)

    netinterface.resizable(0, 0)
    netinterface.overrideredirect(1)
    netinterface.configure(background=bgr)
    
    netinterface.mainloop()
def cancel(event):
    global netinterface,interbool
    try:
        if(interbool):
            netinterface.destroy()
            interbool=False
    except:
        pass

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
    musiclist.delete(0,tk.END)
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
                        musiclist.insert(tk.END,i)
                        d[i]=p
                    except:
                        pass
            else:
                try:
                    walk(p,s)
                except:
                        pass
        musiclist.bind("<Double-Button-1>",OnDouble)
    except Exception as e:
        musiclist.insert(tk.END,str(e))


def OnDouble(event):
    global song,songnum,songinfo,totlength,pre,d
    pre=0
    widget = event.widget
    songnum=widget.curselection()[0]
    song = widget.get(songnum)
    collectsonginfoandplay(song)

def collectsonginfoandplay(sng):
    global song,songnum,prelist,i,totlength
    song=sng
    songnum = musiclist.get(0, "end").index(song)
    prelist.append(songnum)
    musiclist.activate(songnum)
    musiclist.see(songnum)
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
    global playing,playbut,pauimg,thread,playlabel,t,artimg
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    albumart(song)
    playlabel.config(image=artimg)
    playing=True
    playbut.config(image=pauimg)


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
    v=float(((100-event.y)*1.0)/100)
    vol.set(v*100)
    pygame.mixer.music.set_volume(v)
    with open('C:\\ProgramData\\SideBar\\vol.txt','w') as f:
        f.write('vol:'+str(v))

def playtime():
    global tv,hr,minit,sec,pt,timeslider,pre,i,live
    try:
        while(live):
            pt=pygame.mixer.music.get_pos()
            if(pt is -1):
                timeslider.set(0)
                sec=0
                minit=0
                hr=0
                if(songnum is not None):
                    i=0
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
    except:
        pygame.mixer.music.stop()

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
    musiclist.activate(songnum)
    musiclist.see(songnum)
    song = musiclist.get(songnum)
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
    musiclist.activate(songnum)
    musiclist.see(songnum)        
    song = musiclist.get(songnum)
    songinfo=mutagen.File(d[song])
    totlength=songinfo.info.length
    timeslider.configure(from_=0, to=int(totlength))
    totsec=int(totlength)%60
    totmin=int(totlength)//60
    tothr=totmin//60
    totv.set('%02d:%02d:%02d'%(tothr,totmin,totsec))
    i=0
    play(d[song])

def initMixer():
    BUFFER = 3072
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)


def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan

def controlvol(event):
    global v
    v=(float(event)*1.0)/100.0
    pygame.mixer.music.set_volume(v)
    with open('C:\\ProgramData\\SideBar\\vol.txt','w') as f:
        f.write('vol:'+str(v))

def volscroll(event):
    global v,vol
    if(event.delta<0 and (v-0.1 < 0.0) is False):
        voldecrease()
    elif(event.delta>0 and (v+0.1 > 1.0)is False):
        volincrease()
    
def volincrease():
    global v,vol
    v+=0.1
    pygame.mixer.music.set_volume(v)
    vol.set(v*100)
    with open('C:\\ProgramData\\SideBar\\vol.txt','w') as f:
        f.write('vol:'+str(v))
    

def voldecrease():
    global v,vol
    v-=0.1
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
    global search,musiclist,c,d,backbut,r,loc,locbut,d,refreshbut
    musiclist.delete(0,tk.END)
    searchkey=search.get().lower()
    backbut.place(x=int(ws*(205/dw)),y=int(hs*(575/dh)))
    locbut.place(x=int(ws*(235/dw)),y=int(hs*(575/dh)))
    refreshbut.place(x=int(ws*(265/dw)),y=int(hs*(575/dh)))
    c=0
    for i in d:
        if(searchkey in i.lower()):
            c+=1
            musiclist.insert(tk.END,i)

def backlist():
    global dircontent,locbut,d,refreshbut
    if(os.path.isdir(dircontent)):
        wlkfunc(dircontent)
        backbut.place(x=ws,y=int(hs*(575/dh)))
        locbut.place(x=int(ws*(205/dw)),y=int(hs*(575/dh)))
        refreshbut.place(x=int(ws*(235/dw)),y=int(hs*(575/dh)))
        
def refresh():
    global d
    if(os.path.isdir(dircontent)):
        wlkfunc(dircontent)


def shufflesong():
    global shuffle
    if(shuffle is False):
        shuffle=True
        shufbut.configure(bg='grey')
        with open('C:\\ProgramData\\SideBar\\shuf.txt','w') as f:
            f.write('shuffle:1')
    else:
        shuffle=False
        shufbut.configure(bg=bgr)
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
try:
    fr=tk.Frame(app,background=bgr,height = hs, width =ws)
except:
    bgr='#000000'
    fr=tk.Frame(app,background=bgr,height = hs, width =ws)
fr.pack()
fr.bind("<Enter>",start_hovereffect )
fr.bind("<Leave>",start_leaveeffect )

buttonClose = tk.Button(fr,text='X' ,background='red',height = int(hs*(1/dh)), width =int(ws*(4/dw)),borderwidth=0,command =on_closing,font='Helvetica %d bold'%(int(ws*(12/dw))),state=tk.DISABLED)
#buttonClose.pack(side="right")
buttonClose.place( x =2, y = 0)
buttonClose.bind("<Enter>", lambda event: buttonClose.config(state=tk.NORMAL))
buttonClose.bind("<Leave>", lambda event: buttonClose.config(state=tk.DISABLED))


buttonColor = tk.Button(fr,text='Color' ,foreground='white',background='black',height = int(hs*(1/dh)), width =int(ws*(6/dw)),borderwidth=0,command =choosecolor,font='Helvetica %d bold'%(int(ws*(9/dw))))
#buttonClose.pack(side="right")
buttonColor.place( x =int(ws*(50/dw)), y = 0)
buttonColor.bind("<Enter>", lambda event: buttonColor.config(background='white',foreground='black'))
buttonColor.bind("<Leave>", lambda event: buttonColor.config(background='black',foreground='white'))

buttonPosition = tk.Button(fr ,foreground='white',background='black',height = int(hs*(1/dh)), width =int(ws*(13/dw)),borderwidth=0,command =position,font='Helvetica %d bold'%(int(ws*(9/dw))))
#buttonClose.pack(side="right")
buttonPosition.place( x =int(ws*(100/dw)), y = 0)
buttonPosition.bind("<Enter>", lambda event: buttonPosition.config(background='white',foreground='black'))
buttonPosition.bind("<Leave>", lambda event: buttonPosition.config(background='black',foreground='white'))

if(right):
    buttonPosition.configure(text='Left Window')
else:
    buttonPosition.configure(text='Right Window')

app.wm_attributes('-alpha',alpha)
app.wm_attributes('-topmost', 1)
app.resizable(0, 0)
app.overrideredirect(1)
app.protocol("WM_DELETE_WINDOW", on_closing)
app.bind('<Button-1>',cancel)


s = Style(fr)
s.layout("LabeledProgressbar",
         [('LabeledProgressbar.trough',
           {'children': [('LabeledProgressbar.pbar',
                          {'sticky': 'ns'}),
                         ("LabeledProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])

l1 = tk.Label(fr, borderwidth=6, relief="ridge")
l1.place(x =int(ws*(24/dw)), y = int(hs*(60/dh)))
# Progress bar widget 
progress = Progressbar(l1, orient = 'horizontal',length = int(ws*(220/dw)), mode = 'determinate',style="LabeledProgressbar")
progress.pack()
s.configure("LabeledProgressbar", thickness=int(hs*(70/dh)),text=" 0%",foreground='white',background='green',font='Helvetica %d bold'%(int(ws*(38/dw))),troughcolor='black')

t = threading.Thread(target=bar, args=())
t.daemon = True
t.start()

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
nety=int(hs*(160/dh))
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
buttonSelectInterface = tk.Button(fr, text=interface,borderwidth=0,background='black',foreground='white',command =getnetinterface,font='Helvetica %d bold'%(int(ws*(14/dw))))
buttonSelectInterface.place(x=netx, y=nety+int(hs*(150/dh)))
buttonSelectInterface.bind("<Enter>", lambda event: buttonSelectInterface.config(background='grey'))
buttonSelectInterface.bind("<Leave>", lambda event: buttonSelectInterface.config(background='black'))


'''-----------------------------------music player--------------------------------'''


'''artpath= resource_path("art.png")
photo = tk.PhotoImage(file = artpath)
artimg = photo.subsample(4,4)'''

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
playlabel.place(x=0,y=int(hs*(350/dh)))

prevbut = tk.Button(fr,command=previoussong,bg=bgr,borderwidth=0,image=previousimg)
prevbut.place(x=int(ws*(155/dw)),y=int(hs*(350/dh)))

playbut = tk.Button(fr,command=playorpause,bg=bgr,borderwidth=0,image=playimg)
playbut.place(x=int(ws*(153/dw)),y=int(hs*(399/dh)))

nextbut = tk.Button(fr,command=nextsong,bg=bgr,borderwidth=0,image=nextimg)
nextbut.place(x=int(ws*(155/dw)),y=int(hs*(450/dh)))

shufbut = tk.Button(fr,command=shufflesong,bg=bgr,borderwidth=0,image=shuffleimg)
shufbut.place(x=int(ws*(210/dw)),y=int(hs*(350/dh)))

if(shuffle):
    shufbut.configure(bg='grey')

sb= tk.Scrollbar()
sb.pack( side = tk.RIGHT, fill=tk.Y )


musiclist = tk.Listbox(fr,yscrollcommand = sb.set,font=("bold", 10),background=bgr,foreground='white',selectmode=tk.SINGLE,width=int(ws)-int(ws*(264/dw)),height=int(hs*(12/dh)))
musiclist.place(x=0,y=int(hs*(606/dh)))
sb.config( command = musiclist.yview )

search=tk.Entry(fr,width=25,bg='white')
search.place(x=0,y=int(hs*(582/dh)))
search.insert(0,'Search Music')
search.bind("<Button-1>", lambda event: clear_entry(event, search))

searchbut=tk.Button(fr,command=searchmusic,borderwidth=0,width=6,bg='black',fg='white',text='Search')
searchbut.place(x=int(ws*(155/dw)),y=int(hs*(580/dh)))

backbut=tk.Button(fr,command=backlist,bg=bgr,borderwidth=0,image=backimg)
backbut.place(x=ws,y=int(hs*(575/dh)))

locbut=tk.Button(fr,command=filechooser,borderwidth=0,bg=bgr,image=filechooserimg)
locbut.place(x=int(ws*(205/dw)),y=int(hs*(575/dh)))

refreshbut=tk.Button(fr,command=refresh,borderwidth=0,bg=bgr,image=refreshimg)
refreshbut.place(x=int(ws*(235/dw)),y=int(hs*(575/dh)))

vol =tk.Scale(fr,borderwidth=0,command=controlvol,showvalue='no',highlightthickness=0,length=140,width=18,bg=bgr,from_ = 100,to = 0,orient = tk.VERTICAL ,resolution = 10)
vol.bind('<MouseWheel>',volscroll)
vol.bind('<Button-1>',middlevol)
vol.place(x=int(ws*(260/dw)),y=int(hs*(355/dh)))
vol.set(100)

timeslider =tk.Scale(fr,borderwidth=0, bg=bgr,showvalue='no',width=18,highlightthickness=0,length=int(ws*(300/dw)),from_=0, to=100, resolution=1, orient=tk.HORIZONTAL)
timeslider.bind('<Button-1>',middleplay)
timeslider.place(x=0,y=int(hs*(530/dh)))

tv = tk.StringVar()
time_elapsed = tk.Label(fr,bg=bgr,fg='white',textvariable=tv)
time_elapsed.place(x=0,y=int(hs*(550/dh)))
tv.set('00:00:00')

totv = tk.StringVar()
total_time = tk.Label(fr,bg=bgr,fg='white',textvariable=totv)
total_time.place(x=int(ws-56),y=int(hs*(550/dh)))
totv.set('00:00:00')


playv = tk.StringVar()
songlabel= tk.Label(fr,fg='white',bg=bgr,font=("bold", 10),textvariable=playv)
songlabel.place(x=0,y=int(hs*(505/dh)))
playv.set(prsntname)


if(dircontent!=None and os.path.isdir(dircontent)):
    autowlk(dircontent)
   
initMixer()
try:
    if(volinfo.startswith('vol:')):
        v=float(volinfo[4:])
        pygame.mixer.music.set_volume(v)
        vol.set(v*100)
except:
    v=1.0
    pygame.mixer.music.set_volume(v)
    vol.set(v*100)

try:
    thread1=threading.Thread(target=playtime,args=())
    thread1.start()

    thread2=threading.Thread(target=namedisp,args=())
    thread2.start()
except:
    pygame.mixer.music.stop()


'''-----------------------------------music player--------------------------------'''
app.mainloop()
