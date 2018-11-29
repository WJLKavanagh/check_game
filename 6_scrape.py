import sys

f = open("results/"+sys.argv[1], "r").readlines()
print(sys.argv[1][:-4] + ", Knight-Archer, Knight-Wizard, Archer-Wizard")
count = 1



for i in range(len(f)):
    if f[i].find("calculating adversaries") > 0:
        seed_res = []
        for c in range(3):
            seed_res.append(float(f[i+c+1][f[1+i].index("0."):-1]))
        print("0, " + str(seed_res[0]) + ", " \
                + str(seed_res[1]) + ", " + str(seed_res[2]))
    elif f[i].find("opponent team in iteration") > 0:
        delta = 1
        index = f[i+delta].index("0.")
        it_res = []
        for j in range(3):
            res1 = float(f[i+delta][index:-1])
            res2 = float(f[i+1+delta][index:-1])
            if res1 > res2:
                it_res.append(res2)
            else:
                it_res.append(res1)
            delta += 2
        print(str(count) + ", " + str(it_res[0]) + ", " \
                + str(it_res[1]) + ", " + str(it_res[2]))
        count+=1
