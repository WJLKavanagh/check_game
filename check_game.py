import sys
import shutil
import os

import free_strat, prefix, suffix, seed_strat, nuEducate, smgPrefix

characters = ["K", "A", "K", "W"]

def find_prev_result():                 # Reads log.txt and returns last found p(win)
    info = open("log.txt", "r").readlines()
    l = len(info)
    res = ""
    prop = ""
    # find prop & result
    for i in range(1,l):
        if info[l-i][:8] == "Result: " and res == "":
            res = info[l-i][8:20]
        if "Model checking: " in info[l-i] and prop == "":
            prop = info[l-i].split("Model checking: ")[1][:-1]
            break;
    # print ..
    return float(res)

def optimality(characters):

    print "Calculating optimal values..."

    sys.stdout=open("smg.prism","w")
    smgPrefix.run(characters)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, False)

    sys.stdout=sys.__stdout__
    os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 4 -s > log.txt")
    p1_opt = find_prev_result()
    print "Optimal strategy for player one guarantees:", p1_opt
    os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 5 -s > log.txt")
    p2_opt = find_prev_result()
    print "Optimal strategy for player two guarantees:", p2_opt
    return p1_opt, p2_opt

def iterate(characters, iters, p1_opt, p2_opt):

    returnable_results = [p1_opt, p2_opt]
    print "Starting iterations..."
    # Creating the initial seeded model file for iteration
    sys.stdout=open("seed.prism","w")
    prefix.run(characters, "mdp")
    seed_strat.run(characters, 1, "none")
    free_strat.run(characters, 2)

    sys.stdout=sys.__stdout__
    os.system("cp seed.prism seed_mul.prism")
    sys.stdout=open("seed.prism","a")
    suffix.run(characters, False)
    sys.stdout=open("seed_mul.prism","a")
    suffix.run(characters, True)
    # Two files written, single and default initial states
    sys.stdout=sys.__stdout__

    os.system("prism seed.prism props.props -prop 2 -s > log.txt")
    p2_win_seed = find_prev_result()
    print "P2(win):", p2_win_seed
    returnable_results += [p2_win_seed]

    # Generate adversary files (states and transitions)
    os.system("prism seed_mul.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta >> log.txt")

    loops = 0
    while loops < iters:

        # Do Free v Educated
        sys.stdout=open("FE.prism","w")
        prefix.run(characters, "mdp")
        free_strat.run(characters, 1)
        nuEducate.run(characters, "tmp", 2)

        sys.stdout=sys.__stdout__
        os.system("cp FE.prism FE_mul.prism")
        sys.stdout=open("FE.prism","a")
        suffix.run(characters, False)
        sys.stdout=open("FE_mul.prism","a")
        suffix.run(characters, True)
        # Two files written, single and default initial states
        sys.stdout=sys.__stdout__
        os.system("prism FE.prism props.props -prop 1 -s >> log.txt")
        p1_win = find_prev_result()
        print "P1(win):", p1_win
        returnable_results += [p1_win]
        if abs(p1_win - p1_opt) < 0.0001:
            print "OPTIMAL VALUE FOR P1 REACHED, DIFFERENCE =", abs(p1_win - p1_opt)
            it_count = len(returnable_results)
            for i in range(it_count - 1, 11):
                returnable_results += ["/"]
            returnable_results += [it_count - 2]
            return returnable_results
        # Generate adversary files (states and transitions)
        os.system("prism FE_mul.prism props.props -prop 1 -s -exportadvmdp tmp.tra -exportstates tmp.sta >> log.txt")


        # Do Educated v Free
        sys.stdout=open("EF.prism","w")
        prefix.run(characters, "mdp")
        nuEducate.run(characters, "tmp", 1)
        free_strat.run(characters, 2)

        sys.stdout=sys.__stdout__
        os.system("cp EF.prism EF_mul.prism")
        sys.stdout=open("EF.prism","a")
        suffix.run(characters, False)
        sys.stdout=open("EF_mul.prism","a")
        suffix.run(characters, True)
        # Two files written, single and default initial states
        sys.stdout=sys.__stdout__
        os.system("prism EF.prism props.props -prop 2 -s >> log.txt")
        p2_win = find_prev_result()
        print "P2(win):", p2_win
        returnable_results += [p2_win]
        if abs(p2_win - p2_opt) < 0.0001:
            print "OPTIMAL VALUES FOR P2 REACHED, DIFFERENCE =", abs(p2_win-p2_opt)
            it_count = len(returnable_results)
            for i in range(it_count - 1, 11):
                returnable_results += ["/"]
            returnable_results += [it_count - 2]
            return returnable_results
        # Generate adversary files (states and transitions)
        os.system("prism EF_mul.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta >> log.txt")

        loops += 1

    returnable_results += [loops]
    return returnable_results

def find_attribute(C, attribute):
    index_diff = 0
    for i in range(len(info)):
        if info[i][0] == C:
            attributes = info[i+1][:-1].split(", ")
            break
    for j in range(len(attributes)):
        if attributes[j] == attribute:
            index_diff = j + 2
            break
    return i + index_diff

def rewrite(character, attribute, b):
    global info
    f = open("char_info.txt","r+")
    info = f.readlines()
    num = find_attribute(character, attribute)
    f.close()
    f = open("char_info.txt", "w")
    for i in range(len(info)):
        if i != num:
             f.write(info[i])
        else:
             f.write(b + "\n")
    f.close()

def run_single():
    opt1, opt2 = optimality(characters)
    if abs(opt1 - 0.5) > 0.1 or abs(opt2 - 0.5) > 0.1:
        print "optimal strategy is not within 10% of 50%"
        return [opt1, opt2, "/", "/", "/", "/", "/", "/", "/", "/", "/", "/", "-1"]
    results = iterate(characters, 8, opt1, opt2)
    return results


""" NEW VERSION:::      """
n = 192
f = open("source.csv", "r+")
column_header = f.readline()
nums = f.readlines()
f.close()
g = open("source.csv", "w")
g.write(column_header)
lines_read = 0
attrib = column_header.split(", ")
for line in nums:
    if len(nums[lines_read].split(", ")) > 10:
        g.write(nums[lines_read])
        lines_read = lines_read + 1
        n = n - 1
        continue
    for i in range(9):
        if i == 8:
            rewrite(attrib[i][0], attrib[i][2:], nums[lines_read].split(", ")[i][:-1])
        else:
            rewrite(attrib[i][0], attrib[i][2:], nums[lines_read].split(", ")[i])
    run_results = run_single()
    n = n - 1
    new_line = line[:-1] + ", "
    print "RUN_RES: ", run_results
    for elem in run_results:
        new_line += str(elem)
        new_line += ", "
    new_line += "\n"
    g.write(new_line)
    lines_read = lines_read + 1
    print "lines left:", n
g.close()


"""     OLD VERSION:::
K_acc_range = [0.755, 0.810]                # RULE: Knight)acc >> ARcher_acc
W_acc_range = [0.695, 0.750]
A_acc_range = [0.625, 0.695]

for a in K_acc_range:
    rewrite("K", "acc", str(a))
    for b in W_acc_range:
        rewrite("W", "acc", str(b))
        for c in A_acc_range:
            rewrite("A", "acc", str(c))
            print "================="
            print "RUNNING WITH K:W:A ACCUARY AS:", a,b,c
            run_single()
"""



"""
    TODO:
???     display_info()       THIS A PATH DIAG?
DONE    Opt matching
DONE    configuration_configurations() // changing char_info
???     helpful output
"""
