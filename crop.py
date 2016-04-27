from Tkinter import *
import PIL
from PIL import Image, ImageTk
import json
import os.path as path
import os

global boxes
boxes = list()
global canvas
global color
global beditting
global paireditting
objColor = "blue"
#defines when to start a new box
tolerance = 50
#which box are we editting
global beditting
beditting = 0
paireditting = 0
#line width
lineWidth=3

#base directory
baseFolder="E:\DCIM\\base_dir"
#image dir
imgFolder="E:\DCIM\\dataset"
#dir for final images
finImgFolder="E:\DCIM\\dataset_complete"

global color_table
global name_table
global object_table
global img_name
global canvas_img #stores canvas image to delete later
global cur_img_num

canvas_img=None #give this a value we can check for later to see if there is already an image
cur_img_num = 0 #stores the index of the all_images array that img_name is

#load the config files
color_table = json.loads(open(path.join(baseFolder, "colors.json")).read())
name_table = json.loads(open(path.join(baseFolder, "names.json")).read())
number_table = json.loads(open(path.join(baseFolder, "number.json")).read())

try:
    object_table = json.loads(open(path.join(baseFolder, "objects.json")).read())
except:
    object_table=dict()

all_images = os.listdir(imgFolder) #the names of all the files in the imgFolder

#we need to initially set the img_name so that this loop will work
img_name=all_images[0]
i=1
while(img_name in object_table.keys()):
    print img_name
    img_name=all_images[i]
    cur_img_num=i
    i=i+1

def load_picture():
    global canvas
    global color_table
    global name_table
    global object_table
    global img_name
    global canvas_img #stores canvas image to delete later
    global cur_img_num
    global canvas_img
    global photo #because python garbage collecting destroys the img
    if canvas_img: #canvas image is not None
        print("already a picture in canvas... removing it")
        canvas.delete(canvas_img)
    print(path.join(imgFolder, img_name))
    image = Image.open(path.join(imgFolder, img_name))
    scaler = 0.75
    size = 3088*scaler, 2056*scaler
    image.thumbnail(size, Image.ANTIALIAS)
    """basewidth = 800 #TODO: make resizable
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)"""
    photo = ImageTk.PhotoImage(image)
    canvas_img = canvas.create_image(0, 0, image=photo)
    if len(boxes)>0:
        for i in range(len(boxes)-1): #originally made the mistake fo doing item in boxes, but del item then does nothing
            canvas.delete(boxes[i]
                          [1]) #remove from the canvas first
        for i in range(len(boxes)-1):
            del boxes[0]
    #print(boxes)
    beditting=len(boxes)-1
    #print(json.dumps(object_table, sort_keys=True, indent=4, separators=(',', ': ')))
    try:
        #print(json.dumps(object_table[img_name], sort_keys=True, indent=4, separators=(',', ': ')))
        #print("now")
        print "loading "+str(len(object_table[img_name]))+" boxes from "+str(img_name)
        for item in object_table[img_name]:
            canvas.create_rectangle(item['coords'][0],
                                    item['coords'][1],
                                    item['coords'][2],
                                    item['coords'][3],
                                    outline=item['color'],
                                    width=lineWidth)
            boxes.append((item["color"], canvas.create_rectangle(item['coords'][0], item['coords'][1], item['coords'][2], item['coords'][3], outline=item['color'], width=lineWidth)))
    except KeyError:
        print img_name + " does not exist yet in database"
        pass #this just means there is none

#save everything to temp files
def write_out_autosave():
    global name_table
    global object_table
    global img_name
    global canvas_img #stores canvas image to delete later
    global cur_img_num
    open(path.join(baseFolder, "colors_temp.json"), 'w').write(json.dumps(color_table, sort_keys=True, indent=4, separators=(',', ': ')))
    open(path.join(baseFolder, "names_temp.json"), 'w').write(json.dumps(name_table, sort_keys=True, indent=4, separators=(',', ': ')))
    open(path.join(baseFolder, "number_temp.json"), 'w').write(json.dumps(number_table, sort_keys=True, indent=4, separators=(',', ': ')))
    open(path.join(baseFolder, "objects_temp.json"), 'w').write(json.dumps(object_table, sort_keys=True, indent=4, separators=(',', ': ')))

#save everything
def write_out():
    global name_table
    global object_table
    global img_name
    global canvas_img #stores canvas image to delete later
    global cur_img_num
    open(path.join(baseFolder, "colors.json"), 'w').write(json.dumps(color_table, sort_keys=True, indent=4, separators=(',', ': ')))
    open(path.join(baseFolder, "names.json"), 'w').write(json.dumps(name_table, sort_keys=True, indent=4, separators=(',', ': ')))
    open(path.join(baseFolder, "number.json"), 'w').write(json.dumps(number_table, sort_keys=True, indent=4, separators=(',', ': ')))
    open(path.join(baseFolder, "objects.json"), 'w').write(json.dumps(object_table, sort_keys=True, indent=4, separators=(',', ': ')))
                                                               
def key(event):
    global name_table
    global object_table
    global img_name
    global canvas_img #stores canvas image to delete later
    global cur_img_num
    global objColor
    print "pressed", repr(event.char)
    print(event.keycode)
    if(event.char.isdigit()):
        print('digit')
        number=int(event.char)
        objColor=color_table[number]
    if(len(boxes)==0):
        return #nothing to be done after the above commands
    if(event.char=="z"):
        canvas.delete(boxes[len(boxes)-1][1])
        del boxes[len(boxes)-1] #remove last one
        if len(object_table[img_name])==1: #if it is the last one, remove the entry
            del objects_table[img_name]
        else:
            del objects_table[img_name][len(object_table[img_name])-1] #remove last item
        write_out_autosave()

#TODO: fix and use code
def within_range(bcoord, ccoord):
    print(0<bcoord[2]-ccoord[0]<tolerance)
    print(0<ccoord[0]-bcoord[2]<tolerance)
    if 0<bcoord[0]-ccoord[0]<tolerance or 0<ccoord[0]-bcoord[0]<tolerance:
        if 0<bcoord[1]-ccoord[1]<tolerance or 0<ccoord[1]-bcoord[1]<tolerance:
            print("0")
            return (True, 0)
    if 0<bcoord[2]-ccoord[0]<tolerance or 0<ccoord[0]-bcoord[2]<tolerance:
        if 0<bcoord[3]-ccoord[1]<tolerance or 0<ccoord[1]-bcoord[3]<tolerance:
            print("1")
            return (True, 1) #also return which pair it is part of
    return (False, None)
        
def click_started(event):
    #should we create a new bounding box
    """i=0
    for box in boxes:
        if(box[0]==color):
            bbox = canvas.coords(box[1])
            within = within_range(bbox, (event.x, event.y))
            if(within[0]): #only the boolean value
                beditting=i
                print("within")
                paireditting=within[1]
                return None #stop from creating a new box"""
                
        
    #store new shape and the color
    boxes.append((objColor, canvas.create_rectangle(event.x, event.y, event.x+1, event.y+1, outline=objColor, width=lineWidth)))
    #beditting = len(boxes)-1 #store which one we are now editting
    print(beditting)

def dragging(event):
    beditting = len(boxes)-1 #store which one we are now editting
    old = canvas.coords(boxes[beditting][1]) #get last position
    
    if(paireditting==1): #is pairedditing 1
        canvas.coords(boxes[beditting][1], (old[0], old[1], event.x, event.y))
    else: #edit first pair
        canvas.coords(boxes[beditting][1], (event.x, event.y, old[2], old[3]))

def released(event):
    global name_table
    global object_table
    global img_name
    global canvas_img #stores canvas image to delete later
    global cur_img_num
    beditting = len(boxes)-1 #store which one we are now editting
    number_table[objColor]=number_table[objColor]+1
    try:
        object_table[img_name].append({"color":objColor, "coords":(canvas.coords(boxes[beditting][1])), "number":number_table[objColor]})
    except KeyError:
       object_table[img_name] = list()
       object_table[img_name].append({"color":objColor, "coords":(canvas.coords(boxes[beditting][1])), "number":number_table[objColor]})
    write_out_autosave()
    

def Open():
    pass

def save():
    write_out()

def saveas():
    pass

def change_color(color):
    print(color)
    global objColor
    objColor=color

def next_picture():
    global img_name
    global cur_img_num
    cur_img_num=cur_img_num+1
    img_name=all_images[cur_img_num]
    load_picture()

def previous_picture():
    global img_name
    global cur_img_num
    cur_img_num=cur_img_num-1
    img_name=all_images[cur_img_num]
    load_picture()

root = Tk()
root.bind("<Key>", key)
root.geometry('1920x1080')
#bar
frame = Frame(root)
buttonFrame = Frame(frame)
Button(buttonFrame, text="save", command=save).pack(side=LEFT)
Button(buttonFrame, text="open", command=Open).pack(side=LEFT)
Button(buttonFrame, text="save as", command=saveas).pack(side=LEFT)
buttonFrame.pack()
Label(frame, text="picture controls").pack()
controlFrame = Frame(frame)
Button(controlFrame, text="back", command=previous_picture).pack(side=LEFT)
Button(controlFrame, text="next", command=next_picture).pack(side=LEFT)
controlFrame.pack()
for color,name in zip(color_table, name_table):
    Button(frame, text=name, command=lambda c=color: change_color(c),  bg=color).pack()
frame.pack(side=LEFT)
canvas = Canvas(root,width=999,height=999)
canvas.bind("<Button-1>", click_started)
canvas.bind("<B1-Motion>", dragging)
canvas.bind("<ButtonRelease-1>", released)
canvas.pack(side=LEFT)
load_picture()

root.mainloop()
