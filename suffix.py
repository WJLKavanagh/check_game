import sys

info = open("char_info.txt", "r").readlines()
chars = []
s = {}              # STATE DICTIONARY

def new_action(act):
    return act

def find_char(act):
    global chars
    pos = act[0]
    if pos == "A":
        return chars[0]
    elif pos == "B":
        return chars[1]
    elif pos == "C":
        return chars[2]
    elif pos == "D":
        return chars[3]

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

def knight_attack(act, i):
    global s
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + str(act[-1]).lower() + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + str(act[-1]).lower() + "_hea' = " + str(act[-1]).lower() + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(max(s.keys())) + ") + (1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"

def archer_attack(act, i):
    global s
    opps = ["c", "d"]
    if act[0] == "C" or act[0] == "D":
        opps = ["a", "b"]
    # opp1 and opp 2 alive:
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + opps[0] + "_hea > 0 & " + opps[1] + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc * " + str(act)[0] + "_acc : (" + opps[0] + "_hea' = " + opps[0] + "_hea -",
    print str(act[0])[0] + "_dmg) & (" + opps[1] + "_hea' = " + opps[1] + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(max(s.keys())) + ") +"
    print "\t\t\t" + str(act)[0] + "_acc * (1-" + str(act)[0] + "_acc) : (" + opps[0] + "_hea' = " + opps[0] + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(max(s.keys())) + ") +"
    print "\t\t\t" + str(act)[0] + "_acc * (1-" + str(act)[0] + "_acc) : (" + opps[1] + "_hea' = " + opps[1] + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(max(s.keys())) + ") +"
    print "\t\t\t(1-" + str(act)[0] + "_acc) * (1-" + str(act)[0] + "_acc) : (attack' = " + str(max(s.keys())) + ");"
    # opp1 is alive, opp2 is dead
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + opps[0] + "_hea > 0 & " + opps[1] + "_hea <= 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + opps[0] + "_hea' = " + opps[0] + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(max(s.keys())) + ") + (1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"
    # opp2 & !opp1
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + opps[0] + "_hea <= 0 & " + opps[1] + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + opps[1] + "_hea' = " + opps[1] + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(max(s.keys())) + ") + (1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"

def wizard_attack(act, i):
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + str(act[-1]).lower() + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + str(act[-1]).lower() + "_hea' = " + str(act[-1]).lower() + "_hea -",
    print str(act[0])[0] + "_dmg) & (" + str(act[-1]).lower() + "_stun' = true) & (attack' =",
    print str(max(s.keys())) + ") + \n\t\t\t(1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"

def multiple_initial_health(c):             # GENERATE TO_STRING FOR POSSIBLE CHAR HEALTH VALUES FOR MULTIPLE INITIAL STATES
    ret_s = "(" + c + "_hea > " + str(-maxD) + " & " + c + "_hea < " + str(find_max_health()+1) + ")"
    return ret_s

def find_health(C):
    return find_attribute(C, "hea")

def find_max_health():
    global info
    return max(find_health("K"),find_health("A"),find_health("W"))

def run(characters, multiple):
    global chars, s, maxD, minD

    chars = []
    s = {}

    team_1 = [characters[0], characters[1]]
    team_2 = [characters[2], characters[3]]

    for c in team_1:
        chars += [c]
    for c in team_2:
        chars += [c]

    states = 10
    s[0] = "none"
    curr = 1
    L_p = 0
    L = ["A","B","C","D"]
    for i in range(len(L)):
        if chars[i] == "A":
            s[curr] = L[i] + "_opp"
            s[curr+1] = "not_used"
            curr += 2
            L_p += 2
        elif chars[i] == "W" or chars[i] == "U" or chars[i] == "K" or chars[i] == "P":
            if L_p <= 2:
                s[curr] = L[i] + "_C"
                s[curr+1] = L[i] + "_D"
            else:
                s[curr] = L[i] + "_A"
                s[curr+1] = L[i] + "_B"
            curr+=2
            L_p+=2
    standard_states = curr
    s[states-1] = "gap_fix"
    s[states] = "next_turn"

    # STATE DICTIONARY FINISHED
    # standard attack blocks
    i = 0
    for entry in s.keys()[1:standard_states]:
        i = i + 1
        if find_char(s[entry]) == "K":
            knight_attack(s[entry], i)
        elif find_char(s[entry]) == "P":
            princess_attack(s[entry], i)
        elif find_char(s[entry]) == "U":
            unicorn_attack(s[entry], i)
        elif find_char(s[entry]) == "W":
            wizard_attack(s[entry], i)
        elif find_char(s[entry]) == "A":
            archer_attack(s[entry], i)

    print
    #advanced blocks

    for entry in s.keys()[standard_states:]:
        i = i + 1
        if "heal" in s[entry]:
            heal_block(s[entry], i)
        elif "DoT" in s[entry]:
            DoT_block(s[entry], i)

    final = max(s.keys())
    dot_state = "0"
    if "team_1_DoT" in s.values() and "team_2_DoT" in s.values():
        dot_state = str(final-2)
    elif "team_1_DoT" in s.values() or "team_2_DoT" in s.values():
        dot_state = str(final-1)
    print "\t[next_turn] attack = " + str(final) + " & turn_clock > 0 & (a_hea > 0 | b_hea > 0) & (c_hea > 0 | d_hea > 0) ->"
    print "\t\t\t(turn_clock' = 3 - turn_clock) & (attack' = 0);\n"

    print "endmodule\n"

    maxD = 0      # MAX DAMAGE
    for c in ["K","W","A"]:
        if find_attribute(c, "dmg") > maxD:
            maxD = find_attribute(c, "dmg")
    minD = 99   # MIN DAMAGE
    for c in ["K","W","A"]:
        if find_attribute(c, "dmg") < minD:
            minD = find_attribute(c, "dmg")


    # INIT values
    if multiple:
        print "init\t\t\t\t\t//MULTIPLE INITIAL STATES"
        for ch in ['a','b','c','d']:
            print "\t" + multiple_initial_health(ch) + " &"
        print "\tattack = 0 & (turn_clock = 1 | turn_clock = 2) & "
        print "\t( (a_stun = false & b_stun = false) |"
        print "\t(a_stun = false & b_stun = true) |"
        print "\t(a_stun = true & b_stun = false) ) &"
        print "\t( (c_stun = false & d_stun = false) |"
        print "\t(c_stun = false & d_stun = true) |"
        print "\t(c_stun = true & d_stun = false) )"
        print "endinit\n"
    else:
        print "//SINGLE INITIAL STATE"

    print 'label "team_1_win" = (a_hea > 0 | b_hea > 0) & (c_hea <= 0 & d_hea <= 0);'
    print 'label "team_2_win" = (c_hea > 0 | d_hea > 0) & (a_hea <= 0 & b_hea <= 0);'
