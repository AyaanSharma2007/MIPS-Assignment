import time
import os

# from memory_builder import make_byte_addressable
from fetch import fetch
from Decode import decode_instruction, REGISTER_NAMES
from execute import execute_stage
from access_data_memory import access_data_memory
from writeData import write_data_memory

def load_registers(filename="Register.txt"):
    registers = [0] * 32
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i in range(min(32, len(lines))):
                try:
                    line = lines[i].strip()
                    if len(line) == 32:
                        registers[i] = int(line, 2)
                    else:
                        registers[i] = 0
                except ValueError:
                    registers[i] = 0
    return registers

def save_registers(registers, filename="Register.txt"):
    with open(filename, 'w') as f:
        for val in registers:
            f.write(f"{val & 0xFFFFFFFF:032b}\n")

def run_mips_processor():
    print("Starting MIPS Processor Simulation...\n" + "="*50)
    # Reset Register File
    with open("Register.txt", "w") as f:
        for _ in range(32):
            f.write("00000000000000000000000000000000\n")
    from memory_builder import build_all_memories
    build_all_memories()
    
    pc_int = 0
    # registers_state = load_registers("Register.txt") 
    registers_state = [0] * 32
    
    cycle_count = 1

    while True:
        pc_str = f"{pc_int:032b}"
        print(f"\n[Cycle {cycle_count}] PC: {pc_int}")
        
        instr_str = fetch(pc_str, "memory_code.txt")
        if not instr_str:
            print("End of Instructions (or Invalid PC). Processor Halting.")
            break
            
        decoded_info = decode_instruction(int(instr_str, 2))
        
        # ==========================================
        # NEW: SYSCALL INTERCEPTOR
        # ==========================================
        # Check if Opcode is 0x00 and Funct is 0x0c (syscall)
        if decoded_info.get("opcode") == "0x0" and decoded_info.get("funct") == "0xc":
            v0_val = registers_state[2] # $v0 is Register 2
            
            if v0_val == 10:
                print(f"Syscall 10 (Exit) detected at PC {pc_int}. Processor Halting.")
                break
            else:
                print(f"Warning: Syscall {v0_val} not implemented. Ignoring.")
                pc_int += 4
                cycle_count += 1
                continue # Skip the execution stage and go to the next instruction
        # ==========================================

        rs_idx = decoded_info.get("rs", 0)
        rt_idx = decoded_info.get("rt", 0)
        
        rd1_int = registers_state[rs_idx]
        rd2_int = registers_state[rt_idx]
        rs_bin = f"{rd1_int & 0xFFFFFFFF:032b}"
        rt_bin = f"{rd2_int & 0xFFFFFFFF:032b}"
        
        pc_plus_4 = pc_int + 4
        ex_result = execute_stage(decoded_info, rs_bin, rt_bin, pc_plus_4)
        
        if ex_result.get("new_pc_int") == -4:
             print("Halt loop detected. Processor Halting.")
             break

        mem_read_data_bin = "00000000000000000000000000000000"
        
        if ex_result.get("mem_read"):
            mem_read_data_bin = access_data_memory(ex_result["alu_result_bin"], "memory_data.txt")
            
        if ex_result.get("mem_write"):
            store_data = ex_result.get("store_data_bin", "00000000000000000000000000000000")
            write_data_memory(ex_result["alu_result_bin"], store_data, "memory_data.txt")
            
        if ex_result.get("reg_write"):
            write_reg_idx = ex_result.get("write_dest_reg")
            
            if write_reg_idx is not None and write_reg_idx > 0:
                if ex_result.get("mem_to_reg"):
                    wb_data_int = int(mem_read_data_bin, 2)
                else:
                    wb_data_int = int(ex_result["alu_result_bin"], 2)
                    
                registers_state[write_reg_idx] = wb_data_int

        if ex_result.get("update_pc"):
            pc_int = ex_result["new_pc_int"]
        else:
            pc_int = pc_plus_4
            
        cycle_count += 1
        save_registers(registers_state, "Register.txt")
        input("Press Enter to execute the next cycle...")

    print("="*50)
    save_registers(registers_state, "Register.txt")
    print("Execution Complete! Final data saved to 'Register.txt' and 'Data.txt'.")

if __name__ == "__main__":
    if not os.path.exists("Register.txt"):
        with open("Register.txt", "w") as f:
            for _ in range(32):
                f.write("00000000000000000000000000000000\n")
                
    run_mips_processor()