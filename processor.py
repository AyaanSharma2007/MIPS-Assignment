import memory_builder
import fetch
import Decode
import access_data_memory
import ALUandSignExtend
import RegisterFunction
import writeData
PC = 0
RUNNING = True
while RUNNING:
    raw_instruction=fetch.fetch(PC,"Instructions.txt")
    decoded_instruction=Decode.decode_instruction(raw_instruction)
    if(decoded_instruction["type"]=="R-Type") :
        pass
    elif(decoded_instruction["type"]=="J-Type"):
        pass
    else: #instruction I type hai
        pass