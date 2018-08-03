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
            curr += 1
            L_p += 1
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
    print "\ta_hea : ["+LB+"..A_hea];"
    print "\tb_hea : ["+LB+"..B_hea];"
    print "\tc_hea : ["+LB+"..C_hea];"
    print "\td_hea : ["+LB+"..D_hea];"
    print "\tturn_clock : [0..2];"

    states = 1
    for entry in chars:
        if entry == "A":
            states += 1
        elif entry == "W":
            states += 2
        elif entry == "P":
            states += 3
        elif entry == "K":
            states += 2
        elif entry == "U":
            states += 3
    print "\tattack : [0.." + str(states) + "];\t\t\t// Chosen action:\n\t// 0 : NONE,",         # EXPLAIN ATTACK STATES
    curr = 1
    L_p = 0
    L = ["A","B","C","D"]
    for i in range(len(L)):
        if chars[i] == "A":
            print str(curr) + " : " + L[i] + "_opp,",
            curr += 1
            L_p += 1
        elif chars[i] == "W" or chars[i] == "U" or chars[i] == "K" or chars[i] == "P":
            if L_p <= 2:
                print str(curr) + " : " + L[i] + "_C,",
                print str(curr+1) + " : " + L[i] + "_D,",
            else:
                print str(curr) + " : " + L[i] + "_A,",
                print str(curr+1) + " : " + L[i] + "_B,",
            curr+=2
            L_p+=2

    # BASIC RELATIONSHIPS DONE

    for c in chars:
        if c == "P":         # Princesses require individual healing states
            print str(curr) + " : " + L[chars.index(c)] + "_heal,",
            curr += 1

    if "U" in team_2:        # Unicorns require dot calc.
        print str(curr) + " : team_1_DoT,",
        curr += 1
    if "U" in team_1:
        print str(curr) + " : team_2_DoT,",
        curr += 1

    print str(states) + " : " + "NEXT_TURN."

    # ADV RELATIONSHIPS DONE
    """
    if "W" in team_2:
        print "\ta_stun : bool;\n\tb_stun : bool;";
    if "W" in team_1:
        print "\tc_stun : bool;\n\td_stun : bool;"
        """

    if "U" in team_1 or "W" in team_1 or "U" in team_2 or "W" in team_2:
        print

    print "\ta_stun : bool;\n\tb_stun : bool;\n\tc_stun : bool;\n\td_stun : bool;";

    if "U" in team_2:
        print "\ta_dot : [0.." + info[17][0] + "] init 0;\n\tb_dot : [0.." + info[17][0] + "] init 0;"
    if "U" in team_1:
        print "\tc_dot : [0.." + info[17][0] + "] init 0;\n\td_dot : [0.." + info[17][0] + "] init 0;"

    print "\n\t[flip_coin]	turn_clock = 0 ->"
    print "\t\t\t\t0.5 : (turn_clock' = 1) + 0.5 : (turn_clock' = 2);\n"
