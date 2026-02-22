from ALUandSignExtend import ALU, sign_extend_16_to_32

def execute_stage(decoded_info, rs_val_bin, rt_val_bin, pc_plus_4_int):
    opcode = int(decoded_info["opcode"], 16)
    
    funct = int(decoded_info.get("funct", "0"), 16) if decoded_info.get("funct") else 0
    
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

    if opcode == 0x00:
        ex_result["write_dest_reg"] = decoded_info["rd"]
        ex_result["reg_write"] = True 
        
        if funct == 0x20:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "010")

        elif funct == 0x22:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "011") 
            
        elif funct == 0x00:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int << shamt) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"

        elif funct == 0x02:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            res = (rt_int & 0xFFFFFFFF) >> shamt
            ex_result["alu_result_bin"] = f"{res:032b}"
            
        elif funct == 0x03:
            rt_int = int(rt_val_bin, 2)
            shamt = decoded_info["shamt"]
            if rt_int & 0x80000000: 
                res = (rt_int >> shamt) | (((1 << shamt) - 1) << (32 - shamt))
            else:
                res = rt_int >> shamt
            ex_result["alu_result_bin"] = f"{res & 0xFFFFFFFF:032b}"
            
        elif funct == 0x2A:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, rt_val_bin, "100")
            
        elif funct == 0x08:
            ex_result["update_pc"] = True
            ex_result["new_pc_int"] = int(rs_val_bin, 2)
            ex_result["reg_write"] = False

        elif funct == 0x0C:
            ex_result["reg_write"] = False

    elif opcode == 0x02:
        ex_result["update_pc"] = True
        jump_target_addr = int(decoded_info["address"], 16)
        upper_pc_bits = pc_plus_4_int & 0xF0000000
        lower_jump_bits = jump_target_addr * 4
        ex_result["new_pc_int"] = upper_pc_bits | lower_jump_bits

    elif opcode == 0x03:
        ex_result["update_pc"] = True
        jump_target_addr = int(decoded_info["address"], 16)
        upper_pc_bits = pc_plus_4_int & 0xF0000000
        lower_jump_bits = jump_target_addr * 4
        ex_result["new_pc_int"] = upper_pc_bits | lower_jump_bits

        ex_result["write_dest_reg"] = 31 
        ex_result["reg_write"] = True
        ex_result["alu_result_bin"] = f"{pc_plus_4_int:032b}"

    else:
        imm = decoded_info["immediate"]
        imm_16_bin = f"{imm & 0xFFFF:016b}"
        extended_imm_bin = sign_extend_16_to_32(imm_16_bin)
        
        if opcode == 0x08:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010")
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        elif opcode == 0x23:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010") 
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True
            ex_result["mem_read"] = True
            ex_result["mem_to_reg"] = True

        elif opcode == 0x2B:
            ex_result["alu_result_bin"] = ALU(rs_val_bin, extended_imm_bin, "010") 
            ex_result["store_data_bin"] = rt_val_bin 
            ex_result["reg_write"] = False 
            ex_result["mem_write"] = True

        elif opcode == 0x04:
            if imm == -1 and rs_val_bin == rt_val_bin:
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = -4 
                return ex_result

            alu_res = ALU(rs_val_bin, rt_val_bin, "011") 
            if int(alu_res, 2) == 0:                     
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)

        elif opcode == 0x05:
            if imm == -1 and rs_val_bin != rt_val_bin:
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = -4 
                return ex_result

            alu_res = ALU(rs_val_bin, rt_val_bin, "011") 
            if int(alu_res, 2) != 0:                     
                ex_result["update_pc"] = True
                ex_result["new_pc_int"] = pc_plus_4_int + (imm * 4)
                
        elif opcode == 0x0F:
            res = (imm << 16) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

        elif opcode == 0x0D:
            rs_int = int(rs_val_bin, 2)
            res = (rs_int | (imm & 0xFFFF)) & 0xFFFFFFFF
            ex_result["alu_result_bin"] = f"{res:032b}"
            ex_result["write_dest_reg"] = decoded_info["rt"]
            ex_result["reg_write"] = True

    return ex_result