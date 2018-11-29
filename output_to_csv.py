import sys
file_name = "results/c" + sys.argv[1] + "_execution_" + sys.argv[2] + ".txt"
f = file(file_name, "r")

print "iteration, KA, KW, WA"

lines = f.readlines()
num_printed = 0
for line in lines:
    if line[:8] == "ProbAdv_":
        if num_printed % 6 == 0:
            print str(num_printed / 6) + ",",
        if num_printed % 6 < 5:
            print line[34:-1] + ",",
        else:
            print line[34:-1]
        num_printed += 1
