def write_data_memory(address, write_data, file_name="Data.txt"):
    # FIX: Divide by 4 to convert MIPS byte address to Python line number.
    # This aligns the write operation with how access_data_memory.py reads it.
    line_number = int(address, 2) // 4
    
    with open(file_name, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # EXTEND: Dynamically grow the memory if we write to a new, higher address
    while len(lines) <= line_number:
        lines.append("00000000000000000000000000000000") # Fill gaps with 0s

    # WRITE: Update the specific line with our new 32-bit string
    lines[line_number] = write_data
    
    # SAVE: Write everything back to the file
    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line + "\n")