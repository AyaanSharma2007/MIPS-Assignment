def access_data_memory(address_32bit, file_name="memory_data.txt"):
    byte_address = int(address_32bit, 2)

    with open(file_name, 'r') as file:
        memory_lines = [line.strip() for line in file.readlines()]

    if memory_lines and len(memory_lines[0]) == 32:
        raise ValueError(f"{file_name} is 32bit per line. access_data_memory expects byte-addressable 8-bit memory.")

    while len(memory_lines) <= byte_address + 3:
        memory_lines.append("00000000")

    b0 = memory_lines[byte_address]
    b1 = memory_lines[byte_address + 1]
    b2 = memory_lines[byte_address + 2]
    b3 = memory_lines[byte_address + 3]

    return b0 + b1 + b2 + b3