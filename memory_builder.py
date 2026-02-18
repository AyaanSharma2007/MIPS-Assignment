def make_byte_addressable(inf="Instructions.txt", outf="memory_code.txt"):
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

if __name__ == "__main__":
    make_byte_addressable()