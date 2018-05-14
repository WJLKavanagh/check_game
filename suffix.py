import sys

info = open("char_info.txt", "r").readlines()
chars = []
s = {}              # STATE DICTIONARY

def new_action(act):
    if len(act) == 4:
        return act[0] + "_" + act[-1]
    return act[0] + "_opp"

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

def princess_attack(act, i):
    heal_state = -1
    for blah in s.keys():
        if s[blah] == act[0]+"_heal":
            heal_state = blah
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + str(act[-1]).lower() + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + str(act[-1]).lower() + "_hea' = " + str(act[-1]).lower() + "_hea -",
    print str(act[0])[0] + "_dmg) & (attack' = " + str(heal_state) + ") + \n\t\t\t(1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"

def wizard_attack(act, i):
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + str(act[-1]).lower() + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + str(act[-1]).lower() + "_hea' = " + str(act[-1]).lower() + "_hea -",
    print str(act[0])[0] + "_dmg) & (" + str(act[-1]).lower() + "_stun' = true) & (attack' =",
    print str(max(s.keys())) + ") + \n\t\t\t(1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"

def unicorn_attack(act, i):
    print "\t[" + new_action(act) + "] attack = " + str(s.keys()[i]) + " & " + str(act[-1]).lower() + "_hea > 0 ->"
    print "\t\t\t" + str(act)[0] + "_acc : (" + str(act[-1]).lower() + "_hea' = " + str(act[-1]).lower() + "_hea -",
    print str(act[0])[0] + "_dmg) & (" + str(act[-1]).lower() + "_dot' = " + str(act)[0] + "_DoT_dur) & (attack' =",
    print str(max(s.keys())) + ") + \n\t\t\t(1-" + str(act)[0] + "_acc) : (attack' =",
    print str(max(s.keys())) + ");"

def heal_block(act, i):
    friend = "A"
    if act[0] == "A":
        friend = "B"
    elif act[0] == "C":
        friend = "D"
    elif act[0] == "D":
        friend = "C"
    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & " + str(act[0]).lower() + "_hea = " + str(act[0]) + "_hea",
    print "& (" + friend.lower() + "_hea <= 0 | " + friend.lower() + "_hea = " + friend + "_hea) ->\t\t\t\t// none suitable\n\t\t\t(attack' =",
    print str(max(s.keys())) + ");"
    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & " + friend.lower() + "_hea > 0 &",
    print friend.lower() + "_hea < " + friend + "_hea & (" + friend + "_hea - " + friend.lower() + "_hea >",
    print act[0] + "_hea - " + act[0].lower() + "_hea) ->\t\t// heal friend"
    print "\t\t\t"+act[0] + "_heal_acc : (" + friend.lower() + "_hea' = min(" + friend + "_hea, " + friend.lower() + "_hea +",
    print act[0] + "_heal)) & (attack' = " +str(max(s.keys()))+ ") + \n\t\t\t(1-" + act[0] + "_heal_acc) : (attack' = " + str(max(s.keys()))+");"

    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & " + act[0].lower() + "_hea < " + act[0] + "_hea & ( (",
    print friend + "_hea - " + friend.lower() + "_hea <= " + act[0] + "_hea - " + act[0].lower() + "_hea) | " + friend.lower() + "_hea <= 0 )",
    print "->\t// heal self"
    print "\t\t\t"+act[0] + "_heal_acc : (" + act[0].lower() + "_hea' = min(" + act[0] + "_hea, " + act[0].lower() + "_hea +",
    print act[0] + "_heal)) & (attack' = " + str(max(s.keys()))+ ") + \n\t\t\t(1-" + act[0] + "_heal_acc) : (attack' = " + str(max(s.keys()))+");"
    print

def DoT_block(act, i):
    o = ["a", "b"]
    if act[5] == "2":
        o = ["c", "d"]
    exit_state = 0
    if act[5] == "1" and "team_2_DoT" in s.values():
        exit_state = max(s.keys()) - 1
    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & " + o[0] + "_hea > 0 & " + o[0] + "_dot > 0 &",
    print o[1] + "_hea > 0 & " + o[1] + "_dot > 0 ->\t\t// both"
    print "\t\t\t(" + o[0] + "_hea' = " + o[0] + "_hea - 1) & (" + o[0] + "_dot' = " + o[0] + "_dot - 1) &",
    print "(" + o[1] + "_hea' = " + o[1] + "_hea - 1) &\n\t\t\t(" + o[1] + "_dot' = " + o[1] + "_dot - 1) &",
    print "(attack' = " + str(exit_state) + ");"

    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & " + o[0] + "_hea > 0 & " + o[0] + "_dot > 0 &",
    print "("+o[1] + "_hea <= 0 | " + o[1] + "_dot <= 0) ->\t\t// first"
    print "\t\t\t(" + o[0] + "_hea' = " + o[0] + "_hea - 1) & (" + o[0] + "_dot' =",
    print o[0] + "_dot - 1) & (attack' = " + str(exit_state) + ");"

    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & (" + o[0] + "_hea <= 0 | " + o[0] + "_dot <= 0) &",
    print o[1] + "_hea > 0 & " + o[1] + "_dot > 0 ->\t\t// second"
    print "\t\t\t(" + o[1] + "_hea' = " + o[1] + "_hea - 1) & (" + o[1] + "_dot' =",
    print o[1] + "_dot - 1) & (attack' = " + str(exit_state) + ");"

    print "\t[" + str(act) + "] attack = " + str(s.keys()[i]) + " & (" + o[0] + "_hea <= 0 | " + o[0] + "_dot <= 0) &",
    print "("+o[1] + "_hea <= 0 | " + o[1] + "_dot <= 0) ->\t// neither"
    print "\t\t\t(attack' = " + str(exit_state) + ");"
    print

def multiple_initial_health(c):             # GENERATE TO_STRING FOR POSSIBLE CHAR HEALTH VALUES FOR MULTIPLE INITIAL STATES
    ret_s = "( (" + c + "_hea > " + str(-maxD) + " & " + c + "_hea < (" + c.upper() + "_hea-" + str(minD-1) + ") ) | "
    ret_s += c + "_hea = " + c.upper() + "_hea)"
    return ret_s

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
    s[0] = "none"
    curr = 1
    L_p = 0
    L = ["A","B","C","D"]
    for i in range(len(L)):
        if chars[i] == "A":
            s[curr] = L[i] + "->opp"
            curr += 1
            L_p += 1
        elif chars[i] == "W" or chars[i] == "U" or chars[i] == "K" or chars[i] == "P":
            if L_p <= 2:
                s[curr] = L[i] + "->C"
                s[curr+1] = L[i] + "->D"
            else:
                s[curr] = L[i] + "->A"
                s[curr+1] = L[i] + "->B"
            curr+=2
            L_p+=2
    standard_states = curr

    for c in chars:
        if c == "P":         # Princesses require individual healing states
            s[curr] = L[chars.index(c)] + "_heal"
            curr += 1


    if "U" in team_2:        # Unicorns require dot calc.
        s[curr] = "team_1_DoT"
        curr += 1
    if "U" in team_1:
        s[curr] = "team_2_DoT"
        curr += 1

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
    for c in chars:
        if find_attribute(c, "dmg") > maxD:
            maxD = find_attribute(c, "dmg")
    minD = 99   # MIN DAMAGE
    for c in chars:
        if find_attribute(c, "dmg") < minD:
            minD = find_attribute(c, "dmg")


    # INIT values
    if multiple:
        print "init\t\t\t\t\t//MULTIPLE INITIAL STATES"
        for ch in ['a','b','c','d']:
            print "\t" + multiple_initial_health(ch) + " &"
        print "\tattack = 0 & turn_clock = 0 |"
        if "W" in team_2:
            print "\t(attack = 0 & turn_clock = 1 & "
            print "\t(a_stun = false & b_stun = false) |"
            print "\t(a_stun = false & b_stun = true) |"
            print "\t(a_stun = true & b_stun = false) )"
        else:
            print "\t(attack = 0 & turn_clock = 1) |"
        if "W" in team_1:
            print "\t(attack = 0 & turn_clock = 2 & "
            print "\t(c_stun = false & d_stun = false) | "
            print "\t(c_stun = false & d_stun = true) | "
            print "\t(c_stun = true & d_stun = false) )"
            print "\t(attack = 0 & turn_clock = 2) "

    else:
        print "init\t\t\t\t\t//SINGLE INITIAL STATE"
        print "\ta_hea = A_hea & b_hea = B_hea &\n\tc_hea = C_hea & d_hea = D_hea & \n\tattack = 0 & turn_clock = 0"
        if "W" in team_2:
            print "\t& a_stun = false & b_stun = false"
        if "W" in team_1:
            print "\t& c_stun = false & d_stun = false"
    print "endinit\n"

    print 'label "team_1_win" = (a_hea > 0 | b_hea > 0) & (c_hea <= 0 & d_hea <= 0);'
    print 'label "team_2_win" = (c_hea > 0 | d_hea > 0) & (a_hea <= 0 & b_hea <= 0);'
