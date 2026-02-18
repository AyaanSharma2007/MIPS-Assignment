def write_data_memory(address, write_data, file_name="Data.txt"):
    line_number = int(address, 2)
    with open(file_name, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # 2. EXTEND (Fix the "Out of Bounds" bug)
    # If we want index 5, length must be at least 6.
    while len(lines) <= line_number:
        lines.append("00000000000000000000000000000000") # Fill gaps with 0s

    # 3. WRITE (Direct access, no loop needed)
    lines[line_number] = write_data
    
    # 4. SAVE
    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line + "\n")
            
    print(f"Successfully wrote data to Address {line_number}")