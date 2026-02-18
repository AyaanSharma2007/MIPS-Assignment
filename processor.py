import time
import os

# Tere banaye gaye SAARE files yahan import ho rahe hain
from memory_builder import make_byte_addressable
from fetch import fetch
from Decode import decode_instruction
from RegisterFunction import register_file
from execute import execute_stage
from access_data_memory import access_data_memory
from writeData import write_data_memory

def load_registers(filename="Register.txt"):
    """Register.txt se 32-bit strings padh kar integer list banata hai."""
    registers = [0] * 32
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i in range(min(32, len(lines))):
                try:
                    registers[i] = int(lines[i].strip(), 2)
                except ValueError:
                    registers[i] = 0
    return registers

def save_registers(registers, filename="Register.txt"):
    """Integer list ko wapas 32-bit binary strings banakar Register.txt me save karta hai."""
    with open(filename, 'w') as f:
        for val in registers:
            # Format integer to 32-bit binary string, handling negatives
            f.write(f"{val & 0xFFFFFFFF:032b}\n")

def run_mips_processor():
    print("🚀 Starting MIPS Processor Simulation...\n" + "="*50)
    
    # 1. SETUP INSTRUCTION MEMORY
    # Yeh line Instructions.txt se memory_code.txt bana degi!
    print("[SYSTEM] Building memory from Instructions.txt...")
    make_byte_addressable("Instructions.txt", "memory_code.txt")
    
    # 2. INITIALIZE PC AND REGISTERS
    pc_int = 0
    # Register.txt ko padh kar state load kar rahe hain
    registers_state = load_registers("Register.txt") 
    
    cycle_count = 1

    # ==========================================
    # THE MAIN CPU CLOCK LOOP
    # ==========================================
    while True:
        pc_str = f"{pc_int:032b}"
        print(f"\n[Cycle {cycle_count}] PC: {pc_int}")
        
        # --- STAGE 1: FETCH ---
        instr_str = fetch(pc_str, "memory_code.txt")
        if not instr_str:
            print("🛑 End of Instructions (or Invalid PC). Processor Halting.")
            break
            
        # --- STAGE 2: DECODE & REGISTER READ ---
        decoded_info = decode_instruction(instr_str)
        
        rs_idx = decoded_info.get("rs", 0)
        rt_idx = decoded_info.get("rt", 0)
        
        # Tere RegisterFunction ko call kiya
        rd1_int, rd2_int = register_file(rs_idx, rt_idx, 0, 0, 0, registers_state)
        
        # Execute module ke ALU ke liye binary string me badla
        rs_bin = f"{rd1_int & 0xFFFFFFFF:032b}"
        rt_bin = f"{rd2_int & 0xFFFFFFFF:032b}"
        
        # --- STAGE 3: EXECUTE ---
        pc_plus_4 = pc_int + 4
        ex_result = execute_stage(decoded_info, rs_bin, rt_bin, pc_plus_4)
        
        # --- STAGE 4: MEMORY ---
        mem_read_data_bin = "00000000000000000000000000000000"
        
        if ex_result["mem_read"]:
            # Tera access_data_memory file call kiya
            mem_read_data_bin = access_data_memory(ex_result["alu_result_bin"], "Data.txt")
            
        if ex_result["mem_write"]:
            # Tera writeData file call kiya
            write_data_memory(ex_result["alu_result_bin"], ex_result["store_data_bin"], "Data.txt")
            
        # --- STAGE 5: WRITE BACK ---
        if ex_result["reg_write"]:
            write_reg_idx = ex_result["write_dest_reg"]
            
            # $zero (0) me nahi likhte
            if write_reg_idx != 0 and write_reg_idx is not None:
                if ex_result["mem_to_reg"]:
                    wb_data_int = int(mem_read_data_bin, 2)
                else:
                    wb_data_int = int(ex_result["alu_result_bin"], 2)
                    
                # Register me likh diya (RegWrite = 1)
                register_file(0, 0, write_reg_idx, wb_data_int, 1, registers_state)
                
        # HAR CYCLE KE BAAD REGISTER.TXT UPDATE KARO
        save_registers(registers_state, "Register.txt")
                
        # --- UPDATE PC ---
        if ex_result["update_pc"]:
            pc_int = ex_result["new_pc_int"]
        else:
            pc_int = pc_plus_4
            
        cycle_count += 1
        time.sleep(0.1) # Terminal mein step-by-step dekhne ke liye delay

    print("="*50)
    print("✅ Execution Complete! Saara final data 'Register.txt' aur 'Data.txt' mein save ho gaya hai.")

if __name__ == "__main__":
    # Ensure Register.txt exists initially to avoid file errors
    if not os.path.exists("Register.txt"):
        with open("Register.txt", "w") as f:
            for _ in range(32):
                f.write("00000000000000000000000000000000\n")
                
    run_mips_processor()