def decode_instruction(instruction_str):
    instr = int(instruction_str, 2)
    opcode = (instr >> 26) & 0x3F
    decoded = {
        "hex": hex(instr),
        "opcode": hex(opcode),
    }
    if opcode == 0:
        decoded["type"] = "R-Type"
        decoded["rs"] = (instr >> 21) & 0x1F
        decoded["rt"] = (instr >> 16) & 0x1F
        decoded["rd"] = (instr >> 11) & 0x1F
        decoded["shamt"] = (instr >> 6) & 0x1F
        decoded["funct"] = hex(instr & 0x3F)
    elif opcode in (0x02, 0x03):
        decoded["type"] = "J-Type"
        decoded["address"] = hex(instr & 0x03FFFFFF)
    else:
        decoded["type"] = "I-Type"
        decoded["rs"] = (instr >> 21) & 0x1F
        decoded["rt"] = (instr >> 16) & 0x1F
        imm = instr & 0xFFFF
        if imm & 0x8000:
            imm -= 0x10000
        decoded["immediate"] = imm
    return decoded