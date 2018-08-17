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

    # For each possible pair
        # Generate their strategy vs adversarial+naive_padding
        # Replace naive_padding with pure-strats to make a fully realised adversarial strategy
        # Calculate probability of winning
        # update max_prob, best_pair if probWin > max_prob.
    # return







    # Finds the adversarial team for target_team against recently identified strategy
    best_prob = 0.0
    best_team = None
    for candidate_team in ([["K", "A"], ["K", "W"], ["W", "A"]]):
        sys.stdout=open("it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism", "w")
        if target_team == 1:
            matchup = candidate_team + opposing_pair
            prefix.run(matchup, "mdp", False)
            free_strat.run(matchup, 1)
            sys.stdout=sys.__stdout__
            os.system("cat adversarial_strategy"+str(iterations)+".txt >> it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism")
            sys.stdout=open("it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism", "a")
            suffix.run(matchup, False)
        else:
            matchup = opposing_pair + candidate_team
            prefix.run(matchup, "mdp", False)
            sys.stdout=sys.__stdout__
            os.system("cat adversarial_strategy"+str(iterations)+".txt >> it"+str(iterations)+"vs"+str(candidate_team[0])+str(candidate_team[1])+".prism")
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
    prefix.run(full_comp, "mdp", True)
    if target_team == 1:
        free_strat.run(full_comp, 1)
        os.system("cat adversarial_strategy"+str(iterations)+".txt >> it"+str(iterations)+"_adv.prism")
    else:
        os.system("cat adversarial_strategy"+str(iterations)+".txt >> it"+str(iterations)+"_adv.prism")
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
        prefix.run(characters, "mdp", False)
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
    prefix.run(chosen_seed_team+best_opponents, "mdp", True)
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
    while True:#above_opt(bestProbAdv, opposition, challenger):             # Closed for testing
        opposition = challenger
        print "Iteration " + str(iterations) + ": finding best strat against educated:", opposition
        sys.stdout=open("adversarial_strategy"+str(iterations)+".txt","w")                                             # Write adversary to file and copy rather than write x3
        if iterations%2 == 1 :
            nuNuEducate.run(challenger + opposition, "tmp", 2)
            sys.stdout=sys.__stdout__
            challenger, bestProbAdv = find_adversary(1, iterations, opposition)
        else:
            nuNuEducate.run(opposition + challenger, "tmp", 1)
            sys.stdout=sys.__stdout__
            challenger, bestProbAdv = find_adversary(2, iterations, opposition)
        iterations+=1

def run():
    global possible_pairs
    possible_pairs = [["K","A"],["K","W"],["W","A"]]
    best_score = 0.0
    best_pair = None
    chosen_seed_team = possible_pairs[0]
    print chosen_seed_team, "chosen as the seed, calculating adversaries..."
    for i in range(len(possible_pairs)):
        sys.stdout=open("seed"+str(i)+".prism","w")
        matchup = chosen_seed_team + possible_pairs[i]
        prefix.run(matchup, "mdp", False)
        seed_strat.run(matchup, 1, "none", 0)
        free_strat.run(matchup, 2)
        suffix.run(matchup, False)
        sys.stdout=sys.__stdout__
        os.system("prism -cuddmaxmem 20g -javamaxmem 20g seed"+str(i)+".prism props.props -prop 2 > log.txt")
        pair_result = find_prev_result()
        print "ProbAdv_2(" + str(matchup) + ") = " + str(pair_result)
        if pair_result > best_score:
            best_score = pair_result
            best_pair = possible_pairs[i]
    print best_pair, "found as adversarial team, generating strategy..."
    matchup = chosen_seed_team + best_pair
    sys.stdout = open("seed_v_adv.prism", "w")
    prefix.run(matchup, "mdp", True)
    seed_strat.run(matchup, 1, "none", 0)
    free_strat.run(matchup, 2)
    suffix.run(matchup, True)
    sys.stdout=sys.__stdout__
    os.system("prism -cuddmaxmem 20g -javamaxmem 20g seed_v_adv.prism props.props -prop 2 > log.txt")
    sys.stdout = open("adversarial_strategy_0.txt", "w")
    nuNuEducate.run(matchup, "tmp", 2)
    sys.stdout=sys.__stdout__

    iteration = 1
    while(True):
        best_pair = flip_and_run(iteration, best_pair)
        iteration+=1

def flip_and_run(it, opponent):
    print opponent, "is opponent team in iteration:", str(it)
    best_pair = None
    best_score = 0.0
    for i in range(len(possible_pairs)):
        sys.stdout=open("it"+str(it)+"vs"+possible_pairs[i][0]+possible_pairs[i][1]+".prism","w")
        if it % 2 == 1:
            matchup = possible_pairs[i]+opponent
            prefix.run(matchup, "mdp", False)
            free_strat.run(matchup, 1)
            sys.stdout=sys.__stdout__
            os.system("cat adversarial_strategy_"+str(it-1)+".txt >> it"+str(it)+"vs"+possible_pairs[i][0]+possible_pairs[i][1]+".prism")
            sys.stdout=open("it"+str(it)+"vs"+possible_pairs[i][0]+possible_pairs[i][1]+".prism","a")
        else:
            matchup = opponent+possible_pairs[i]
            prefix.run(matchup, "mdp", False)
            sys.stdout=sys.__stdout__
            os.system("cat adversarial_strategy_"+str(it-1)+".txt >> it"+str(it)+"vs"+possible_pairs[i][0]+possible_pairs[i][1]+".prism")
            sys.stdout=open("it"+str(it)+"vs"+possible_pairs[i][0]+possible_pairs[i][1]+".prism","a")
            free_strat.run(matchup, 2)
        suffix.run(matchup, False)
        sys.stdout=sys.__stdout__
        os.system("prism -cuddmaxmem 20g -javamaxmem 20g it"+str(it)+"vs"+possible_pairs[i][0]+possible_pairs[i][1]+".prism props.props -prop "+str(2-it%2)+" > log.txt")
        pair_result = find_prev_result()
        print "ProbAdv_"+str(it%2)+"(" + str(matchup) + ") = " + str(pair_result)
        if pair_result > best_score:
            best_score = pair_result
            best_pair = possible_pairs[i]
    print best_pair, "found as adversarial team, generating strategy..."
    sys.stdout = open("it"+str(it)+"_adv.prism", "w")
    if it % 2 == 1:
        matchup = best_pair + opponent
        prefix.run(matchup, "mdp", True)
        free_strat.run(matchup, 1)
        sys.stdout=sys.__stdout__
        os.system("cat adversarial_strategy_"+str(it-1)+".txt >> it"+str(it)+"_adv.prism")
        sys.stdout=open("it"+str(it)+"_adv.prism","a")
        suffix.run(matchup, True)
    else:
        matchup = opponent + best_pair
        prefix.run(matchup, "mdp", True)
        sys.stdout=sys.__stdout__
        os.system("cat adversarial_strategy_"+str(it-1)+".txt >> it"+str(it)+"_adv.prism")
        sys.stdout=open("it"+str(it)+"_adv.prism","a")
        free_strat.run(matchup, 2)
        suffix.run(matchup, True)
    sys.stdout=sys.__stdout__
    os.system("prism -cuddmaxmem 20g -javamaxmem 20g it"+str(it)+"_adv.prism props.props -prop "+str(2-it%2)+" > log.txt")
    sys.stdout = open("adversarial_strategy_"+str(it)+".txt", "a")
    nuNuEducate.run(matchup, "tmp", 2-(it%2))
    sys.stdout=sys.__stdout__
    return best_pair

#generate_opt_grid()    # closed for testing.
#iterate()
run()
