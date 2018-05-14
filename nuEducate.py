import sys

def populate_state_dictionary(characters):
    global s
    team_1 = [characters[0], characters[1]]
    team_2 = [characters[2], characters[3]]
    states = 1
    for entry in characters:
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
        if characters[i] == "A":
            s[curr] = L[i] + "_opp"
            curr += 1
            L_p += 1
        elif characters[i] == "W" or characters[i] == "U" or characters[i] == "K" or characters[i] == "P":
            if L_p <= 2:
                s[curr] = L[i] + "_C"
                s[curr+1] = L[i] + "_D"
            else:
                s[curr] = L[i] + "_A"
                s[curr+1] = L[i] + "_B"
            curr+=2
            L_p+=2
    standard_states = curr

    for c in characters:
        if c == "P":         # Princesses require individual healing states
            s[curr] = L[characters.index(c)] + "_heal"
            curr += 1

    if "U" in team_2:        # Unicorns require dot calc.
        s[curr] = "team_1_DoT"
        curr += 1
    if "U" in team_1:
        s[curr] = "team_2_DoT"
        curr += 1
    s[states] = "next_turn"

def populate_states(file, team):
    states = {}
    for line in open(file+".sta", "r").readlines()[1:]:
        values = line.split("(")[1][:-2].split(",")
        if values[5] == "0" and values[4] == str(team):
            states[line.split("(")[0]] = ",".join(values[:4]) + "," + ",".join(values[-2:])
    return states

def against_wizard(characters, team):
    return (team == 1 and ("W" in characters[2:])) or (team == 2 and ("W") in characters[:2])

def relevant_transition(team, action):
    pos = ["A","B","C","D"]
    return (action[0] in pos[(2*team) - 2 : team*2] and action[1] == "_") or action == "team_" + str(team) + "_turn" or action == "next_turn"

def populate_transitions(file, team):
    transitions = {}
    tra_f = open(file+".tra", "r")
    tra_f.readline()
    for line in tra_f:
        detail = line.split()
        if relevant_transition(team, detail[4]):
            transitions[detail[0]] = [detail[2],detail[4]]
    return transitions

def find_min_max_damage(characters):
    min_damage = 999
    max_damage = 0
    for c in characters:
            if find_attribute(c, "dmg") < min_damage:
                min_damage = find_attribute(c, "dmg")
    max_damage = 0
    for c in characters:
            if find_attribute(c, "dmg") > max_damage:
                max_damage = find_attribute(c, "dmg")
    return min_damage, max_damage

def find_attribute(C, attribute):
    global info
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

def is_valid(a,b,c,d,characters):
    global minD, maxD
    if (a <= 0 and b <= 0) or (c <= 0 and d <= 0):
        return False
    for i in range(len([a,b,c,d])):
        if [a,b,c,d][i] > find_health(characters[i]) - minD and [a,b,c,d][i] < find_health(characters[i]):
            return False
    return True

def print_guard(a,b,c,d,t):
    print "\t[team_" + str(t) + "_turn]\tturn_clock = " + str(t) + " & attack = 0 & a_hea =",
    print a, "& b_hea =", b, "& c_hea =", c, "& d_hea =", d, "->"

def print_wGuard(a,b,c,d,t,s1,s2):
    chars = ["a","b","c","d"]
    print "\t[team_" + str(t) + "_turn]\tturn_clock = " + str(t) + " & attack = 0 & a_hea =",
    print a, "& b_hea =", b, "& c_hea =", c, "& d_hea =", d, "&", chars[t*2-2] + "_stun =", s1,
    print "&", chars[t*2-1] + "_stun =", s2, "->"

def find_command(a,b,c,d,s1,s2):
    state_description = ",".join([str(a),str(b),str(c),str(d),s1,s2])
    state_id = states.keys()[states.values().index(state_description)][:-1]
    dec_state_id = transitions[state_id][0]
    return transitions[dec_state_id][1]
    """if s1 == s2 and s1 == "false":
        return transitions[dec_state_id][1]
    if dec_state_id in transitions.keys():
        return transitions[dec_state_id][1]
    return None"""

def print_command(command, resets, team):
    comm_val = 0
    for elem in s.keys():
        if s[elem] == command:
            break
        comm_val += 1
    if resets:
        chars = ["a", "b", "c", "d"]
        print "\t\t\t\t1 : (attack' =", str(comm_val) + ") & (" +chars[team*2-2] + "_stun' = false) &",
        print "(" + chars[team*2-1] + "_stun' = false) ;"
    else:
        print "\t\t\t\t1 : (attack' =", str(comm_val) + ") ;"

def print_GuardComm(a,b,c,d,t):
    print_guard(a,b,c,d,t)
    comm = find_command(a,b,c,d,"false","false")
    print_command(comm, False, t)

def print_wGuardComms(a,b,c,d,t):
    comm = find_command(a,b,c,d,"false","false")
    if comm != None:
        print_wGuard(a,b,c,d,t,"false","false")
        print_command(comm, True, t)
    comm = find_command(a,b,c,d,"false","true")
    if comm != None:
        print_wGuard(a,b,c,d,t,"false","true")
        print_command(comm, True, t)
    comm = find_command(a,b,c,d,"true","false")
    if comm != None:
        print_wGuard(a,b,c,d,t,"true","false")
        print_command(comm, True, t)

def run(characters, file, team):
    global s, info, minD, maxD, states, transitions
    s = {}              # STATE DICTIONARY
    transitions = populate_transitions(file,team)
    states = populate_states(file,team)
    status = [0,0]
    info = open("char_info.txt", "r").readlines()
    populate_state_dictionary(characters)
    minD, maxD = find_min_max_damage(characters)
    for a in range(1-maxD, find_health(characters[0]) +1):
        for b in range(1-maxD, find_health(characters[1]) +1):
            for c in range(1-maxD, find_health(characters[2]) +1):
                for d in range(1-maxD, find_health(characters[3]) +1):
                    if is_valid(a,b,c,d,characters):
                        status[0] += 1
                        if against_wizard(characters, team):
                            print_wGuardComms(a,b,c,d,team)
                        else:
                            print_GuardComm(a,b,c,d,team)
                    else:
                        status[1] += 1
    print "//", status

# run(["K", "A", "K", "W"], "tmp", 1)
