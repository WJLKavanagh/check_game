import sys

def define_constants(c, l):
    for i in range(len(info)):
        if info[i][0] == str(c):
            print "\t//", info[i],
            deets = info[i+1][:-1].split(", ")
            for j in range(len(deets)):
                if deets[j] != "\n":
                    ty = "double"
                    if "." not in info[i+j+2]:
                        ty = "int"
                    print "const", ty, l + "_" + deets[j], "=", info[i+j+2][:-1] + ";"

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
    return int(info[i + index_diff])

def find_health(C):
    return find_attribute(C, "hea")

def find_max_health():
    global info
    return max(find_health("K"),find_health("A"),find_health("W"))

def run(characters, model, multiple):    #USAGE: python prefix.py A B C D model_type
    global info
    info = open("char_info.txt", "r").readlines()
    team_1 = [characters[0], characters[1]]
    team_2 = [characters[2], characters[3]]
    chars = []
    for c in team_1:
        chars += [c]
    for c in team_2:
        chars += [c]

    mD = 0      # MAX DAMAGE
    for c in ["K","W","A"]:
            if find_attribute(c, "dmg") > mD:
                mD = find_attribute(c, "dmg")
    LB = str(1-mD)   # LOWER BOUND FOR HEALTH

    print model                   # DTMC or MDP
    print "\n// TEAM 1"
    define_constants(team_1[0], "A")
    define_constants(team_1[1], "B")
    print "\n// TEAM 2"
    define_constants(team_2[0], "C")
    define_constants(team_2[1], "D")
    max_h = str(find_max_health())
    print "\nmodule game"
    if multiple:
        print "\ta_hea : ["+LB+".."+max_h+"];"
        print "\tb_hea : ["+LB+".."+max_h+"];"
        print "\tc_hea : ["+LB+".."+max_h+"];"
        print "\td_hea : ["+LB+".."+max_h+"];"
        print "\tturn_clock : [0..2];"
        print "\tattack : [0..10];",
    else:
        print "\ta_hea : ["+LB+".."+max_h+"]\tinit A_hea;"
        print "\tb_hea : ["+LB+".."+max_h+"]\tinit B_hea;"
        print "\tc_hea : ["+LB+".."+max_h+"]\tinit C_hea;"
        print "\td_hea : ["+LB+".."+max_h+"]\tinit D_hea;"
        print "\tturn_clock : [0..2]\tinit 0;"
        print "\tattack : [0..10]\tinit 0;",

    print "\t\t\t// Chosen action:\n\t// 0 : NONE,",         # EXPLAIN ATTACK STATES
    states = 10

    curr = 1
    L_p = 0
    L = ["A","B","C","D"]
    for i in range(len(L)):
        if chars[i] == "A":
            print str(curr) + " : " + L[i] + "_opp,",
            print str(curr+1) + " : not_used,",
            curr += 2
            L_p += 2
        elif chars[i] == "W" or chars[i] == "U" or chars[i] == "K" or chars[i] == "P":
            if L_p <= 2:
                print str(curr) + " : " + L[i] + "_C,",
                print str(curr+1) + " : " + L[i] + "_D,",
            else:
                print str(curr) + " : " + L[i] + "_A,",
                print str(curr+1) + " : " + L[i] + "_B,",
            curr+=2
            L_p+=2
    print str(states-1) + " : " + "gap_fix,",
    print str(states) + " : " + "NEXT TURN."
    print "\ta_stun : bool;\n\tb_stun : bool;\n\tc_stun : bool;\n\td_stun : bool;"
    print "\n\t[flip_coin]	turn_clock = 0 ->"
    print "\t\t\t\t0.5 : (turn_clock' = 1) + 0.5 : (turn_clock' = 2);\n"
