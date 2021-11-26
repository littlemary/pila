from datetime import *
from tkinter import *
from tkinter import filedialog as fd
from array import array
from sys import byteorder as system_endian
from os import stat

def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    n = int(num, from_base) if isinstance(num, str) else num
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while n > 0:
        n,m = divmod(n, to_base)
        res += alphabet[m]
    return res[::-1]

def makearray(textstr, hex_arr):
    result=['', '', '', '', '', '', '', '', '']
    if (len(textstr)<108):
        return 0
    #bar_length
    mystr = hex_arr[5] + hex_arr[6]
    mystrdecode = convert_base(mystr, 10, 16)
    #mystrdecode = mystrdecode[:-1]
    result[0] = mystrdecode

    #angle_left_grad
    mystr = hex_arr[8] + hex_arr[9]
    mystrdecode = convert_base(mystr, 10, 16)
    result[1] = mystrdecode

    #angle_right_grad
    mystr = hex_arr[10] + hex_arr[11]
    mystrdecode = convert_base(mystr, 10, 16)
    mystrdecode = mystrdecode[:-1]
    result[2] = mystrdecode

    #height_profile
    mystr = hex_arr[12] + hex_arr[13]
    mystrdecode = convert_base(mystr, 10, 16)
    mystrdecode = mystrdecode[:-1]
    result[3] = mystrdecode

    # qty_bar
    mystr=hex_arr[15]
    mystrdecode = convert_base(mystr, 10, 18)
    result[4] = mystrdecode

    # bar_color
    mystrdecode = textstr[52:68]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[5] = data1.decode('utf-8')

    # bar_code
    mystrdecode = textstr[68:80]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[6] = data1.decode('utf-8')

    # bar_number
    mystrdecode = textstr[82:84]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[7] = data1.decode('utf-8')

    mystrdecode = textstr[84:96]
    data = bytes(mystrdecode, "utf-8")
    data1 = bytes.fromhex(data.decode("ascii"))
    result[8] = data1.decode('utf-8')
    return result
def startdata():
    return
def updatescroll(i=1):
    canvas.create_window((0, 0), window=frame_tbl, anchor=NW)

    frame_tbl.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(ALL)  # Get bounding box of canvas with Buttons.
    # print('canvas.bbox(tk.ALL): {}'.format(bbox))
    LABEL_BG = "#ccc"  # Light grey.
    ROWS, COLS = i, 8  # Size of grid.
    ROWS_DISP = 7  # Number of rows to display.
    COLS_DISP = 8  # Number of columns to display.
    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.
    w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
    dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
    canvas.configure(scrollregion=bbox, width=dw, height=dh)

def writearrtogrid(parserresult):
    add_left='0'

    row_=0
    for curw in parserresult:
        row_=row_+1
        height_pr=curw[1]
        angleright=curw[2]
        addleft='error'
        addright='error'
        if angleright == "45":
            addleft=height_pr
            addright = height_pr
        if angleright == "90":
            addleft='0'
            addright = '0'
        if addleft=='error' or addright=='error':
            realsize='error'
        else:
            realsize=str(int(curw[0]) - int(addleft) - int(addright))

        # bar_length
        lbl = Label(frame_tbl, width="10", text=str(curw[0]), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=0, padx=1, pady=1)
        # angle_left_grad/#angle_right_grad
        lbl = Label(frame_tbl, width="10", text=str(curw[2]+"/"+curw[3]), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=1, padx=1, pady=1)
        # height_profile
        lbl = Label(frame_tbl, width="10", text=str(curw[1]), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=2, padx=1, pady=1)
        # add_right_left
        lbl = Label(frame_tbl, width="10", text=str(addright+"/"+addleft), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=3, padx=1, pady=1)
        # realsize
        lbl = Label(frame_tbl, width="10", text=str(realsize), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=4, padx=1, pady=1)
        # article_profile-qty_bar
        lbl = Label(frame_tbl, width="10", text=str(curw[8] + "-" + curw[4]  ), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=5, padx=1, pady=1)
        # barcode
        lbl = Label(frame_tbl, width="10", text=str(curw[6]+"-"+curw[7]), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=6, padx=1, pady=1)
        # bar_color
        lbl = Label(frame_tbl, width="10", text=str(curw[5]), font=("Tahoma", 10), padx=10, pady=5, bg="white")
        lbl.grid(row=row_, column=7, padx=1, pady=1)

        result_arr[0] = curw[0]#bar_length
        result_arr[1] = curw[2]#angle_left_grad
        result_arr[2] = curw[3]#angle_right_grad
        result_arr[3] = height_pr#height_profile
        result_arr[4] = addleft#addleft
        result_arr[5] = addright#addright
        result_arr[6] = realsize#realsize
        result_arr[7] = curw[8]#article_profile
        result_arr[8] = curw[4]#qty_bar
        result_arr[9] = curw[6]#bar_code
        result_arr[10] = curw[7]#bar_number
        result_arr[11] = curw[5]#bar_color
    updatescroll(len(parserresult))



def importdata():
    updatescroll(1)
    hex_arr=[]
    str_text = ''


    filenamexml = fd.askopenfilename(filetypes=(("PRG files", "*.prg"), ("all files", " *.*")))

    if filenamexml:
        try:
            lbl_message["text"] = u"Подождите... Идет импортирование данных"
            lbl_message["bg"] = "lightgreen"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"

            with open(filenamexml, "rb") as f:
                # Read the whole file at once
                for i in f.read():
                    a = ord(chr(i))
                    a1 = "{:02x}".format(a)
                    hex_arr.append(a1)
        except:
            lbl_message["text"] = u"Не могу открыть файл"
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return
    else:
        lbl_message["text"] = u"Не могу открыть файл"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return
    lbl_message["text"] = u"Данные загружены"
    lbl_message["bg"] = "lightgreen"
    lbl_message["width"] = "100"
    lbl_message["height"] = "3"

    for cur in range(0, len(hex_arr), 54):
        start=cur
        end=cur+54
        if end>len(hex_arr):
            end=len(hex_arr)
        str_text = ''.join(hex_arr[start:end])
        res = makearray(str_text, hex_arr[start:end])
        if res != 0:
            parserresult.append(res)


    writearrtogrid(parserresult)


root = Tk()
parserresult = []
result_arr = ['','','','','','','','','','','','']
lbl_message = Label(root, text="", font=("Tahoma", 12), width="0", height="0", bg="white")
lbl_message.grid(row=1, columnspan=4)
lbl_message["text"] = u"Подключите файл для разбора"
lbl_message["bg"] = "lightgreen"
lbl_message["width"] = "100"
lbl_message["height"] = "3"

but_import = Button(root,
           text= u"Импорт данных из файла",
           width=30, height=1,
           font=("Tahoma", 12),
           bg="orange", command=importdata
                  )
but_import.grid(row=2,column=1, padx=5, pady=30)

but_start = Button(root,
           text= u"СТАРТ",
           width=30, height=1,
           font=("Tahoma", 12),
           bg="green", command=startdata
                  )
but_start.grid(row=2,column=2, padx=5, pady=30)

mycolor1 = '#eeeeee'

frame_ = Frame(root, bg=mycolor1, borderwidth=25)
frame_.grid(row=3, column=0, columnspan="4")
frame2_c = Frame(frame_)
frame2_c.grid(row=8, columnspan="3", sticky=NW)
# Add a canvas in that frame.
canvas = Canvas(frame2_c, bg="grey")
canvas.grid(row=0, column=0)

# Create a vertical scrollbar linked to the canvas.
vsbar = Scrollbar(frame2_c, orient=VERTICAL, command=canvas.yview)
vsbar.grid(row=0, column=1, sticky=NS)
canvas.configure(yscrollcommand=vsbar.set)

# Create a horizontal scrollbar linked to the canvas.
hsbar = Scrollbar(frame2_c, orient=HORIZONTAL, command=canvas.xview)
hsbar.grid(row=1, column=0, sticky=EW)
canvas.configure(xscrollcommand=hsbar.set)

# Create a frame on the canvas to contain the buttons.
frame_tbl = Frame(canvas, bg="grey", bd=2)

lbl = Label(frame_tbl, width="10", text="Длина", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=0, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Углы", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=1, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Высота", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=2, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Добавочные", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=3, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Реал. размер", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=4, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Артикуль", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=5, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Баркод", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=6, padx=1, pady=1)
lbl = Label(frame_tbl, width="10", text="Цвет", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
lbl.grid(row=0, column=7, padx=1, pady=1)
updatescroll(1)

root.title(u"Раскрой пилы")
root.geometry('1024x768')
root.configure(bg="grey")
root.mainloop()