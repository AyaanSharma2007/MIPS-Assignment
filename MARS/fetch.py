def fetch(pc, memory_file="memory_code.txt"):
    """
    Fetches a 32-bit instruction from a byte-addressable memory file.
    
    Args:
        pc (int): The current Program Counter (byte address).
        memory_file (str): Path to the text file containing 8-bit binary strings.
        
    Returns:
        str: A 32-bit binary string.
    """
    try:
        with open(memory_file, 'r') as f:
            # Read all lines and strip whitespace/newlines
            lines = [line.strip() for line in f.readlines()]
            
        # Ensure we don't go out of bounds
        if pc + 3 >= len(lines):
            print(f"Error: PC {pc} is out of memory range.")
            return None

        # Fetch 4 consecutive bytes starting from the PC
        # MIPS is typically Big-Endian: PC is the MSB (most significant byte)
        instruction_segments = lines[pc : pc + 4]
        
        # Join the 4 segments into one 32-bit string
        instruction_32 = "".join(instruction_segments)
        
        return instruction_32

    except FileNotFoundError:
        print(f"Error: {memory_file} not found.")
        return None

# Example Usage:
# current_pc = 0
# instruction = fetch(current_pc)
# print(f"Instruction at {current_pc}: {instruction}")