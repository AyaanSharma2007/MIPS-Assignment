def access_data_memory(address_32bit, file_name="Data.txt"):
    # Divide by 4 to convert MIPS byte address to Python line number
    line_number = int(address_32bit, 2) // 4 
    
    with open(file_name, 'r') as file:
        memory_lines = file.readlines()
        
    if line_number < len(memory_lines):
        fetched_data = memory_lines[line_number].strip()
        return fetched_data
    else:
        return "00000000000000000000000000000000"