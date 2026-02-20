import time
import os

# Tere banaye gaye SAARE files yahan import ho rahe hain
from memory_builder import make_byte_addressable
from fetch import fetch
from Decode import decode_instruction, REGISTER_NAMES
from execute import execute_stage
from access_data_memory import access_data_memory
from writeData import write_data_memory

# Helper to convert register names like "$t0" to their index (e.g., 8)
REGISTER_MAP = {name: i for i, name in enumerate(REGISTER_NAMES)}

def load_registers(filename="Register.txt"):
    """Register.txt se 32-bit strings padh kar integer list banata hai."""
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
        decoded_info = decode_instruction(int(instr_str, 2))
        
        rs_idx = REGISTER_MAP.get(decoded_info.get("rs"), 0)
        rt_idx = REGISTER_MAP.get(decoded_info.get("rt"), 0)
        
        # Read from our in-memory register state
        rd1_int = registers_state[rs_idx]
        rd2_int = registers_state[rt_idx]
        
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
            write_dest = ex_result["write_dest_reg"]
            write_reg_idx = -1 # Default to invalid
            
            # Handle JAL where dest is an int (31), and others where it's a string name
            if isinstance(write_dest, int):
                write_reg_idx = write_dest
            elif isinstance(write_dest, str):
                write_reg_idx = REGISTER_MAP.get(write_dest, -1)

            # Write to register if it's a valid, non-zero register
            if write_reg_idx > 0:
                if ex_result["mem_to_reg"]:
                    wb_data_int = int(mem_read_data_bin, 2)
                else:
                    wb_data_int = int(ex_result["alu_result_bin"], 2)
                    
                # Update our in-memory register state
                registers_state[write_reg_idx] = wb_data_int

        # --- UPDATE PC ---
        if ex_result["update_pc"]:
            pc_int = ex_result["new_pc_int"]
        else:
            pc_int = pc_plus_4
            
        cycle_count += 1
        time.sleep(0.1) # Terminal mein step-by-step dekhne ke liye delay

    print("="*50)
    # Save the final state of registers to the file ONCE at the end.
    save_registers(registers_state, "Register.txt")
    print("✅ Execution Complete! Saara final data 'Register.txt' aur 'Data.txt' mein save ho gaya hai.")

if __name__ == "__main__":
    # Ensure Register.txt exists initially to avoid file errors
    if not os.path.exists("Register.txt"):
        with open("Register.txt", "w") as f:
            for _ in range(32):
                f.write("00000000000000000000000000000000\n")
                
    run_mips_processor()