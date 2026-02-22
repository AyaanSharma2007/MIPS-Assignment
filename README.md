#  MIPS Single-Cycle Processor Simulator

**A cycle-accurate, software-based MIPS datapath simulator.**

MIPS (Microprocessor without Interlocked Pipelined Stages) is a family of Reduced Instruction Set Computer (RISC) architectures designed with an emphasis on simplicity, high performance, and efficient pipelining. 

This project simulates the core functionality of a MIPS processor. Designed to model a streamlined instruction set, this pure Python application accurately replicates the five key stages of execution: Fetch, Decode, Execute, Memory Access, and Writeback without unnecessary complexity. By decoding raw 32-bit machine code and converting it into byte-addressable memory, the simulator dynamically updates architectural states including the Program Counter (PC) and memory addresses cycle-by-cycle.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Assembly](https://img.shields.io/badge/Assembly-000000?style=for-the-badge&logo=assembly&logoColor=white)

---

##  Project Structure

Here is exactly how the files are organized within the simulator:

```mermaid
flowchart LR

%% =========================
%% COLOR SYSTEM
%% =========================
classDef root fill:#6c5ce7,stroke:#ffffff,stroke-width:2px,color:#ffffff

classDef coreParent fill:#0b5ed7,stroke:#ffffff,stroke-width:2px,color:#ffffff
classDef coreChild fill:#4dabf7,stroke:#ffffff,stroke-width:2px,color:#ffffff

classDef memParent fill:#087f5b,stroke:#ffffff,stroke-width:2px,color:#ffffff
classDef memChild fill:#38d9a9,stroke:#ffffff,stroke-width:2px,color:#ffffff

classDef ioParent fill:#c92a2a,stroke:#ffffff,stroke-width:2px,color:#ffffff
classDef ioChild fill:#ff8787,stroke:#ffffff,stroke-width:2px,color:#ffffff


%% =========================
%% ROOT
%% =========================
Root([MIPS Simulator]):::root


%% =========================
%% CORE DATAPATH
%% =========================
Core([Core Datapath]):::coreParent
Root --> Core

Core --> P([processor.py]):::coreChild
Core --> F([fetch.py]):::coreChild
Core --> D([Decode.py]):::coreChild
Core --> E([execute.py]):::coreChild
Core --> ALU([ALUandSignExtend.py]):::coreChild


%% =========================
%% MEMORY MANAGEMENT
%% =========================
MemMgr([Memory Management]):::memParent
Root --> MemMgr

MemMgr --> MB([memory_builder.py]):::memChild
MemMgr --> AM([access_data_memory.py]):::memChild
MemMgr --> WD([writeData.py]):::memChild


%% =========================
%% IO FILES
%% =========================
IO([I/O Files]):::ioParent
Root --> IO

IO --> IN([Instructions.txt]):::ioChild
IO --> DAT([Data.txt]):::ioChild
IO --> REG([Register.txt]):::ioChild
IO --> MC([memory_code.txt]):::ioChild
IO --> MD([memory_data.txt]):::ioChild
```

---

##  System Architecture & Datapath

The simulator is built with a highly modular design. The following flowchart maps out the data flow from memory initialization through the processor's main execution loop.

```mermaid
flowchart TB

%% =================================
%% COLOR SYSTEM
%% =================================
classDef stage fill:#3b82f6,stroke:#ffffff,stroke-width:2px,color:#ffffff
classDef compute fill:#8b5cf6,stroke:#ffffff,stroke-width:2px,color:#ffffff
classDef control fill:#10b981,stroke:#ffffff,stroke-width:2px,color:#ffffff
classDef memory fill:#f97317,stroke:#ffffff,stroke-width:2px,color:#ffffff

%% dull helper operation boxes
classDef signal fill:#f8fafc,stroke:#e5e7eb,stroke-width:1px,color:#9ca3af

%% =================================
%% MAIN FLOW (ROUNDED RECTANGLES)
%% =================================
PC([Program Counter]):::control

Fetch([Fetch Stage]):::stage
Decode([Decode Stage]):::stage
Execute([Execute Stage]):::stage
MemAccess([Memory Access]):::stage
WriteBack([Write Back]):::stage
ReadWrite([Read / Write]):::stage

ALU([ALU + Sign Extend]):::compute


%% =================================
%% MEMORY (CYLINDERS)
%% =================================
INST[(Instruction Memory)]:::memory
DATA[(Data Memory)]:::memory
REG[(Register File Output)]:::memory


%% =================================
%% OPERATION BOXES (DULL COLORS)
%% =================================
ReadInstr([Reads Instruction]):::signal
MathLogic([Math & Logic]):::signal



%% =================================
%% PIPELINE FLOW
%% =================================
PC --> Fetch
Fetch --> Decode
Decode --> Execute
Execute --> MemAccess
MemAccess --> WriteBack


%% =================================
%% INTERACTIONS
%% =================================
Fetch -.-> ReadInstr -.-> INST
Execute -.-> MathLogic -.-> ALU
MemAccess --> ReadWrite --> DATA
WriteBack --> REG
```

##  Supported Algorithmic Workloads
As part of this project, we implemented three core algorithmic programs in MIPS assembly language:

### Binary Search:
Utilizes a divide-and-conquer approach to efficiently locate the exact index of a target integer (k) within a sorted sequence of n integers, significantly reducing time complexity compared to linear methods.

### Median and Average Calculator:
Analyzes a sequence of integers to compute both the arithmetic mean and the statistical middle of the dataset, handling the necessary logic required for accurate whole-number results.

### Partition Function:
Implements a standard array partitioning algorithm, a core component of QuickSort. It selects a pivot element and rearranges the given sequence so that all values smaller than the pivot precede it, returning the pivot's correct sorted index.

##  How to Run the Simulator
### Memory Initialization State

Before the cycles begin, the simulator automatically handles the memory translation from 32-bit MARS output to 8-bit byte-addressable RAM.

```mermaid
stateDiagram-v2

%% ===== STATES (ALL COLORED BLOCKS) =====
state "32-bit Input Received from MARS" as Input
state "processor.py boots" as Boot
state "MemoryBuilder" as Builder
state "Splits strings into 8-bit chunks" as Split
state "ByteAddressableRAM" as RAM
state "Execution begins" as Exec
state "ReadyState" as Ready

%% ===== FLOW =====
[*] --> Input
Input --> Boot
Boot --> Builder
Builder --> Split
Split --> RAM
RAM --> Exec
Exec --> Ready
Ready --> [*]

%% ===== ALTERNATING COLOR PALETTE =====
%% Blue (dark)
style Input fill:#2563eb,stroke:#ffffff,stroke-width:2px,color:#ffffff

%% Teal (light)
style Boot fill:#99f6e4,stroke:#ffffff,stroke-width:2px,color:#042f2e

%% Purple (dark)
style Builder fill:#7c3aed,stroke:#ffffff,stroke-width:2px,color:#ffffff

%% Orange (light)
style Split fill:#fdba74,stroke:#ffffff,stroke-width:2px,color:#7c2d12

%% Blue (dark)
style RAM fill:#1d4ed8,stroke:#ffffff,stroke-width:2px,color:#ffffff

%% Green (light)
style Exec fill:#86efac,stroke:#ffffff,stroke-width:2px,color:#064e3b

%% Indigo (dark)
style Ready fill:#4338ca,stroke:#ffffff,stroke-width:2px,color:#ffffff
```

### 1. Load Your Binaries

To execute a new MIPS program, use the copy-paste method to load your machine code into the simulator:

Copy the 32-bit instruction binary from your program and paste it into Instructions.txt.

Copy the 32-bit data binary and paste it into Data.txt

### 2. Execute the Datapath

Open your terminal, navigate to the project directory, and initialize the main processor loop:

```bash
python processor.py
```

### 3. Verify Execution State

Upon encountering a halt loop or a syscall 10, the simulator will safely exit and dump the final processor state:

Check Register.txt for final register values

**At the end of every single clock cycle, the processor's active register state is instantly synced and saved to `Register.txt`    
and, data is instantly synced and saved to `memory_data.txt` for accurate cycle-by-cycle debugging.**

Check memory_data.txt for any variables or arrays written back to RAM via sw instructions.

## 🎓 Academic Context
This simulator was developed as part of EGC 121: Computer Architecture, prepared for Prof. Karthikeyan Vaidyanathan at the International Institute of Information Technology, Bangalore (IIITB).

### Contributors:

Arush Kumar Jain (Roll No: BC2025013)

Ayaan Sharma (Roll No: BC2025017)

Manvik Kumar Gupta (Roll No: BC2025059)


<div align="center">
  <p><i>It’s exactly like a real MIPS processor, except it runs at the blazing fast speed of a Python while loop.</i></p>
</div>



