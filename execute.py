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
        "store_data_bin": "00000000000000000000000000000000", # Added for SW safety
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

        # SUB - Subtract (funct: 0x22) -> ADDED THIS FOR YOU
        elif funct == 0x22:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "011") 
            
        # SLL - Shift Left Logical (funct: 0x00)
        elif funct == 0x00:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int << shamt) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
        # SRL - Shift Right Logical (funct: 0x02)
        elif funct == 0x02:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int & 0xFFFFFFFF) >> shamt
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
        # JR - Jump Register (funct: 0x08)
        elif funct == 0x08:
            ex_result["update_pc"] = True
            ex_result["new_pc_int"] = int(rs_val_bin, 2)
            ex_result["reg_write"] = False # JR doesn't write to register
            
        # SYSCALL (funct: 0x0C)
        elif funct == 0x0C:
            # We don't do anything in the EX stage for syscall since 
            # processor.py intercepts it, but we MUST ensure it doesn't write!
            ex_result["reg_write"] = False

    # ==========================================
    # 2. J-TYPE INSTRUCTIONS
    # ==========================================
    # J - Jump (Opcode: 0x02)
    elif opcode == 0x02:
        ex_result["update_pc"] = True
        jump_target_addr = int(decoded_info["address"], 16)
        upper_pc_bits = pc_plus_4_int & 0xF0000000
        lower_jump_bits = jump_target_addr * 4
        ex_result["new_pc_int"] = upper_pc_bits | lower_jump_bits

    # JAL - Jump And Link (Opcode: 0x03)
    elif opcode == 0x03:
        ex_result["update_pc"] = True
        jump_target_addr = int(decoded_info["address"], 16)
        upper_pc_bits = pc_plus_4_int & 0xF0000000
        lower_jump_bits = jump_target_addr * 4
        ex_result["new_pc_int"] = upper_pc_bits | lower_jump_bits

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

        # SW - Store Word (Opcode: 0x2B) -> ADDED THIS FOR YOU
        elif opcode == 0x2B:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010") # Calculate memory address
            ex_result["store_data_bin"] = rt_val_bin # The data we want to write into memory
            ex_result["reg_write"] = False # We write to memory, NOT a register
            ex_result["mem_write"] = True

        # BEQ - Branch on Equal (Opcode: 0x04)
        elif opcode == 0x04:
            if imm == -1 and rs_val_bin == rt_val_bin:
                print("INFO: Detected halt loop (beq $rs, $rs, -1). Halting.")
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = -4 
                return ex_result

            alu_res = ALU(rs_val_bin, rt_val_bin, "011") # Subtract Rs and Rt
            if int(alu_res, 2) == 0:                     # If Result == 0, they are equal
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)

        # BNE - Branch Not Equal (Opcode: 0x05)
        elif opcode == 0x05:
            if imm == -1 and rs_val_bin != rt_val_bin:
                print("INFO: Detected halt loop (bne $rs, $rt, -1). Halting.")
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = -4 
                return ex_result

            alu_res = ALU(rs_val_bin, rt_val_bin, "011") # Subtract
            if int(alu_res, 2) != 0:                     # If Result != 0, they are NOT equal
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)
                
        # LUI - Load Upper Immediate (Opcode: 0x0F)
        elif opcode == 0x0F:
            res = (imm << 16) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        # ORI - OR Immediate (Opcode: 0x0D)
        elif opcode == 0x0D:
            rs_int = int(rs_val_bin, 2)
            res = (rs_int | (imm & 0xFFFF)) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

    return ex_result