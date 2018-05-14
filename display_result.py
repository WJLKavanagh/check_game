info = open("log.txt", "r").readlines()
l = len(info)

res = ""
prop = ""
# find prop & result
for i in range(1,l):
    if info[l-i][:8] == "Result: " and res == "":
        if info[l-i][8:11] == "0.0":
            res = "False"
        else:
            res = info[l-i][8:20] + " to 10 dp"
    if "Model checking: " in info[l-i] and prop == "":
        prop = info[l-i].split("Model checking: ")[1][:-1]
        break;

# print ..
print "PROP: " + prop + " = " + res
