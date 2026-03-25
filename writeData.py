def write_data_memory(address, write_data, file_name="memory_data.txt"):
    byte_address = int(address, 2)

    with open(file_name, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    while len(lines) <= byte_address + 3:
        lines.append("00000000")

    lines[byte_address]     = write_data[0:8]
    lines[byte_address + 1] = write_data[8:16]
    lines[byte_address + 2] = write_data[16:24]
    lines[byte_address + 3] = write_data[24:32]

    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line + "\n")