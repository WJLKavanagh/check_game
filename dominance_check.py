import sys, shutil, os, filecmp                                             # utility imports
import free_strat, prefix, suffix, seed_strat, nu_educate_strat, smgPrefix, nu_smgprefix, nu_free_strat       # PRISM-generating files

# Reads log.txt and returns last found p(win)
def find_prev_result():
    info = open("/scratch/william/" + sys.argv[1] + "/log.txt", "r").readlines()
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
    sys.stdout=open(file_name,"w+")
    smgPrefix.run(characters)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, False)
    sys.stdout=sys.__stdout__
    # run prism-games with lots of memory, hardcoded extended prism-games location on SAND
    os.system("/scratch/gethin/prism-william/prism/bin/prism -cuddmaxmem 100g -javamaxmem 100g "+file_name+" smg_props.props -prop 4 -s > /scratch/william/" + sys.argv[1] + "/log.txt")
    return find_prev_result()

def generate_strategy(characters, i):
    file = "/scratch/william/" + sys.argv[1] + "/smg" + characters[0] + characters[1] + characters[2] + characters[3] + "_mul.prism"
    sys.stdout = open(file, "w+")
    nu_smgprefix.run(characters, "smg", True)
    nu_free_strat.run(characters, 1)
    nu_free_strat.run(characters, 2)
    suffix.run(characters, True)
    sys.stdout = sys.__stdout__
    os.system("/scratch/gethin/prism-william/prism/bin/prism -cuddmaxmem 100g -javamaxmem 100g "+file+" smg_props.props -prop 4 -s -exportadvmdp tmp.tra -exportstates tmp.sta > /scratch/william/" + sys.argv[1] + "/opt_gen_" + str(i) + ".txt")
    sys.stdout = open("/scratch/william/" + sys.argv[1] + "/candidate_dom_s_" + str(i) + ".txt","w+")
    nu_educate_strat.run(characters, "tmp", 1)
    sys.stdout= sys.__stdout__
    os.system("cat tmp.sta > /scratch/william/" + sys.argv[1] + "/" + characters[0] + characters[1] + characters[2] + characters[3] + ".sta")

# Main: setup
global pairs
os.system("mkdir /scratch/william/" + sys.argv[1])
pairs = [["K","A"],["K","W"],["W","A"]]
for i in range(len(pairs)):
    generate_strategy(pairs[i]+pairs[i],i)
    print "strategy generated for " + str(pairs[i]) + "..."
    res1 = 0
    res2 = 0
    for j in range(1,3):
        # find adversaries of other material against newly generated optimal strategy
        k = (i + j)%3
        file_name = "/scratch/william/" + sys.argv[1] + "/opt" + str(pairs[i][0])+str(pairs[i][1]) + "_vs_adv" + str(pairs[k][0])+str(pairs[k][1]) + ".txt"
        sys.stdout = open(file_name,"w+")
        prefix.run(pairs[i] + pairs[k], "mdp", False)
        sys.stdout = sys.__stdout__
        os.system("cat /scratch/william/" + sys.argv[1] + "/candidate_dom_s_" + str(i) + ".txt >> " + file_name)
        sys.stdout=open(file_name,"a")
        free_strat.run(pairs[i] + pairs[k], 2)
        suffix.run(pairs[i] + pairs[k], False)
        sys.stdout=sys.__stdout__
        os.system("/scratch/gethin/prism-william/prism/bin/prism -cuddmaxmem 100g -javamaxmem 100g " + file_name + " props.props -prop 2 -s > /scratch/william/" + sys.argv[1] + "/log.txt")
        print "optimal strategy can be beaten with a probability of",
        if j == 2:
            res2 = find_prev_result()
            print str(res2), "by the adversary for " + str(pairs[k])
            if res2 > 0.5:
                print "optimal strategy for " + str(pairs[i]) + " is not dominant."
                break
        else:
            res1 = find_prev_result()
            print str(res1), "by the adversary for " + str(pairs[k])
            if res1 > 0.5:
                print "optimal strategy for " + str(pairs[i]) + " is not dominant."
                break                       # Try the next symmetric optimal strat.
    if res1 < 0.5 and res2 < 0.5 and res1 > 0 and res2 > 0:
        print "dominant strategy found for " + str(pairs[i])
        break

print "Check opt_gen_(0-2) to ensure optimal strategies are unique"

# NOT USED:
# def compare_candidate(plr_pair, ignore_pair, t):
#     ret_dict = {}
#     print "Optimal strategy generated, calculating adversarial probabilities..."
#     for p in pairs:
#         if p != ignore_pair:
# 	    ret_dict[str(p)] = []
#             for i in range(2):
#                 if i == 1:                          # Run again with relfected ordering
#                     tmp = [p[1],p[0]]
#                     chars = plr_pair + tmp
#                 else:
#                     chars = plr_pair + p
#                 file_name = "/scratch/william/" + sys.argv[1] + "/cmp"
#                 for char in chars:
#                     file_name += char
#                 file_name += ".prism"
#                 # Generate a prism file to represent SMG of game between both teams
#                 sys.stdout=open(file_name,"w+")
#                 prefix.run(chars, "mdp", False)
#                 sys.stdout = sys.__stdout__
#                 os.system("cat candidate_dom_s_" + str(t) + ".txt >> " + file_name)
#                 sys.stdout=open(file_name,"a")
#                 free_strat.run(chars, 2)
#                 suffix.run(chars, False)
#                 sys.stdout=sys.__stdout__
#                 # run prism-games with lots of memory, hardcoded prism-games location on SAND
#                 os.system("/usr/local/prism-games-2.0.beta3-linux64/bin/prism -cuddmaxmem 300g -javamaxmem 300g "+ file_name + " props.props -prop 2 -s > /scratch/william/" + sys.argv[1] + "/log.txt")
#                 if i == 1:
#                     ret_dict[str(p)] += [find_prev_result()]
#                 else:
#                     ret_dict[str(p)] += [find_prev_result()]
#     # Have dictionary with 2 entries e.g. {"KA": 0.37, 0.53, "WA": 0.45, 0.24}
#     # Need to find the ordering which is worse for each pair (e.g. KA and AW from above)
#
#     dominant_strategy = True
#     for output_pair in ret_dict.keys():
#         dominant = "dominant"
#         if ret_dict[output_pair][0] > 0.50 and ret_dict[output_pair][1] > 0.50:
#             dominant = "not dominant"
#             dominant_strategy = False
#         print "\tAgainst " + output_pair + " the strategy is " + dominant + " with minimum probabilities of winning = " + str(1 - ret_dict[output_pair][0]) + " and " + str(1-ret_dict[output_pair][1])
#     if dominant_strategy:
#         print "\t\tThe optimal strategy for ", plr_pair, "against", ignore_pair, " is a dominant strategy."
#         exit(0)
#     else:
#         print "This is not a dominant strategy."
