import sys

if len(sys.argv) != 5:
    raise ValueError('Inserire <input1_name> <input2_name> <output_name> <bit>')

X = sys.argv[1]
Y = sys.argv[2]
W = sys.argv[3]
bit = sys.argv[4]
file_name = (f'multiplicator_part1_{X}-{Y}-{W}-{bit}.txt')

for i in range(int(bit)):
    for j in range(int(bit)):
        text_generated = (f'{W}{j}{i} = AND({X}{j}, {Y}{i})\n')
        f = open(file_name, "a")
        f.write(text_generated)
f.close()
