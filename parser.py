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

def main():
    hex_arr=[]
    str_text = ''
    parserresult=[]

    filenamexml = fd.askopenfilename(filetypes=(("PRG files", "*.prg"), ("all files", " *.*")))
    with open(filenamexml, "rb") as f:
        # Read the whole file at once
        for i in f.read():
            a=ord(chr(i))
            a1="{:02x}".format(a)
            hex_arr.append(a1)


    for cur in range(0, len(hex_arr), 54):
        start=cur
        end=cur+54
        if end>len(hex_arr):
            end=len(hex_arr)
        str_text = ''.join(hex_arr[start:end])
        res = makearray(str_text, hex_arr[start:end])
        if res != 0:
            parserresult.append(res)
    fw = open('text.csv', 'w')
    result_arr = ['bar_length', 'angle_left_grad', 'angle_right_grad', 'height_profile', 'bar_code', 'bar_number', 'article_profile', 'qty_bar', 'qty_cut', 'marker_end_cut', 'bar_color', 'add_left_head', 'add_right_head', 'real_size']
    result_str = ";".join(result_arr)
    add_left='0'
    fw.write(result_str + '\n')
    for curw in parserresult:
        result_arr[0] = curw[0]#bar_length
        result_arr[1] = curw[2]#angle_left_grad
        result_arr[2] = curw[3]#angle_right_grad
        result_arr[3] = curw[1]#height_profile
        result_arr[4] = curw[6]#bar_code
        result_arr[5] = curw[7]#bar_number
        result_arr[6] = curw[8]#article_profile
        result_arr[7] = curw[4]#qty_bar
        result_arr[8] = '0'#qty_cut
        result_arr[9] = '0'#marker_end_cut
        result_arr[10] = curw[5]#bar_color
        addleft='error'
        if result_arr[1] == "45":
            addleft=result_arr[3]
        if result_arr[1] == "90":
            addleft='0'
        addright = 'error'
        if result_arr[1] == "45":
            addright = result_arr[3]
        if result_arr[1] == "90":
            addright = '0'

        result_arr[11] = addleft
        result_arr[12] = addright

        if addleft=='error' or addright=='error':
            realsize='error'
        else:
            realsize=str(int(result_arr[0]) - int(addleft) - int(addright))
        result_arr[13] = realsize

        curwstr=";".join(result_arr)
        print(curwstr)
        fw.write(curwstr+'\n')


main()