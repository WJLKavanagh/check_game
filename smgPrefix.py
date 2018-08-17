import sys

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

def run(characters):
    global info
    info = open("char_info.txt", "r").readlines()
    team_1 = [characters[0], characters[1]]
    team_2 = [characters[2], characters[3]]
    chars = characters

    mD = 0      # MAX DAMAGE
    for c in chars:
            if find_attribute(c, "dmg") > mD:
                mD = find_attribute(c, "dmg")

    LB = str(1-mD)   # LOWER BOUND FOR HEALTH

    print "smg"
    print "\n// TEAM 1"
    define_constants(team_1[0], "A")
    define_constants(team_1[1], "B")
    print "\n// TEAM 2"
    define_constants(team_2[0], "C")
    define_constants(team_2[1], "D")

    # DEFINE PLAYERS

    print "\nplayer p1\n\t[team_1_turn]\nendplayer\n\nplayer p2\n\t[team_2_turn]\nendplayer\n\nplayer sys\n\t[flip_coin],",
    curr = 1
    L_p = 0
    L = ["A","B","C","D"]
    for i in range(len(L)):
        if chars[i] == "A":
            print "[" + L[i] + "_opp],",
            curr += 2
            L_p += 2
        elif chars[i] == "W" or chars[i] == "U" or chars[i] == "K" or chars[i] == "P":
            if L_p <= 2:
                print "[" + L[i] + "_C],",
                print "[" + L[i] + "_D],",
            else:
                print "[" + L[i] + "_A],",
                print "[" + L[i] + "_B],",
            curr+=2
            L_p+=2

    print "[next_turn]\nendplayer\n"

    print "\nmodule game"
    print "\ta_hea : ["+LB+"..A_hea] init A_hea;"
    print "\tb_hea : ["+LB+"..B_hea] init B_hea;"
    print "\tc_hea : ["+LB+"..C_hea] init C_hea;"
    print "\td_hea : ["+LB+"..D_hea] init D_hea;"
    print "\tturn_clock : [0..2] init 0;"

    states = 10
    print "\tattack : [0.." + str(states) + "] init 0;\t\t\t// Chosen action:\n\t// 0 : NONE,",         # EXPLAIN ATTACK STATES
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

    print "\ta_stun : bool;\n\tb_stun : bool;\n\tc_stun : bool;\n\td_stun : bool;";

    print "\n\t[flip_coin]	turn_clock = 0 ->"
    print "\t\t\t\t0.5 : (turn_clock' = 1) + 0.5 : (turn_clock' = 2);\n"
