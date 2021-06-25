import sys

if len(sys.argv) != 2:
    raise ValueError('Inserire <bit>')

bit = sys.argv[1]
file_name = (f'multiplicator_part1_{bit}.txt')

for i in range(int(bit)):
    for j in range(int(bit)):
        text_generated = (f'W{j}{i} = AND(X{j}, Y{i})\n')
        f = open(file_name, "a")
        f.write(text_generated)
f.close()
