import sys
import shutil
import os

import free_strat, prefix, suffix, seed_strat, nuEducate, smgPrefix

def find_prev_result():                 # Reads log.txt and returns last found p(win)
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
                res = info[l-i][8:20]
        if "Model checking: " in info[l-i] and prop == "":
            prop = info[l-i].split("Model checking: ")[1][:-1]
            break;
    return float(res)

def optimality(characters):

    print "Calculating optimal values..."

    sys.stdout=open("smg.prism","w")
    smgPrefix.run(characters)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, False)

    sys.stdout=sys.__stdout__
    os.system("~/../../usr/prism-games/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 4 -s > log.txt")
    p1_opt = find_prev_result()
    print "Optimal strategy for player one guarentees:", p1_opt
    os.system("~/../../usr/prism-games/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 5 -s > log.txt")
    p2_opt = find_prev_result()
    print "Optimal strategy for player two guarentees:", p2_opt
    return p1_opt, p2_opt

conf_1 = ["K", "A", "K", "W"]
print "comparing: ", conf_1
optimality(conf_1)
conf_2 = ["K", "A", "A", "W"]
print "comparing: ", conf_2
optimality(conf_2)
conf_3 = ["K", "W", "A", "W"]
print "comparing: ", conf_3
optimality(conf_3)
