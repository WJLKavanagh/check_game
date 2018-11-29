import sys, shutil, os, filecmp                                             # utility imports
import free_strat, prefix, suffix, seed_strat, nu_educate_strat, smgPrefix, nu_smgprefix, nu_free_strat       # PRISM-generating files

# Reads log.txt and returns last found p(win)
def find_prev_result():
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

# Takes 4 characters and returns opt(win) for either team as two floats
def optimality(characters):
    char_string = ""
    for c in characters:
        char_string += str(c)
    file_name = "smg"+char_string+".prism"
    # Generate a prism file to represent SMG of game between both teams
    sys.stdout=open(file_name,"w")
    smgPrefix.run(characters)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, False)
    sys.stdout=sys.__stdout__
    # run prism-games with lots of memory, hardcoded prism-games location on SAND
    os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 100g -javamaxmem 100g "+file_name+" smg_props.props -prop 4 -s > log.txt")
    return find_prev_result()

def generate_strategy(characters, i):
    file = "smg" + characters[0] + characters[1] + characters[2] + characters[3] + "_mul.prism"
    sys.stdout = open(file,"w")
    nu_smgprefix.run(characters, "smg", True)
    nu_free_strat.run(characters, 1)
    nu_free_strat.run(characters, 2)
    suffix.run(characters, True)
    sys.stdout = sys.__stdout__
    os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 100g -javamaxmem 100g "+file+" smg_props.props -prop 1 -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")
    sys.stdout = open("candidate_dom_s_" + str(i) + ".txt","w")
    nu_educate_strat.run(characters, "tmp", 1)
    sys.stdout= sys.__stdout__

def compare_candidate(plr_pair, ignore_pair, t):
    ret_dict = {}
    for p in pairs:
        if p != ignore_pair:
            chars = plr_pair + p
            file_name = "cmp"+chars+".prism"
            # Generate a prism file to represent SMG of game between both teams
            sys.stdout=open(file_name,"w")
            prefix.run(chars, "mdp", False)
            sys.stdout = sys.__stdout__
            os.system("cat candidate_dom_s_" + t + ".txt >> " + file_name)
            sys.stdout=open(file_name,"a")
            free_strat.run(chars, 2)
            suffix.run(chars, False)
            sys.stdout=sys.__stdout__
            # run prism-games with lots of memory, hardcoded prism-games location on SAND
            os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 300g -javamaxmem 300g "+file_name+" props.props -prop 1 -s > log.txt")
            ret_dict[p] = find_prev_result()

# Main: setup
global pairs
pairs = [["K","A"],["K","W"],["A","W"]]
for pair in pairs:
    print "Testing if a dominant strategy exists for", pair
    winning_strats = 0
    for opp_pair in pairs:
        if pair != opp_pair:
            print "testing", pair, opp_pair
            prob = optimality(pair + opp_pair)
            if prob > 0.5:
                print "Strategy could be dominant..."
                winning_strats+=1
            else:
                print "Non-dominant pair"
                break
        if winning_strats > 1:          # Dominant pair found
            file_suffix = 1
            print "Pair could be dominant - generating optimal strategies..."      # strategies written to file as candidate_dom_s_1.txt and candidate_dom_s_2.txt
            for opp_pair in pairs:
                if opp_pair != pair:
                    generate_strategy(pair+opp_pair, file_suffix)
                    values = compare_candidate(pair, opp_pair, file_suffix)
                    print values
                    for p in values.keys():
                        print "Comparing optimal strat against " + str(opp_pair) + " to " + str(p) + ": " + str(values[p])
                    file_suffix += 1

#
# # Find adversary of seed strategy:
#     # generate file: seed_v_free for all opponents
#     # calculate probAdv_2 and find_max() for greatest probAdv and 'best' opponent pair
# for i in range(len(possible_pairs)):
#     sys.stdout=open("seed"+str(i)+".prism","w")
#     matchup = chosen_seed_team + possible_pairs[i]
#     prefix.run(matchup, "mdp", False)
#     seed_strat.run(matchup, 1, "none")           # "none" as no preferred action.
#     free_strat.run(matchup, 2)
#     suffix.run(matchup, False)
#     sys.stdout=sys.__stdout__
#     os.system("prism -s -javamaxmem 100g seed"+str(i)+".prism props.props -prop 2 > log.txt")
#     pair_result = find_prev_result()
#     print "ProbAdv_2(" + str(matchup) + ") = " + str(pair_result)
#     if pair_result > best_score:
#         best_score = pair_result
#         best_pair = possible_pairs[i]
#
# # Generate first adversary (adversarial_strategy_0.txt)
#     # Create model with multiple i in I
#     # write adversary to file using tmp files generated by PRISM calculation
# print best_pair, "found as adversarial team, generating strategy..."
# matchup = chosen_seed_team + best_pair
# sys.stdout = open("seed_v_adv.prism", "w")
# prefix.run(matchup, "mdp", True)
# seed_strat.run(matchup, 1, "none")
# free_strat.run(matchup, 2)
# suffix.run(matchup, True)
# sys.stdout=sys.__stdout__
# os.system("prism -cuddmaxmem 100g -javamaxmem 100g seed_v_adv.prism props.props -prop 2 -s -exportadvmdp tmp.tra -exportstates tmp.sta > log.txt")
# sys.stdout = open("adversarial_strategy_0.txt", "w")
# educate_strat.run(matchup, "tmp", 2)
# sys.stdout=sys.__stdout__
#
# # Core loop
# iteration = 1
# old_opponents = chosen_seed_team
# while adversary_is_unique(iteration):
#     #above_opt(best_score, old_opponents, best_pair)       #prob, op, chal
#     old_opponents = best_pair
#     best_pair, best_score = flip_and_run(iteration, best_pair)
#     iteration+=1
#
# # End
# print "Loop found, run terminated."
