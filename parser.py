import random
from time import sleep

from tkinter import *
from tkinter import filedialog as fd

from parser_functions import convert_base
from parser_functions import makearray

from modbus_function import modbus_start_connection
from modbus_function import modbus_write_array

from array import array
from sys import byteorder as system_endian
from os import stat

def clear_frame():
    for widget in frame_tbl.winfo_children():
        widget.destroy()
    lbl = Label(frame_tbl, width="10", text="Номер", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=0, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Длина", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=1, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Углы", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=2, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Высота", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=3, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Добавочные", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=4, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Реал. размер", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=5, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Артикуль", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=6, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Баркод", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=7, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Цвет", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=8, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Выполнено", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=0, column=9, padx=1, pady=1)

    lbl = Label(frame_tbl, width="10", text="qty_bar", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=0, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="bar_length", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=1, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="angle_left_grad\nangle_right_grad", font=("Tahoma", 10), padx=10, pady=5,
                bg="lightgreen")
    lbl.grid(row=1, column=2, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="height_profile", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=3, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Вычисляемое", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=4, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="real_size", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=5, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="article_profile", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=6, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="bar_code\n-bar_number", font=("Tahoma", 10), padx=10, pady=5,
                bg="lightgreen")
    lbl.grid(row=1, column=7, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="bar_color", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=8, padx=1, pady=1)
    lbl = Label(frame_tbl, width="10", text="Выполнено", font=("Tahoma", 10), padx=10, pady=5, bg="lightgreen")
    lbl.grid(row=1, column=9, padx=1, pady=1)

def rewrite_table():
    clear_frame()
    row_=1
    for curw in result_arr:
        row_=row_+1
        if curw[12]=='1':
            color_="lightblue"
        else:
            color_ = "white"
        writeonerow(row_, curw, color_)

def get_changes_modbus():
    endrecords = len(result_arr)
    return random.randint(1,endrecords)


def check_changes(record_number_complete=0):
     kolrecords = len(result_arr)
     program_end=1
     for cur in result_arr:
         if cur[12]=='':
             program_end=0 # программа еще не закончена. порезаны не все записи
     if program_end==1:
         lbl_message["text"] = u"Программа завершена"
         lbl_message["bg"] = "green"
         lbl_message["width"] = "100"
         lbl_message["height"] = "3"
         return 0
     new_check = get_changes_modbus()
     if record_number_complete != new_check:
         record_number_complete = new_check
         for curw in result_arr:
             qty_num_ = int(curw[8])
             if qty_num_ == record_number_complete:
                 curw[12] = '1'
         rewrite_table()

     check_changes(record_number_complete)

def writeonerow(row_, curw, color_):
        # bar_length
        lbl = Label(frame_tbl, width="10", text=str(curw[8]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=0, padx=1, pady=1)
        lbl = Label(frame_tbl, width="10", text=str(curw[0]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=1, padx=1, pady=1)
        # angle_left_grad/#angle_right_grad
        lbl = Label(frame_tbl, width="10", text=str(curw[1] + "/" + curw[2]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=2, padx=1, pady=1)
        # height_profile
        lbl = Label(frame_tbl, width="10", text=str(curw[3]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=3, padx=1, pady=1)
        # add_right_left
        lbl = Label(frame_tbl, width="10", text=str(curw[4] + "/" + curw[5]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=4, padx=1, pady=1)
        # realsize
        lbl = Label(frame_tbl, width="10", text=str(curw[6]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=5, padx=1, pady=1)
        # article_profile
        lbl = Label(frame_tbl, width="10", text=str(curw[7]), font=("Tahoma", 10), padx=10, pady=5,
                    bg=color_)
        lbl.grid(row=row_, column=6, padx=1, pady=1)
        # barcode
        lbl = Label(frame_tbl, width="10", text=str(curw[9] + "-" + curw[10]), font=("Tahoma", 10), padx=10, pady=5,
                    bg=color_)
        lbl.grid(row=row_, column=7, padx=1, pady=1)
        # bar_color
        lbl = Label(frame_tbl, width="10", text=str(curw[11]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=8, padx=1, pady=1)
        lbl = Label(frame_tbl, width="10", text=str(curw[12]), font=("Tahoma", 10), padx=10, pady=5, bg=color_)
        lbl.grid(row=row_, column=9, padx=1, pady=1)



def startdata():
#    check_changes(0)
#    return 0
    if len(result_arr) == 0:
        lbl_message["text"] = u"Нет данных для отправки\nПодключите файл для разбора"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return 0
    connect = modbus_start_connection()
    if connect == 0:
        lbl_message["text"] = u"Ошибка соединения с ПЛК"
        lbl_message["bg"] = "red"
        lbl_message["width"] = "100"
        lbl_message["height"] = "3"
        return 0
    write_modbus = modbus_write_array(result_arr)
    if isinstance(write_modbus, str):
            lbl_message["text"] = write_modbus
            lbl_message["bg"] = "red"
            lbl_message["width"] = "100"
            lbl_message["height"] = "3"
            return 0
    row_ = 1
    for curw in result_arr:
        row_=row_+1
        curw[12]='1'
        writeonerow(row_, curw, "lightblue")
    updatescroll(len(result_arr))
    lbl_message["text"] = u"Порезка окончена"
    lbl_message["bg"] = "orange"
    lbl_message["width"] = "100"
    lbl_message["height"] = "3"



def updatescroll(i=1):
    canvas.create_window((0, 0), window=frame_tbl, anchor=NW)

    frame_tbl.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(ALL)  # Get bounding box of canvas with Buttons.
    LABEL_BG = "#ccc"  # Light grey.
    i += 2
    ROWS, COLS = i, 11  # Size of grid.
    ROWS_DISP = 12  # Number of rows to display.
    COLS_DISP = 11  # Number of columns to display.
    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.
    w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
    dw, dh = int((w / COLS) * COLS_DISP), int((h / ROWS) * ROWS_DISP)
    canvas.configure(scrollregion=bbox, width=dw, height=dh)

def writearrtogrid():
    result_arr.clear()
    add_left = '0'
    row_ = 1
    qty_bar=0
    for curw in parserresult:
        row_ += 1
        qty_bar+=1
        height_pr = curw[1]
        angleleft = curw[2]
        angleright=curw[3]
        addleft = 'error'
        addright = 'error'
        if angleright == "45":
            addright = height_pr
        if angleright == "90":
            addright = '0'
        if angleleft == "45":
            addleft = height_pr
        if angleleft == "90":
            addleft = '0'

        if addleft=='error' or addright=='error':
            realsize='error'
        else:
            realsize=str(int(curw[0]) - int(addleft) - int(addright))
        result_row=[]
        result_row.clear()
        result_row.append(curw[0])#bar_length
        result_row.append(curw[2])#angle_left_grad
        result_row.append(curw[3])#angle_right_grad
        result_row.append(height_pr)#height_profile
        result_row.append(addleft)#addleft
        result_row.append(addright)#addright
        result_row.append(realsize)#realsize
        result_row.append(curw[8])#article_profile
        result_row.append(str(qty_bar))#qty_bar
        result_row.append(curw[6])#bar_code
        result_row.append(curw[7])#bar_number
        result_row.append(curw[5])#bar_color
        result_row.append('')
        result_arr.append(result_row)
        writeonerow(row_, result_row, "white")
    updatescroll(len(result_arr))



def importdata():
    clear_frame()
    hex_arr=[]
    str_text = ''
    hex_arr.clear()
    result_arr.clear()
    parserresult.clear()
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

    writearrtogrid()


root = Tk()
parserresult = []
parserresult.clear()
result_arr = []
result_arr.clear()
result_row = []
result_row.clear()
lbl_message = Label(root, text="", font=("Tahoma", 12), width="0", height="0", bg="white")
lbl_message.grid(row=1, columnspan=4)
lbl_message["text"] = u"Подключите файл для разбора"
lbl_message["bg"] = "lightgreen"
lbl_message["width"] = "100"
lbl_message["height"] = "3"

but_import = Button(root,
           text=u"Импорт данных из файла",
           width = 30, height = 1,
           font=("Tahoma", 12),
           bg="orange", command=importdata
                  )
but_import.grid(row=2,column=1, padx=5, pady=30)

but_start = Button(root,
           text= u"Послать данные на ПЛК",
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

clear_frame()

updatescroll(1)
root.title(u"Раскрой пилы")
root.geometry('1024x768')
root.configure(bg="grey")
root.mainloop()