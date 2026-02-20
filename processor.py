import time
import os

# Importing all your custom MIPS modules
from memory_builder import make_byte_addressable
from fetch import fetch
from Decode import decode_instruction, REGISTER_NAMES
from execute import execute_stage
from access_data_memory import access_data_memory
from writeData import write_data_memory

def load_registers(filename="Register.txt"):
    """Reads 32-bit strings from Register.txt and converts them to integers."""
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
    """Saves the integer list back to 32-bit binary strings in Register.txt."""
    with open(filename, 'w') as f:
        for val in registers:
            # Format integer to 32-bit binary string, ensuring it handles negatives properly
            f.write(f"{val & 0xFFFFFFFF:032b}\n")

def run_mips_processor():
    print("🚀 Starting MIPS Processor Simulation...\n" + "="*50)
    
    # 1. SETUP INSTRUCTION MEMORY
    print("[SYSTEM] Building byte-addressable memory from Instructions.txt...")
    make_byte_addressable("Instructions.txt", "memory_code.txt")
    
    # 2. INITIALIZE PC AND REGISTERS
    pc_int = 0
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
        # decode_instruction returns integers (0-31) for rs, rt, rd
        decoded_info = decode_instruction(int(instr_str, 2))
        
        # Direct integer mapping (Fixed the string mapping bug here)
        rs_idx = decoded_info.get("rs", 0)
        rt_idx = decoded_info.get("rt", 0)
        
        # Read from our in-memory register state
        rd1_int = registers_state[rs_idx]
        rd2_int = registers_state[rt_idx]
        
        # Convert to 32-bit binary strings for the ALU
        rs_bin = f"{rd1_int & 0xFFFFFFFF:032b}"
        rt_bin = f"{rd2_int & 0xFFFFFFFF:032b}"
        
        # --- STAGE 3: EXECUTE ---
        pc_plus_4 = pc_int + 4
        ex_result = execute_stage(decoded_info, rs_bin, rt_bin, pc_plus_4)
        
        # Check for manual halt signals (like infinite branch loops)
        if ex_result.get("new_pc_int") == -4:
             print("🛑 Halt loop detected. Processor Halting.")
             break

        # --- STAGE 4: MEMORY ---
        mem_read_data_bin = "00000000000000000000000000000000"
        
        if ex_result.get("mem_read"):
            mem_read_data_bin = access_data_memory(ex_result["alu_result_bin"], "Data.txt")
            
        if ex_result.get("mem_write"):
            # Ensure store_data_bin exists before trying to write
            store_data = ex_result.get("store_data_bin", "00000000000000000000000000000000")
            write_data_memory(ex_result["alu_result_bin"], store_data, "Data.txt")
            
        # --- STAGE 5: WRITE BACK ---
        if ex_result.get("reg_write"):
            write_reg_idx = ex_result.get("write_dest_reg")
            
            # Write to register if it's a valid, non-zero register (Register 0 is hardwired to 0)
            if write_reg_idx is not None and write_reg_idx > 0:
                if ex_result.get("mem_to_reg"):
                    wb_data_int = int(mem_read_data_bin, 2)
                else:
                    wb_data_int = int(ex_result["alu_result_bin"], 2)
                    
                # Update our in-memory register state
                registers_state[write_reg_idx] = wb_data_int

        # --- UPDATE PC ---
        if ex_result.get("update_pc"):
            pc_int = ex_result["new_pc_int"]
        else:
            pc_int = pc_plus_4
            
        cycle_count += 1
        time.sleep(0.1) # Terminal delay

    print("="*50)
    # Save the final state to Register.txt
    save_registers(registers_state, "Register.txt")
    print("✅ Execution Complete! Saara final data 'Register.txt' aur 'Data.txt' mein save ho gaya hai.")

if __name__ == "__main__":
    # Ensure Register.txt exists so we don't hit a FileNotFoundError on the first run
    if not os.path.exists("Register.txt"):
        with open("Register.txt", "w") as f:
            for _ in range(32):
                f.write("00000000000000000000000000000000\n")
                
    run_mips_processor()