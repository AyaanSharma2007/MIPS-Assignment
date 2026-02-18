from ALUandSignExtend import ALU, sign_extend_16_to_32

def execute_stage(decoded_info, rs_val_bin, rt_val_bin, pc_plus_4_int):
    """
    EX Stage: Processes instruction and generates control signals for MEM and WB.
    """
    opcode = int(decoded_info["opcode"], 16)
    
    # Extract funct code safely (only exists for R-Type)
    funct = int(decoded_info.get("funct", "0"), 16) if decoded_info.get("funct") else 0
    
    # Default Control Signals (Sab Off)
    ex_result = {
        "alu_result_bin": "00000000000000000000000000000000",
        "write_dest_reg": None, 
        "reg_write": False,     
        "mem_read": False,      
        "mem_write": False,
        "mem_to_reg": False,
        "update_pc": False,     # Jump/Branch handle karne ke liye
        "new_pc_int": 0         # Naya PC address
    }

    # ==========================================
    # 1. R-TYPE INSTRUCTIONS (Opcode == 0x00)
    # ==========================================
    if opcode == 0x00:
        ex_result["write_dest_reg"] = decoded_info["rd"]
        ex_result["reg_write"] = True # Mostly R-types write to a register
        
        # ADD / MOVE (funct: 0x20)
        if funct == 0x20:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "010")
            
        # SLL - Shift Left Logical (funct: 0x00)
        elif funct == 0x00:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int << shamt) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            
        # SRA - Shift Right Arithmetic (funct: 0x03)
        elif funct == 0x03:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            # Handle Python's sign bit correctly for 32-bit
            if rt_int & 0x80000000: 
                res = (rt_int >> shamt) | (((1 << shamt) - 1) << (32 - shamt))
            else:
                res = rt_int >> shamt
            ex_result["alu_result_bin"] = f"{res & 0xFFFFFFFF:032b}"
            
        # SLT - Set Less Than (funct: 0x2A) -> Used in blt/bgt
        elif funct == 0x2A:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "100")
            
        # JR - Jump Register (funct: 0x08)
        elif funct == 0x08:
            ex_result["update_pc"] = True
            ex_result["new_pc_int"] = int(rs_val_bin, 2)
            ex_result["reg_write"] = False # JR doesn't write to register

    # ==========================================
    # 2. J-TYPE INSTRUCTIONS
    # ==========================================
    # J - Jump (Opcode: 0x02)
    elif opcode == 0x02:
        ex_result["update_pc"] = True
        ex_result["new_pc_int"] = int(decoded_info["address"], 16) * 4

    # JAL - Jump And Link (Opcode: 0x03)
    elif opcode == 0x03:
        ex_result["update_pc"] = True
        ex_result["new_pc_int"] = int(decoded_info["address"], 16) * 4
        ex_result["write_dest_reg"] = 31 # Save return address in $ra (Register 31)
        ex_result["reg_write"] = True
        ex_result["alu_result_bin"] = f"{pc_plus_4_int:032b}" # Save PC+4 to $ra

    # ==========================================
    # 3. I-TYPE INSTRUCTIONS
    # ==========================================
    else:
        imm = decoded_info["immediate"]
        imm_16_bin = f"{imm & 0xFFFF:016b}"
        extended_imm_bin = sign_extend_16_to_32(imm_16_bin)
        
        # ADDI / SUBI / LI (Opcode: 0x08)
        if opcode == 0x08:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010")
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        # LW - Load Word (Opcode: 0x23)
        elif opcode == 0x23:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010") # Calculate memory address
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True
            ex_result["mem_read"] = True
            ex_result["mem_to_reg"] = True

        # BEQ - Branch on Equal (Opcode: 0x04)
        elif opcode == 0x04:
            alu_res = ALU(rs_val_bin, rt_val_bin, "011") # Subtract Rs and Rt
            if int(alu_res, 2) == 0:                     # If Result == 0, they are equal
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)

        # BNE - Branch Not Equal (Opcode: 0x05) -> Used internally by bgt/blt
        elif opcode == 0x05:
            alu_res = ALU(rs_val_bin, rt_val_bin, "011") # Subtract
            if int(alu_res, 2) != 0:                     # If Result != 0, they are NOT equal
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)
                
        # LUI - Load Upper Immediate (Opcode: 0x0F) -> Used by 'la'
        elif opcode == 0x0F:
            res = (imm << 16) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        # ORI - OR Immediate (Opcode: 0x0D) -> Used by 'la'
        elif opcode == 0x0D:
            rs_int = int(rs_val_bin, 2)
            res = (rs_int | (imm & 0xFFFF)) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

    return ex_result