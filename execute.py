from ALUandSignExtend import ALU, sign_extend_16_to_32

def execute_stage(decoded_info, rs_val_bin, rt_val_bin, pc_plus_4_int):
    opcode = int(decoded_info["opcode"], 16)
    
    funct = int(decoded_info.get("funct", "0"), 16) if decoded_info.get("funct") else 0 #give me the value of this key, if it exists
    
    ex_result = {
        "alu_result_bin": "00000000000000000000000000000000",
        "store_data_bin": "00000000000000000000000000000000",
        "write_dest_reg": None, 
        "reg_write": False,     
        "mem_read": False,      
        "mem_write": False,
        "mem_to_reg": False,
        "update_pc": False,     
        "new_pc_int": 0         
    }

    if opcode == 0x00: #for R-type
        ex_result["write_dest_reg"] = decoded_info["rd"]
        ex_result["reg_write"] = True 
        
        if funct == 0x20: #for add
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "010")

        elif funct == 0x22: #for sub
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "011") 
            
        elif funct == 0x00: #for shift left
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int << shamt) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"

        elif funct == 0x02: #for shift right logical
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int & 0xFFFFFFFF) >> shamt
            ex_result["alu_result_bin"] = f"{res:032b}"
            
        elif funct == 0x03: #for shift right arithmetic
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            if rt_int & 0x80000000: #when rt_int is negative
                res = (rt_int >> shamt) | (((1 << shamt) - 1) << (32 - shamt))
            else:
                res = rt_int >> shamt
            ex_result["alu_result_bin"] = f"{res & 0xFFFFFFFF:032b}"
            
        elif funct == 0x2A: #for set less than
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "100")
            
        elif funct == 0x08: #for jump register
            ex_result["update_pc"] = True
            ex_result["new_pc_int"] = int(rs_val_bin, 2)
            ex_result["reg_write"] = False

        elif funct == 0x0C: #for syscall
            ex_result["reg_write"] = False

    elif opcode == 0x02: #for jump
        ex_result["update_pc"] = True
        jump_target_addr = int(decoded_info["address"], 16)
        upper_pc_bits = pc_plus_4_int & 0xF0000000
        lower_jump_bits = jump_target_addr * 4
        ex_result["new_pc_int"] = upper_pc_bits | lower_jump_bits

    elif opcode == 0x03: #for jump and link
        ex_result["update_pc"] = True
        jump_target_addr = int(decoded_info["address"], 16)
        upper_pc_bits = pc_plus_4_int & 0xF0000000
        lower_jump_bits = jump_target_addr * 4
        ex_result["new_pc_int"] = upper_pc_bits | lower_jump_bits

        ex_result["write_dest_reg"] = 31 #this is register 31 i.e. $ra
        ex_result["reg_write"] = True
        ex_result["alu_result_bin"] = f"{pc_plus_4_int:032b}"
        #after using jal we jr $ra i.e. jump register

    else: #for I-type
        imm = decoded_info["immediate"]
        imm_16_bin = f"{imm & 0xFFFF:016b}"
        extended_imm_bin = sign_extend_16_to_32(imm_16_bin)

        #010 performs additon in ALU

        if opcode == 0x08: #for addi
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010")
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        elif opcode == 0x23: #for lw
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010") 
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True
            ex_result["mem_read"] = True
            ex_result["mem_to_reg"] = True

        elif opcode == 0x2B: #for sw
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010") 
            ex_result["store_data_bin"] = rt_val_bin 
            ex_result["reg_write"] = False 
            ex_result["mem_write"] = True

        elif opcode == 0x04: #for beq i.e. branch if equal
            if imm == -1 and rs_val_bin == rt_val_bin: 
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = -4 
                return ex_result

            alu_res = ALU(rs_val_bin, rt_val_bin, "011") #normal case
            if int(alu_res, 2) == 0:                     
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)

        elif opcode == 0x05: #for branch if not equal i.e. bne
            if imm == -1 and rs_val_bin != rt_val_bin:
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = -4 
                return ex_result

            alu_res = ALU(rs_val_bin, rt_val_bin, "011") #normal case
            if int(alu_res, 2) != 0:                     
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)
                
        elif opcode == 0x0F: #for load upper immediate i.e. lui
            res = (imm << 16) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        elif opcode == 0x0D: #for ori i.e. or immediate
            rs_int = int(rs_val_bin, 2)
            res = (rs_int | (imm & 0xFFFF)) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

    return ex_result