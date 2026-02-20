# Create a lookup list mapping index 0-31 to the register names from your table
REGISTER_NAMES = [
    "$0", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
    "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
    "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
    "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
]

def decode_instruction(instruction):
    # Extract opcode (bits 31-26)
    opcode = (instruction >> 26) & 0x3F
    
    decoded = {
        "hex": hex(instruction),
        "opcode": hex(opcode),
    }

    if opcode == 0:
        # R-TYPE
        decoded["type"] = "R-Type"
        
        # Extract the integer value, then look up the string name
        rs_num = (instruction >> 21) & 0x1F
        rt_num = (instruction >> 16) & 0x1F
        rd_num = (instruction >> 11) & 0x1F
        
        decoded["rs"] = rs_num
        decoded["rt"] = rt_num
        decoded["rd"] = rd_num
        
        decoded["shamt"] = (instruction >> 6) & 0x1F
        decoded["funct"] = hex(instruction & 0x3F)
        
    elif opcode == 0x02 or opcode == 0x03:
        # J-TYPE
        decoded["type"] = "J-Type"
        decoded["address"] = hex(instruction & 0x03FFFFFF)
        
    else:
        # I-TYPE
        decoded["type"] = "I-Type"
        
        # Extract the integer value, then look up the string name
        rs_num = (instruction >> 21) & 0x1F
        rt_num = (instruction >> 16) & 0x1F
        
        decoded["rs"] = rs_num
        decoded["rt"] = rt_num
        
        # Handle signed immediate
        imm = instruction & 0xFFFF
        if imm & 0x8000:
            imm -= 0x10000
        decoded["immediate"] = imm

    return decoded