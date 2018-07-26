

"""
K_hea_range: 8-12 (1)
K_acc_range: 0.65-0.8(0.05)
K_dmg_range: 2-4 (1)

A_hea_range: 6-10(1)
A_acc_range: 0.5-0.65(0.05)
A_dmg_range: 1-3 (1)

W_hea_range: 6-10(1)
W_acc_range: 0.55-0.7 (0.05)
W_dmg_range: 1-3 (1)"""
n = 0
for a in range(8, 10, 1):
    for c in range(2,4,1):
        for d in range(6, 8, 1):
            for f in range(1, 3, 1):
                for g in range(6, 8, 1):
                    for i in range(1,3,1):
                        if d >= a:
                            continue
                        if g > a:
                            continue
                        print str(a) +", "+"0.8"+", " +str(c)+", "+str(d)+", "+"0.75"+", "+str(f)+", "+str(g)+", "+"0.8"+", "+str(i)
                        n = n + 1

#print "NUMBER: " + str(n)
