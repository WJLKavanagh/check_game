import sys
import shutil
import os

import free_strat, prefix, suffix, seed_strat, nuNuEducate, smgPrefix

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
    #LAPTOP
    #os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 8g -javamaxmem 8g smg.prism smg_props.props -prop 4 -s > log.txt")
    #DESKTOP
    #os.system("~/../../usr/prism-games/prism-games-2.0.beta3-linux64/bin/prism  -cuddmaxmem 8g -javamaxmem 8g smg.prism smg_props.props -prop 4 -s > log.txt")
    #SAND
    os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 8g -javamaxmem 8g smg.prism smg_props.props -prop 4 -s > log.txt")

    p1_opt = find_prev_result()
    #print "Optimal strategy for player one guarantees:", p1_opt
    #LAPTOP
    #os.system("~/Documents/Applications/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 8g -javamaxmem 8g smg.prism smg_props.props -prop 5 -s > log.txt")
    #DESKTOP
    #os.system("~/../../usr/prism-games/prism-games-2.0.beta3-linux64/bin/prism  -cuddmaxmem 8g -javamaxmem 8g smg.prism smg_props.props -prop 5 -s > log.txt")
    #SAND
    os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 8g -javamaxmem 8g smg.prism smg_props.props -prop 5 -s > log.txt")

    p2_opt = find_prev_result()
    #print "Optimal strategy for player two guarantees:", p2_opt
    return p1_opt, p2_opt

def generate_opt_grid():    # Generates grid of opt(win) for all permutations of G
    global KAkw, KAwa, KAka, KWkw, KWwa, KWka, WAkw, WAwa, WAka
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
    print "KA\t|"+str(KAka)+"\t|"+str(KAkw)+"\t|"+str(KAwa)
    print "KW\t|"+str(KWka)+"\t|"+str(KWkw)+"\t|"+str(KWwa)
    print "WA\t|"+str(WAka)+"\t|"+str(WAkw)+"\t|"+str(WAwa)

def above_opt(probability, opposition, challenger):
    opt = 0
    if challenger == ["K","A"]:
        if opposition == ["K","W"]:
            opt = KAkw
        elif opposition == ["W","A"]:
            opt = KAwa
        else:
            opt = KAka
    elif challenger == ["K","W"]:
         if opposition == ["K","W"]:
             opt = KWkw
         elif opposition == ["W","A"]:
             opt = KWwa
         else:
             opt = KWka
    else:
        if opposition == ["K","W"]:
            opt = WAkw
        elif opposition == ["W","A"]:
            opt = WAwa
        else:
            opt = WAka
    return probability > opt

def find_adversary(target_team, iterations, opposing_pair):
    # Finds the adversarial team for target_team against recently identified strategy
    best_prob = 0.0
    best_team = None
    for candidate_team in ([["K", "A"], ["K", "W"], ["W", "A"]]):
        sys.stdout=open("it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism", "w")
        if target_team == 1:
            matchup = candidate_team + opposing_pair
            prefix.run(matchup, "mdp")
            free_strat.run(matchup, 1)
            sys.stdout=sys.__stdout__
            os.system("cat adversarial_strategy.txt >> it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism")
            sys.stdout=open("it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism", "a")
            suffix.run(matchup, False)
        else:
            matchup = opposing_pair + candidate_team
            prefix.run(matchup, "mdp")
            sys.stdout=sys.__stdout__
            os.system("cat adversarial_strategy.txt >> it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism")
            sys.stdout=open("it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism", "a")
            free_strat.run(matchup, 2)
            suffix.run(matchup, False)
        sys.stdout=sys.__stdout__
        os.system("prism -cuddmaxmem 8g -javamaxmem 8g it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1]) + ".prism props.props -prop " + str(target_team) + " > log.txt")
        candidate_probability = find_prev_result()
        if candidate_probability > best_prob:
            best_prob = candidate_probability
            best_team = candidate_team
        print candidate_team, "could guarantee", candidate_probability, "against", opposing_pair
    print "generating states for best opponent:", best_team, "with probAdv =", best_prob
    sys.stdout = open("it"+str(iterations)+"_adv.prism", "w")
    if target_team == 1:
        full_comp = best_team + opposing_pair
    else:
        full_comp = opposing_pair + best_team
    prefix.run(full_comp, "mdp")
    if target_team == 1:
        free_strat.run(full_comp, 1)
        os.system("cat adversarial_strategy.txt")
    else:
        os.system("cat adversarial_strategy.txt")
        free_strat.run(full_comp,2)
    suffix.run(full_comp, True)
    sys.stdout=sys.__stdout__
    os.system("prism -cuddmaxmem 8g -javamaxmem 8g it"+str(iterations)+"_adv.prism props.props -prop " + str(target_team) + " -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")
    return best_team, best_prob

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
        seed_strat.run(characters, 1, "none", 0)
        free_strat.run(characters, 2)
        suffix.run(characters, False)
        sys.stdout=sys.__stdout__
        os.system("prism -cuddmaxmem 8g -javamaxmem 8g seed"+str(loop)+".prism props.props -prop 2 > log.txt")
        adversarial_probability = find_prev_result()
        print(opposing_team,"can win with probability:", adversarial_probability)
        if adversarial_probability > highest_adversary:
            highest_adversary = adversarial_probability
            best_opponents = opposing_team
        #os.system("rm seed.prism")
        loop += 1
    print "continuing with...", best_opponents, "as team 2"
    sys.stdout = open("seed_v_adv.prism", "w")
    prefix.run(chosen_seed_team+best_opponents, "mdp")
    seed_strat.run(chosen_seed_team+best_opponents, 1, "none", 0)
    free_strat.run(chosen_seed_team+best_opponents, 2)
    suffix.run(chosen_seed_team+best_opponents, True)
    sys.stdout=sys.__stdout__
    os.system("prism -cuddmaxmem 8g -javamaxmem 8g seed_v_adv.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")
    print "Adversarial strategy generated"

    opposition = chosen_seed_team
    challenger = best_opponents
    iterations = 1
    bestProbAdv = highest_adversary
    while above_opt(bestProbAdv, opposition, challenger):
        opposition = challenger
        print "Iteration " + str(iterations) + ": find best stat against", opposition
        sys.stdout=open("adversarial_strategy.txt","w")                                             # Write adversary to file and copy rather than write x3
        if iterations%2 == 0:
            nuNuEducate.run(challenger + opposition, "tmp", 2)
            sys.stdout=sys.__stdout__
            challenger, bestProbAdv = find_adversary(1, iterations, opposition)
        else:
            nuNuEducate.run(opposition + challenger, "tmp", 1)
            sys.stdout=sys.__stdout__
            challenger, bestProbAdv = find_adversary(2, iterations, opposition)
        iterations+=1


    """
    # setup players (p1,p2) and find first adversary.
    p1 = chosen_seed_team
    p2 = best_opponents
    sys.stdout = open("seed_v_adv.prism", "w")
    prefix.run(p1+p2, "mdp")
    seed_strat.run(p1+p2, 1, "none", 0)
    free_strat.run(p1+p2, 2)
    suffix.run(p1+p2, True)
    sys.stdout=sys.__stdout__
    os.system("prism -cuddmaxmem 8g -javamaxmem 8g seed_v_adv.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")
    print ("Adversary calculated")


    iterations = 0
    educated = p2
    challenger = p1
    ProbAdv = 1.0           # To pass initial check
    while above_opt(ProbAdv, educated, challenger):     # While ProbAdv > ProbOpt
        educated = challenger
        print "iteration:", str(iterations) + ", finding adversarial strategy against:", educated
        sys.stdout=open("adversarial_strategy.txt","w")                                             # Write adversary to file and copy rather than write x3
        if iterations%2 == 0:
            nuNuEducate.run(challenger + educated, "tmp", 2)
            sys.stdout=sys.__stdout__
            challenger = find_adversary(1, iterations, educated)
        else:
            nuNuEducate.run(educated + challenger, "tmp", 1)
            sys.stdout=sys.__stdout__
            challenger = find_adversary(2, iterations, educated)
        iterations+=1
        ProbAdv = find_prev_result()
        print "Best team found to be:", challenger, "with P = " + str(ProbAdv)

    """
generate_opt_grid()
iterate()
