import sys
file_name = "results/c" + sys.argv[1] + "_execution_" + sys.argv[2] + ".txt"
f = file(file_name, "r")

print "Iteration & Knight-Archer & Knight-Wizard & Wizard-Archer  \\"
print "\hline"
lines = f.readlines()
num_printed = 0
for line in lines:
    if line[:8] == "ProbAdv_":
        if num_printed % 3 == 0:
            if num_printed == 0:
                print "seed &",
            else:
                print str(num_printed / 3) + " &",
        if num_printed % 3 < 2:
            print line[34:-1], "&",
        else:
            print line[34:-1], '\\' + '\\'
        num_printed += 1
