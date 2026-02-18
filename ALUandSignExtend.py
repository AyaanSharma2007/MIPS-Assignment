def sign_extend_16_to_32(binary_str):
    if len(binary_str) != 16:
        return "Error: Input must be exactly 16 bits."
    msb = binary_str[0]
    prefix = msb * 16
    return prefix + binary_str

def ALU(operand1_bin, operand2_bin, control_line):
    # 1. Convert the 32-bit binary strings to integers
    # We use int(x, 2) to treat them as numbers.
    val1 = int(operand1_bin, 2)
    val2 = int(operand2_bin, 2)
    
    result = 0
    
    # 2. Perform the operation based on the Control Line
    if control_line == "000":   # AND
        result = val1 & val2
        
    elif control_line == "001": # OR
        result = val1 | val2
        
    elif control_line == "010": # ADD
        result = val1 + val2
        
    elif control_line == "011": # SUB
        result = val1 - val2
        
    elif control_line == "100": # SLT (Set on Less Than)
        # Note: In real CPUs (like MIPS), SLT usually performs a SIGNED comparison.
        # We convert our unsigned integers to signed 32-bit values for accurate comparison.
        
        # Helper to treat number as signed 32-bit
        s_val1 = val1 - (1 << 32) if (val1 >> 31) else val1
        s_val2 = val2 - (1 << 32) if (val2 >> 31) else val2
        
        if s_val1 < s_val2:
            result = 1
        else:
            result = 0
            
    else:
        return "Error: Invalid Control Line"

    # 3. Format the result back to 32-bit binary
    # ' & 0xFFFFFFFF' ensures we simulate 32-bit overflow (dropping extra bits).
    # ':032b' formats it as a binary string padded with zeros to length 32.
    return f'{result & 0xFFFFFFFF:032b}'
