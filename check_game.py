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
            if info[l-i][8:11] == "0.0":
                res = "False"
            else:
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
    print "Optimal strategy for player one guarentees:", p1_opt
    os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 5 -s > log.txt")
    p2_opt = find_prev_result()
    print "Optimal strategy for player two guarentees:", p2_opt
    return p1_opt, p2_opt

def iterate(characters, iters):

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

        # Generate adversary files (states and transitions)
        os.system("prism EF_mul.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta >> log.txt")

        loops += 1

def run_single():
    characters = ["K", "A", "K", "W"]
    opt1, opt2 = optimality(characters)
    iterate(characters, int(sys.argv[1]))

run_single()


"""
    TODO:
        display_info()
        Opt matching
        configuration_configurations() // changing char_info
        helpful output
"""
