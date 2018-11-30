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
    print "Optimal strategy generated, calculating adversarial probabilities..."
    for p in pairs:
        if p != ignore_pair:
            for i in range(2):
                if i == 1:                          # Run again with relfected ordering
                    tmp = [p[1],p[0]]
                    chars = plr_pair + tmp
                else:
                    chars = plr_pair + p
                file_name = "cmp"
                for char in chars:
                    file_name += char
                file_name += ".prism"
                # Generate a prism file to represent SMG of game between both teams
                sys.stdout=open(file_name,"w")
                prefix.run(chars, "mdp", False)
                sys.stdout = sys.__stdout__
                os.system("cat candidate_dom_s_" + str(t) + ".txt >> " + file_name)
                sys.stdout=open(file_name,"a")
                free_strat.run(chars, 2)
                suffix.run(chars, False)
                sys.stdout=sys.__stdout__
                # run prism-games with lots of memory, hardcoded prism-games location on SAND
                os.system("../../../../../../usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 300g -javamaxmem 300g "+ file_name + " props.props -prop 2 -s > log.txt")
                if i == 1:
                    ret_dict[str(tmp)] = find_prev_result()
                else:
                    ret_dict[str(p)] = find_prev_result()
    dominant_strategy = True
    for output_pair in ret_dict.keys():
        dominant = "dominant"
        if ret_dict[output_pair] > 0.5:
            dominant = "not dominant"
            dominant_strategy = False
        print "\tAgainst " + output_pair + " the strategy is " + dominant + " with minimum probability of winning = " + str(1 - ret_dict[output_pair])
    if dominant_strategy:
        print "\t\tThe optimal strategy for ", plr_pair, "against", ignore_pair, " is a dominant strategy."
        exit(0)
    else:
        print "This is not a dominant strategy."

# Main: setup
global pairs
pairs = [["K","A"],["K","W"],["A","W"]]
for pair in pairs:                                                          # Is an optimal strategy for this pair against any other dominant?
    print "Testing if a dominant strategy exists for", pair, "..."
    winning_strats = 0
    for opp_pair in pairs:                                                  # Check vs every opponent pair
        if pair != opp_pair:                                                # Don't check against self
            print "comparing strategy for", pair, "versus", opp_pair, "-",
            prob = optimality(pair + opp_pair)
            if prob > 0.5:                                                  # If it is dominant, add it to the dominance list
                print "Strategy could be dominant, p =", str(prob)
                winning_strats += 1
            else:                                                           # If a strategy isn't dominant for a pair, then the PAIR cannot be dominant
                print "Non-dominant pair, p = " + str(prob) + ", continuing."
                break
    if winning_strats > 1:                                                  # Dominant pair found if 2 dominant strategies are found
        file_suffix = 1
        print "Two dominant strategy candidates - pair could be dominant."      # strategies written to file as candidate_dom_s_1.txt and candidate_dom_s_2.txt
        for opp_pair in pairs:
            if opp_pair != pair:
                print "Generating optimal strategy for", pair, "against", opp_pair,
                generate_strategy(pair+opp_pair, file_suffix)
                compare_candidate(pair, opp_pair, file_suffix)
                file_suffix += 1
        exit(0)                                                             # Only one pair can be a candidate dominant pair.
