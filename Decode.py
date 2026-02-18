#returns a dictionary containing info about the instruction

def decode_instruction(instruction):
    # Extract opcode (bits 31-26)
    opcode = (instruction >> 26) & 0x3F
    
    # Initialize the result dictionary
    decoded = {
        "hex": hex(instruction),
        "opcode": hex(opcode),
    }

    if opcode == 0:
        # R-TYPE: Opcode is 0, actual operation is in 'funct'
        decoded["type"] = "R-Type"
        decoded["rs"] = (instruction >> 21) & 0x1F
        decoded["rt"] = (instruction >> 16) & 0x1F
        decoded["rd"] = (instruction >> 11) & 0x1F
        decoded["shamt"] = (instruction >> 6) & 0x1F
        decoded["funct"] = hex(instruction & 0x3F)
        
    elif opcode == 0x02 or opcode == 0x03:
        # J-TYPE: Jump or Jump and Link
        decoded["type"] = "J-Type"
        decoded["address"] = hex(instruction & 0x03FFFFFF)
        
    else:
        # I-TYPE: Everything else (addi, lw, sw, beq, etc.)
        decoded["type"] = "I-Type"
        decoded["rs"] = (instruction >> 21) & 0x1F
        decoded["rt"] = (instruction >> 16) & 0x1F
        
        # Handle signed immediate (16-bit sign extension)
        imm = instruction & 0xFFFF
        if imm & 0x8000:  # If the 15th bit is 1, it's negative
            imm -= 0x10000
        decoded["immediate"] = imm

    return decoded

# Example usage: ADD $t0, $s1, $s2 -> 0x02324020
# instr = 10001100100100000000100000
# info = decode_mips(instr)

# for key, value in info.items():
#     print(f"{key.capitalize()}: {value}")