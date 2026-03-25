def sign_extend_16_to_32(binary_str):
    if len(binary_str) != 16:
        return None
    #basically concatinating first bit of string 16 times
    return binary_str[0] * 16 + binary_str

# 000 -> AND
# 001 -> OR
# 010 -> ADD
# 011 -> SUB
# 100 -> Less Than

def ALU(operand1_bin, operand2_bin, control_line):
    try:
        val1 = int(operand1_bin, 2)
        val2 = int(operand2_bin, 2)
    except ValueError:
        return None
    if control_line == "000":
        result = val1 & val2
    elif control_line == "001":
        result = val1 | val2
    elif control_line == "010":
        result = val1 + val2
    elif control_line == "011":
        result = val1 - val2
    elif control_line == "100":
        if (val1 >> 31) == 1:          
            s_val1 = val1 - (1 << 32)  
        else:
            s_val1 = val1           
            
        if (val2 >> 31) == 1:
            s_val2 = val2 - (1 << 32)
        else:
            s_val2 = val2
        if s_val1 < s_val2:
            result = 1
        else:
            result = 0
    else:
        return None
    return f'{result & 0xFFFFFFFF:032b}'