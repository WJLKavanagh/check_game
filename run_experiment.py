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
            res = info[l-i][8:20]
        if "Model checking: " in info[l-i] and prop == "":
            prop = info[l-i].split("Model checking: ")[1][:-1]
            break;
    return float(res)

def optimality(characters):     # Takes 4 characters and returns opt(win) for either team

    #print "Calculating optimal values..."

    sys.stdout=open("smg.prism","w")
    smgPrefix.run(characters)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, False)

    sys.stdout=sys.__stdout__
    os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 4 -s > log.txt")
    p1_opt = find_prev_result()
    #print "Optimal strategy for player one guarantees:", p1_opt
    os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 4g smg.prism smg_props.props -prop 5 -s > log.txt")
    p2_opt = find_prev_result()
    #print "Optimal strategy for player two guarantees:", p2_opt
    return p1_opt, p2_opt

def generate_opt_grid():    # Generates grid of opt(win) for all permutations of G

    print "Calculating optimalities, this may take some time...",
    KAkw, KWka = optimality(["K", "A", "K", "W"])
    KAwa, WAka = optimality(["K", "A", "W", "A"])
    print "33% done",
    KWwa, WAkw = optimality(["K", "W", "W", "A"])
    KAka, _ = optimality(["K", "A", "K", "A"])
    print "67% done"
    KWkw, _ = optimality(["K", "W", "K", "W"])
    WAwa, _ = optimality(["W", "A", "W", "A"])
    print "win\\vs\t|KA\t\t|KW\t\t|WA"
    print "KA\t|"+str(KAka)+"|"+str(KAkw)+"|"+str(KAwa)
    print "KW\t|"+str(KWka)+"|"+str(KWkw)+"|"+str(KWwa)
    print "WA\t|"+str(WAka)+"|"+str(WAkw)+"|"+str(WAwa)

def find_adversary(target_team, iterations, matchup):
    # Finds the adversarial team for target_team against recently identified strategy

    print "iteration:", str(iterations) + ", finding adversary for team", str(target_team)
    sys.stdout=open("adversarial_strategy.txt","w")

"""
    STATE OF PLAY: 25/7/18

    nuEducate has been updated so strats are forced to consider being stunned.

    Still needs to add the ability for strats to consider targets with health values > than what they've seen


"""

    nuEducate.run(matchup, "tmp", 3-target_team)
    sys.stdout=sys.__stdout__
    best_prob = 0.0
    best_team = None
    for opposing_team in ([["K", "A"], ["K", "W"], ["W", "A"]]):
        sys.stdout=open("it"+str(iterations)+"_"+str(target_team)+".prism", "w")
        prefix.run(characters, "mdp")
        if target_team == 1:
            free_strat.run()
            print "done for now"

def iterate(): # Cycle until converge upon Nash==
    # Generate seed strategy and find best opposition to it
    chosen_seed_team = ["K", "A"]
    print "Calculating most effective strategy vs:", chosen_seed_team,"..."
    highest_adversary = 0
    best_opponents = None
    loop = 0
    for opposing_team in ([["K", "A"], ["K", "W"], ["W", "A"]]):
        sys.stdout=open("seed"+str(loop)+".prism","w")
        characters = chosen_seed_team + opposing_team
        prefix.run(characters, "mdp")
        seed_strat.run(characters, 1, "none")
        free_strat.run(characters, 2)
        suffix.run(characters, False)
        sys.stdout=sys.__stdout__
        os.system("prism seed"+str(loop)+".prism props.props -prop 2 > log.txt")
        adversarial_probability = find_prev_result()
        print(opposing_team,"can win with probability:", adversarial_probability)
        if adversarial_probability > highest_adversary:
            highest_adversary = adversarial_probability
            best_opponents = opposing_team
        #os.system("rm seed.prism")
        loop += 1
    print ("continuing with...", best_opponents)
    # setup either player (p1,p2) and find first adversary.
    p1 = chosen_seed_team
    p2 = best_opponents
    sys.stdout = open("seed_v_adv.prism", "w")
    prefix.run(p1+p2, "mdp")
    seed_strat.run(p1+p2, 1, "none")
    free_strat.run(p1+p2, 2)
    suffix.run(p1+p2, True)
    sys.stdout=sys.__stdout__
    os.system("prism seed_v_adv.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")

    iterations = 0
    find_adversary(1, iterations, p1+p2)

#generate_opt_grid()
iterate()
