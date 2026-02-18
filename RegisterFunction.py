def register_file(A1, A2, A3, WD, RegWrite, registers_state):
    """
    Simulates the MIPS Register File block.
    
    Inputs:
    A1, A2: Addresses of the registers to read (0-31)
    A3: Address of the register to write to (0-31)
    WD: The 32-bit data to write
    RegWrite: Control signal (1 means write, 0 means do nothing)
    registers_state: The list of 32 integers managed by processor.py
    
    Returns:
    RD1, RD2: The data read from registers A1 and A2
    """
    
    # 1. READ: Continuously output the data from the requested read registers
    RD1 = registers_state[A1]
    RD2 = registers_state[A2]
    
    # 2. WRITE: Update the register state IF the control signal says so
    # We also explicitly protect Register 0 ($zero), which must always remain 0
    if RegWrite == 1 and A3 != 0:
        registers_state[A3] = WD
        
    # Return the two read data outputs
    return RD1, RD2