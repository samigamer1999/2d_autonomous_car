
f = open("temp", "r")
s = ''
for line in f:
    temp = line.split(',')
    s += temp[0] +','+temp[1]+ ' '+ temp[6]+"\n"
f.close()
f = open("new_file.txt", "w")
f.write(s)