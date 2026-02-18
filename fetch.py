def fetch(pc_binary, memory_file="memory_code.txt"):
    """
    Fetches a 32-bit instruction from a byte-addressable memory file.
    Takes a 32-bit binary string as PC, converts it internally, and returns the instruction.
    """
    # EDGE CASE 1: Check if PC is exactly a 32-bit string
    if not isinstance(pc_binary, str) or len(pc_binary) != 32:
        return None
        
    try:
        # Internally convert 32-bit binary string PC to integer
        pc_int = int(pc_binary, 2)
    except ValueError:
        # EDGE CASE 2: Invalid binary format (e.g., contains characters other than 0 and 1)
        return None

    # EDGE CASE 3: Word alignment check (In MIPS, PC must be a multiple of 4)
    if pc_int % 4 != 0:
        return None

    try:
        with open(memory_file, 'r') as f:
            # Read lines and remove whitespace/newlines
            lines = [line.strip() for line in f.readlines()]
            
        # EDGE CASE 4: Out of bounds check (need at least 4 bytes starting from pc_int)
        if pc_int + 3 >= len(lines):
            return None

        # Fetch 4 consecutive bytes
        instruction_segments = lines[pc_int : pc_int + 4]
        
        # EDGE CASE 5: Ensure we actually grabbed 4 valid segments
        if len(instruction_segments) != 4:
            return None

        # Join the 4 segments into one 32-bit string
        instruction_32 = "".join(instruction_segments)
        
        # EDGE CASE 6: Final check to ensure the fetched instruction is exactly 32 bits
        if len(instruction_32) != 32:
            return None
            
        return instruction_32

    except Exception:
        # Handles FileNotFoundError and any other unexpected read errors silently
        return None

# --- Example Usage (Just for you to test, tum isko apne main loop me use kar lena) ---
# dummy_pc = "00000000000000000000000000000100"  # Binary for 4
# instruction = fetch(dummy_pc)
