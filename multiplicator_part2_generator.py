import sys

if len(sys.argv) != 3:
    raise ValueError('Inserire <input_name> <bit>')

W = sys.argv[1]
bit = sys.argv[2]

file_name = (f'multiplicator_part2_{W}-{bit}.txt')

for i in range(int(bit)-1):
    for j in range(int(bit)):
        if i==0:
            if j==0:
                #primo giro ho un halfadder
                text_generated=(f'S{j}{i} = XOR({W}{j}{i+1}, {W}{j+1}{i})\nC{i}{j} = AND({W}{j}{i+1}, {W}{j+1}{i})\n')
                # if j==3:
                #     text_generated=(f'S{i}{j} = XOR({W}{j}{i+1}, {W}{j+1}{i})\nC{i}{j} = AND({W}{j}{i+1}, {W}{j+1}{i})\n')
            else:
                text_generated='wip_fa\n'
        else:
            if j==0:
                #primo giro ho un halfadder
                text_generated=(f'S{j}{i} = XOR({W}{j}{i+1}, S{j+1}{i-1})\nC{i}{j} = AND({W}{j}{i+1}, S{j+1}{i-1})\n')
                # if j==3:
                #     text_generated=(f'S{i}{j} = XOR({W}{j}{i+1}, {W}{j+1}{i})\nC{i}{j} = AND({W}{j}{i+1}, {W}{j+1}{i})\n')
            else:
                text_generated='wip_fa\n'
        f = open(file_name, "a")
        f.write(text_generated)
f.close()
