def fetch(pc_binary, memory_file="memory_code.txt"):
    if not (type(pc_binary)==str) or len(pc_binary) != 32:
        return None
    try:
        pc_int = int(pc_binary, 2)
    except ValueError:
        return None
    if pc_int % 4 != 0:
        return None
    try:
        with open(memory_file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            
        if pc_int + 3 >= len(lines):
            return None
        instruction_segments = lines[pc_int : pc_int + 4]
        if len(instruction_segments) != 4:
            return None
        instruction_32 = "".join(instruction_segments)
        if len(instruction_32) != 32:
            return None
        return instruction_32
    except Exception:
        return None
