def make_byte_addressable(inf, outf):
    """
    Converts a word-addressable memory file (32-bit per line)
    into byte-addressable memory (8-bit per line).
    """
    try:
        with open(inf, 'r') as f_in, open(outf, 'w') as f_out:
            for line in f_in:
                line = line.strip()
                if len(line) == 32:
                    for i in range(0, 32, 8):
                        f_out.write(line[i:i+8] + '\n')
        print(f"Success: '{outf}' generated from '{inf}'.")
    except Exception as e:
        print(f"Error: {e}")


def build_all_memories():
    """
    Convert both instruction and data memory to byte-addressable.
    """
    make_byte_addressable("Instructions.txt", "memory_code.txt")
    make_byte_addressable("Data.txt", "memory_data.txt")


if __name__ == "__main__":
    build_all_memories()