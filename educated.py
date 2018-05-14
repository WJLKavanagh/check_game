import sys

def check_wiz(t,a,b,c,d):
    return (t=="1" and (c=="W" or d=="W")) or (t=="2" and (a=="W" or b=="W"))

def find_state(act):
    for i in range(len(s.keys())):
        if s[i] == act:
            return str(i)

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

def is_valid(a,b,c,d):
    if (a <= 0 and b <= 0) or (c <= 0 and d <= 0):
        return False
    for i in range(len([a,b,c,d])):
        if [a,b,c,d][i] > find_attribute(chars[i], "hea") - min_damage and [a,b,c,d][i] < find_attribute(chars[i],"hea"):
            return False
    return True

def print_wGuard(values, team):
    v = values.split(",")
    print "\t[team_" + str(team) + "_turn]\tturn_clock = " + str(team) + " & attack = 0 & a_hea =",
    print v[0], "& b_hea =", v[1], "& c_hea =", v[2], "& d_hea =", v[3],
    friendly = ["a", "b"]       # Friendly units are stunnable
    if "W" in team_1:
        friendly = ["c", "d"]
    print "& " + friendly[0] + "_stun = " + v[4], "&", friendly[1] + "_stun = " + v[5] + " ->"

def find_wCommand(val, team):
    comm = ""
    state_id = processed_states_from_file.keys()[processed_states_from_file.values().index(val)]
    decision_state = transitions[state_id][0]
    comm = transitions[decision_state][1]
    if team == 2 and "W" in team_1:
        print "\t\t\t\t1 : (attack' =", find_state(comm) + ") & (c_stun' = false) & (d_stun' = false);"
    elif team == 1 and "W" in team_2:
        print "\t\t\t\t1 : (attack' =", find_state(comm) + ") & (a_stun' = false) & (b_stun' = false);"
    else:
        print "\t\t\t\t1 : (attack' =", find_state(comm) + ");"

def run(Cs, file, team):
    global s, chars, info, characters, min_damage, max_damage, team_1, team_2, processed_states_from_file, transitions

    trans_path = file + ".tra"
    state_path = file + ".sta"

    tra_f = open(trans_path, "r")
    info = open("char_info.txt", "r").readlines()
    transitions = {}
    processed_states_from_file = {}
    results = []
    diag = [0,0,0,0]
    min_damage = 999

    tra_f.readline()
    for line in tra_f:
        detail = line.split()
        transitions[detail[0]] = [detail[2], detail[4]]

    chars = []
    s = {}              # STATE DICTIONARY

    team_1 = [Cs[0], Cs[1]]
    team_2 = [Cs[2], Cs[3]]

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
            s[curr] = L[i] + "_opp"
            curr += 1
            L_p += 1
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
    #state dict FINISHED

    # CALCULATE MAX/MIN DAMAGE
    for c in chars:
            if find_attribute(c, "dmg") < min_damage:
                min_damage = find_attribute(c, "dmg")
    max_damage = 0
    for c in chars:
            if find_attribute(c, "dmg") > max_damage:
                max_damage = find_attribute(c, "dmg")

    sta_f = open(state_path, "r").readlines()

    for line in sta_f[1:]:
        details = line[:-2].split(":(")[1].split(",")
        # Check relevant state and team
        if details[5] != "0" or details[4] != str(team):
            continue
        health = ",".join(details[0:4])
        full = health + "," + ",".join(details[-2:])
        processed_states_from_file[line.split(":(")[0]] = full

    for a in range(1-max_damage, find_attribute(Cs[0], "hea")+1):
        for b in range(1-max_damage, find_attribute(Cs[1], "hea")+1):
            for c in range(1-max_damage, find_attribute(Cs[2], "hea")+1):
                for d in range(1-max_damage, find_attribute(Cs[3], "hea")+1):
                    if is_valid(a,b,c,d):
                        health_values = ",".join([str(a),str(b),str(c),str(d)])
                        # GUARD_COMMS needed for (no_stun, no_stun), (stun, no_stun) and (no_stun, stun)
                        if (team == 1 and "W" in team_2) or (team == 2 and "W" in team_1):
                            for i in range(3):
                                stuns = ["false","false"]
                                if i > 0:
                                    stuns[i-1] = "true"
                                state_details = health_values + "," + stuns[0] + "," + stuns[1]
                                if state_details in processed_states_from_file.values():
                                    if processed_states_from_file.keys()[processed_states_from_file.values().index(state_details)] in transitions:
                                        print_wGuard(state_details, team)
                                        find_wCommand(state_details, team)
                                        diag[0] += 1
                                    else:
                                        diag[3] += 1
                                else:
                                    diag[1] += 1
                        else:
                            for i in range(3):
                                stuns = ["false","false"]
                                if i > 0:
                                    stuns[i-1] = "true"
                                state_details = health_values + "," + stuns[0] + "," + stuns[1]
                                if state_details in processed_states_from_file.values():
                                    if processed_states_from_file.keys()[processed_states_from_file.values().index(state_details)] in transitions:
                                        print_wGuard(state_details, team)
                                        find_wCommand(state_details, team)
                                        diag[0] += 1
                                    else:
                                        diag[3] += 1
                                else:
                                    diag[1] += 1
                    else:
                        diag[2] += 1

    print "\n// PURE: " + str(diag[0]) + ", OTHER: " + str(diag[1]) + " MISSED: " + str(diag[2]) + " TRANS_MISS: " + str(diag[3]) + "\n"
