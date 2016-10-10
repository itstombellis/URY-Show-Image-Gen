
output =[]
f = open('Shows.txt', 'r')



for line in f:
    output.append(line)
f.close()

for i in range(0,len(output)):
    output[i] = output[i].rstrip('\n')

