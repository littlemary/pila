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


