import matplotlib.pyplot as plt

from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import *
import tkinter.ttk as ttk
import tkinter.messagebox
global myProcess
#global myMemory
global technique
global my_memory
global list_of_process
list_of_process = []
global root4

class Segment():
    def __init__(self,info_list):
        self.name = info_list[0]
        self.size = info_list[1]
    def Set_Start (self,start):
        self.Start = start
class Process():
    list_of_segments=[]
    def __init__(self,name):
        self.list_of_segments = []
        self.name = name
    def CreateSegment (self,SegmentParameters):
        self.list_of_segments.append(Segment(SegmentParameters))
    def delete_from_memory (self):
        for segment in self.list_of_segments:
            my_memory.De_Allocate(segment.Start)


class Memory():
    def __init__(self,size):
        self.memory_units = size
        self.Allocated_Memory = []
    def Get_Holes (self):
        self.Allocated_Memory.sort()
        if len(self.Allocated_Memory) == 0:
            return [[0,self.memory_units]]
        else :
            list_of_holes = []

            for i in range (len(self.Allocated_Memory)):
                if i==0 and self.Allocated_Memory[i][0] != 0 :
                    start=0
                    size =  self.Allocated_Memory[i][0]
                    if size > 0 :
                        list_of_holes.append([start,size])
                elif i !=0 :
                    start=self.Allocated_Memory[i-1][0]+self.Allocated_Memory[i-1][1]
                    size = self.Allocated_Memory[i][0] - start
                    if size > 0 :
                        list_of_holes.append([start, size])
            if self.Allocated_Memory[-1][0] + self.Allocated_Memory[-1][1]-1 < self.memory_units :
                list_of_holes.append([self.Allocated_Memory[-1][0]+self.Allocated_Memory[-1][1],self.memory_units - (self.Allocated_Memory[-1][0]+self.Allocated_Memory[-1][1]+1) ]      )
            return list_of_holes
    def Allocate_Memory_FF (self,segment_size,segment_name):
        mylist = self.Get_Holes ()
        flag = False
        for hole in mylist:
            if segment_size <= hole[1]:
                self.Allocated_Memory.append([hole[0],segment_size,segment_name])
                flag =True
                return hole[0]
                Draw(myMemory) # initial drawing
        if(not flag):
            return -1
    def Allocate_Memory_BF(self,segment_size,segment_name):
        mylist = self.Get_Holes()
        myCandidate_Holes = []
        flag = False
        for hole in mylist:
            if segment_size <= hole[1]:
                flag = True
                myCandidate_Holes.append([hole[1],hole[0]])
        if (flag):
            myCandidate_Holes.sort()
            self.Allocated_Memory.append( [ myCandidate_Holes[0][1] , segment_size,segment_name])
            return myCandidate_Holes[0][1]
        else:
            return -1
    def De_Allocate(self,start):
        for segment in self.Allocated_Memory:
            if start == segment[0]:
                self.Allocated_Memory.remove(segment)
    def initiallize_memory(self,holes_entry):
        holes = []
        for entry in holes_entry:
            holes.append([int(entry[0].get()),int(entry[1].get())])
        holes.sort()
        for hole in range (len(holes)):
            if hole == 0 and holes[hole][0] != 0:
                start = 0
                size = holes[hole][0]
                if size > 0:
                    self.Allocated_Memory.append([start,size,None])
            elif hole > 0:
                start = holes[hole - 1][0] + holes[hole - 1][1]
                size = holes[hole][0] - start
                if size > 0:
                    self.Allocated_Memory.append([start, size,None])
        if holes[-1][0] + holes[-1][1]  < self.memory_units:
            self.Allocated_Memory.append([holes[-1][0] + holes[-1][1], self.memory_units - (
                        holes[-1][0] + holes[-1][1] + 1),None])
        root4.destroy()



def onclick(event):
    global myProcess
    global fig
    global gnt
    global textvar
    global mybars
    global mytexts
    chosenstart = 0
    chosenend = 0
    if event.dblclick:
        myclick = event.ydata
        for segment in my_memory.Allocated_Memory:
            if myclick>segment[0] and (myclick<segment[0]+segment[1]):
                chosenstart = segment[0]
                chosenend = segment[0]+segment[1]
        for text in mytexts:
            if int(float(str(text).split(", ")[1])) > chosenstart and int(float(str(text).split(", ")[1])) <= chosenend:
                mytexts.remove(text)
                text.remove()

        for bar in mybars:
            if bar.patches[0].get_y() == chosenstart:
                bar.remove()
                my_memory.De_Allocate(chosenstart)
                mybars.remove(bar)

        plt.show()



def Draw(myMemory):
    global gnt
    global fig
    global textvar
    global mybars
    global mytexts
    mybars = []
    myticks = []
    global mytexts
    mytexts= []
    fig , gnt = plt.subplots(figsize=(4, 7.5))
    # change l bg color
    fig.patch.set_facecolor('black')
    # x paramters
    gnt.tick_params(axis='x', colors='white')
    gnt.tick_params(axis='y', colors='white')
    #bbox=dict(facecolor='w', alpha=0.1)
    gnt.set_ylim(myMemory.memory_units, 0)
    gnt.set_xlim(0)
    gnt.grid(True)
    gnt.set_xticks([])
    myticks.append(0)
    myticks.append(myMemory.memory_units)
    for segment in my_memory.Allocated_Memory:
        myticks.append(segment[0])
        myticks.append(segment[0]+segment[1])
       #mybars.append(gnt.bar(bottom=segment.Start ,height= segment.size , x=0, width=2, color='#FDFF7A',url="peter"))
        #mytexts.append(gnt.text(0.3,segment.Start + (segment.size/1.6) , segment.name,size=10 ))
    for segment in myMemory.Allocated_Memory:
         mybars.append(gnt.bar(bottom=segment[0],height= segment[1] , x=0, width=2, color='#FDFF7A',url="peter"))

    gnt.set_yticks(myticks)
    gnt.set_xlabel('Memory Chart \nDouble click to de-allocate', color='w')
    gnt.xaxis.set_label_position('top')
    fig.canvas.mpl_connect('button_press_event',onclick)
    plt.show()



def Redraw1():
    global mybars
    global mytexts
    global gnt
    global fig
    myticks = []
    gnt.cla()

    # change l bg color
    fig.patch.set_facecolor('black')
    # x paramters
    gnt.tick_params(axis='x', colors='white')
    gnt.tick_params(axis='y', colors='white')
    # bbox=dict(facecolor='w', alpha=0.1)
    gnt.set_ylim(my_memory.memory_units, 0)
    gnt.set_xlim(0)
    gnt.grid(True)
    gnt.set_xticks([])
    myticks.append(0)
    myticks.append(my_memory.memory_units)
    gnt.set_yticks(myticks)
    gnt.set_xlabel('Memory Chart \nDouble click to de-allocate', color='w')
    gnt.xaxis.set_label_position('top')
    fig.canvas.mpl_connect('button_press_event',onclick)



    if len(my_memory.Allocated_Memory) == 0:
        gnt.bar(bottom=0, height=my_memory.memory_units, x=0, width=2, color='w', url="peter")
        gnt.set_yticks([0, my_memory.memory_units])
        plt.show()
        return
    for segment in my_memory.Allocated_Memory:
        myticks.append(segment[0])
        myticks.append(segment[0] + segment[1])
    for i in range(len(my_memory.Allocated_Memory)):
        mybars.append(
            gnt.bar(bottom=my_memory.Allocated_Memory[i][0], height=my_memory.Allocated_Memory[i][1], x=0, width=2,
                    color='#FDFF7A', url="peter"))
        mytexts.append(gnt.text(0.3, my_memory.Allocated_Memory[i][0] + (my_memory.Allocated_Memory[i][1] / 1.6),
                                my_memory.Allocated_Memory[i][2], size=10))

    gnt.set_yticks(myticks)
    plt.show()


def mainpage():
    global root

    root = Tk()
    root.title("Memory Segmentation")
    root.geometry("300x300")

    upperframe = Frame()
    upperframe.pack()
    lowerframe = Frame()
    lowerframe.pack(side=BOTTOM)


    label_1 = Label(upperframe, text="Memory Size")
    label_1.pack(side=LEFT)
    name_1 = Entry(upperframe)
    name_1.pack(side=RIGHT)



    label_2 = Label(root, text="Number of Holes")
    label_2.pack()
    name_2 = Entry()
    name_2.pack()


    button_1 = Button(root, text="Next", command=lambda:[holes_page(name_2,name_1)] )
    button_1.pack()



def ShowType (technique):
    global root4
    if (technique.get(pname,segmentsnumber) == "First Fit"):
        First_Fit_page()

    if (technique.get(pname,segmentsnumber) == "Best Fit"):
        Best_Fit_page()


def holes_page(number_entry,memorysize):
    global root4
    global my_memory
    my_memory_size = int(memorysize.get())
    my_memory = Memory(my_memory_size)
    number_of_holes = number_entry.get()
    root.destroy()

    holes_list_entries = []

    root4 = Tk()
    root4.title("Holes")
    root4.geometry("250x500")
    label_2 = Label(root4, text="Start Address")
    label_2.grid(row=0, column=0,columnspan= 3, padx=10,pady=5)

    label_3 = Label(root4, text="Size")
    label_3.grid(row=0, column=4 ,columnspan=3,padx=10,pady=5)
    for i in range(int(number_of_holes)):
        start= Entry(root4, width=10)
        start.grid(row=i+1, column=0 ,columnspan=3,padx=10,pady=5)

        size = Entry(root4, width=10)
        size.grid(row=i+1, column=4 ,columnspan=3,padx=10,pady=5)
        holes_list_entries.append([start,size])


    #choices = ["Best Fit", "First Fit"]
    #technique = Combobox(root4, values=choices, width=10)
    #technique.set("Choose..")
    #label_4 = Label(root4, text="Select a technique", width=30)
    button_1 = Button(root4, text="Next", command=lambda:[Processes(),my_memory.initiallize_memory(holes_list_entries),Draw(my_memory)])
    #menu = Menu(root4)
    #label_4.grid(row=i+2, column=2 ,columnspan=3,padx=10,pady=5)
    #technique.grid(row=i+3, column=2 ,columnspan=3,padx=10,pady=5)
    button_1.grid(row=i+2, column=2 ,columnspan=3,padx=10,pady=5)




def Processes ():
    global root5
    root5 = Tk()
    root5.title("Settings")
    root5.geometry("300x300")
    button_1 = Button(root5, text="Add Process" ,command =lambda :[Add_Process()] )
    button_1.grid(row=0,column=0,columnspan=3,padx=10,pady=10)
    button_2 = Button(root5, text="Deallocate Process",command=lambda:[DeallocateProcess()])
    button_2.grid(row=0,column=4,columnspan=3,padx=10,pady=10)
    label=Label(root5,text="Enter a process name")
    label.grid(row=2,column=0,columnspan=3,padx=10,pady=10)
    entry=Entry(root5, width=20)
    entry.grid(row=2,column=4,columnspan=3,padx=10,pady=10)
    button_3 = Button(root5, text="Show segment table", command=lambda:[table(entry)])
    button_3.grid(row=3, column=1, columnspan=10, padx=10, pady=10)

def Add_Process():
    global root6
    root6 = Tk()
    root6.title("New Process")
    root6.geometry("300x300")
    Plabel = Label(root6, text="Process Name")
    Plabel.grid(row=0, column=0 ,columnspan=3,padx=10,pady=5)
    name = Entry(root6)
    name.grid(row=0, column=4 ,columnspan=3,padx=10,pady=5)

    label_3 = Label(root6, text="Number of Segments")
    label_3.grid(row=1, column=0 ,columnspan=3,padx=10,pady=5)
    name_3 = Entry(root6)
    name_3.grid(row=1, column=4 ,columnspan=3,padx=10,pady=5)

    choices = ["Best Fit", "First Fit"]
    technique = Combobox(root6, values=choices, width=10)
    technique.set("Choose..")
    label_4 = Label(root6, text="Select a technique", width=30)
    button_1 = Button(root6, text="Next",command=lambda: [CreateProcess(name,name_3,technique)])
    menu = Menu(root6)
    label_4.grid(row=3, column=2 ,columnspan=3,padx=10,pady=5)
    technique.grid(row=4, column=2 ,columnspan=3,padx=10,pady=5)
    button_1.grid(row=5, column=2, columnspan=3, padx=10, pady=5)


def CreateProcess (processname,numberofsegments,tech):
    global newprocessroot
    global my_memory
    ff_bf=tech.get()
    segmentlist = []

    segmentlist.clear()
    number_of_segments = int(numberofsegments.get())
    process_name = processname.get()
    root6.destroy()
    newprocessroot = Tk()
    newprocessroot.title("Details")
    newprocessroot.geometry("300x300")

    label_2 = Label(newprocessroot, text="Segment Name")
    label_2.grid(row=0, column=0, columnspan=3, padx=10, pady=5)
    label_3 = Label(newprocessroot, text="Segment Size")
    label_3.grid(row=0, column=4, columnspan=3, padx=10, pady=5)
    for i in range (number_of_segments):
        name = Entry(newprocessroot, width=18)
        name.grid(row=i + 1, column=0, columnspan=3, padx=10, pady=5)

        size=Entry(newprocessroot, width=10)
        size.grid(row=i + 1, column=5, columnspan=3, padx=10, pady=5)

        segmentlist.append([name, size])
    button = Button(newprocessroot, text="Allocate", command =lambda:[segmentchecker (process_name,segmentlist,ff_bf)])
    button.grid(column=4, columnspan=3, padx=10, pady=5)

def segmentchecker (process_name,segment_enrty_list,style):
    global list_of_process
    flag = FALSE
    x = Process(process_name)
    list_of_process.append(x)
    print(len(x.list_of_segments))

    for entry in segment_enrty_list :
        x.CreateSegment([entry[0].get(),int(entry[1].get())])

    print(len(x.list_of_segments))

    newprocessroot.destroy()
    if style =="First Fit":
        for segment in x.list_of_segments:
            segment.Set_Start(my_memory.Allocate_Memory_FF(segment.size, segment.name))
            if segment.Start == -1:
                flag = True
                break

    if style == "Best Fit":
        for segment in x.list_of_segments:
            segment.Set_Start(my_memory.Allocate_Memory_BF(segment.size, segment.name))
            if segment.Start == -1:
                flag = True
                break
    if flag == True:
        x.delete_from_memory()
        tkinter.messagebox.showerror(title="Error", message="Not Enough Space")

    Redraw1()


def DeallocateProcess():


    droot = Tk()
    droot.title("Delete Process")
    droot.geometry("300x300")
    pname = Label(droot, text="Process Name")
    pname.grid(row=0, column=0, columnspan=3, padx=10, pady=5)
    button = Button(droot, text="Deallocate",command = lambda:[Delete(name)])
    button.grid(row=1,column=4, columnspan=3, padx=10, pady=5)
    name = Entry(droot, width=20)
    name.grid(row=0, column=5, columnspan=4, padx=10, pady=5)

def Delete (name):
    global list_of_process
    pname = name.get()
    for process in list_of_process:
        if process.name == pname:
            process.delete_from_memory()
    Redraw1()

def table(name_entry):
    tableroot = Tk()
    tableroot.title("TOC")
    name = name_entry.get()
    tree = ttk.Treeview(tableroot)
    tree["columns"] = ("1", "2","3")
    tree['show'] = 'headings'
    # Assigning the heading names to the
    # respective columns
    tree.heading("1", text="Name")
    tree.heading("2", text="Base")
    tree.heading("3", text="Limit")
    for process in list_of_process:
        if process.name == name:
            display_prcess = process

    for segment in display_prcess.list_of_segments:
       tree.insert("", 'end', text="L1",values=(segment.name, segment.Start, segment.size))


    tree.pack(side=TOP, fill=X)









mainpage()

#root.configure(background='#323638')

root.mainloop()




`
