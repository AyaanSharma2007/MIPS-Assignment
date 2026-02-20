import os

def register_file(A1, A2, A3, WD, RegWrite):
    """
    Simulates the MIPS Register File using a text file for storage.
    
    Inputs:
    A1, A2: Integer addresses of the registers to read (0-31)
    A3: Integer address of the register to write to (0-31)
    WD: The 32-bit data to write (integer)
    RegWrite: Control signal (1 means write, 0 means do nothing)
    
    Returns:
    RD1, RD2: The data read from registers A1 and A2
    """
    filename = "Register.txt"
    
    # --- 1. READ PHASE: Load registers from the file ---
    # We read all 32 lines and convert them into a list of integers
    with open(filename, "r") as file:
        registers_state = [int(line.strip()) for line in file.readlines()]
        
    # Grab the specific values for our output wires
    RD1 = registers_state[A1]
    RD2 = registers_state[A2]
    
    # --- 2. WRITE PHASE: Save back to the file if RegWrite is 1 ---
    # Register 0 is hardwired to 0, so we protect it (A3 != 0)
    if RegWrite == 1 and A3 != 0:
        registers_state[A3] = WD  # Update the specific register in our list
        
        # Open the file in write mode ("w") to overwrite it with the new state
        with open(filename, "w") as file:
            for value in registers_state:
                file.write(f"{value}\n")
                
    # --- 3. OUTPUT ---
    return RD1, RD2