import sys, seed_strat, collections

def populate_state_dictionary(characters):
    global s
    team_1 = [characters[0], characters[1]]
    team_2 = [characters[2], characters[3]]
    states = 2
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
    s[states-1] = "gap_fix"
    s[states] = "next_turn"

def populate_states(file, team):
    states = {}
    for line in open(file+".sta", "r").readlines()[1:]:
        values = line.split("(")[1][:-1].split(",")
        if values[5] == "0" and values[4] == str(team):
            states[line.split("(")[0][:-1]] = ",".join(values[:1]) + "," + values[-1][:-1]
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

def find_max_health():
    global info
    return max(find_health("K"),find_health("A"),find_health("W"))

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

def print_command(command, resets, team):
    comm_val = 0
    for elem in s.keys():
        if s[elem] == command:
            break
        comm_val += 1
    chars = ["a", "b", "c", "d"]
    print "\t\t\t\t1 : (attack' =", str(comm_val) + ") & (" +chars[team*2-2] + "_stun' = false) &",
    print "(" + chars[team*2-1] + "_stun' = false) ;"

def print_GuardComm(a,b,c,d,t):
    print_guard(a,b,c,d,t)
    comm = find_command(a,b,c,d,"false","false")
    print_command(comm, False, t)



def print_wGuardComms(a,b,c,d,t):

    # NEW

    # Find range of states with ABCD



    """         OLD
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
    """


def print_wizardExtras(characters,t):  # What if you're stunned and you haven't encountered this before?
    chars = ["a","b","c","d"]
    ally1 = chars[2*(t-1)]
    ally2 = chars[2*(t-1)+1]
    opp1 = chars[(2-t)*2]
    opp2 = chars[(2-t)*2+1]
    print "// Deal with stuns if unseen "
    for i in range(2):
        character = ally1
        ally = ally2
        if i == 1:
            character = ally2
            ally = ally1
        if characters[2 * (t-1) + i] == "A":     # If the character is an archer and their ally is stunned...
            print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0 & " + character + "_hea",
            print "> 0 & " + character + "_stun = false & " + ally + "_stun = true & (",
            print opp1 + "_hea > 0 | " + opp2 + "_hea > 0) ->"
            print "\t\t\t\t1 : (attack' = " + str(s.keys()[s.values().index(character.upper()+"_opp")]) + ") &",
            print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) ;"
        else:                   # if the character is NOT an archer and their ally is stunned...
                    # if both opponents are alive...
            print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0 & " + character + "_hea",
            print "> 0 & " + character + "_stun = false & " + ally + "_stun = true &",
            print opp1 + "_hea > 0 & " + opp2 + "_hea > 0 ->"
            print "\t\t\t\t0.5 : (attack' = " + str(s.keys()[s.values().index(character.upper()+"_"+opp1.upper())]) + ") &",
            print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) +"
            print "\t\t\t\t0.5 : (attack' = " + str(s.keys()[s.values().index(character.upper()+"_"+opp2.upper())]) + ") &",
            print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) ;"
                    # if only one is alive...
            print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0 & " + character + "_hea",
            print "> 0 & " + character + "_stun = false & " + ally + "_stun = true &",
            print opp1 + "_hea > 0 & " + opp2 + "_hea <= 0 ->"
            print "\t\t\t\t1 : (attack' = " + str(s.keys()[s.values().index(character.upper()+"_"+opp1.upper())]) + ") &",
            print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) ;"
            print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0 & " + character + "_hea",
            print "> 0 & " + character + "_stun = false & " + ally + "_stun = true &",
            print opp1 + "_hea <= 0 & " + opp2 + "_hea > 0 ->"
            print "\t\t\t\t1 : (attack' = " + str(s.keys()[s.values().index(character.upper()+"_"+opp2.upper())]) + ") &",
            print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) ;"
    # If one is alive and the other is dead, then skip..
    print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0 & (" + ally1 + "_hea",
    print "<= 0 & " + ally2 + "_stun = true) | (" + ally1 + "_stun = true &",
    print ally2 + "_hea <= 0) ->"
    print "\t\t\t\t1 : (attack' = " + str(s.keys()[s.values().index("next_turn")]) + ") &",
    print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) ;"

def print_healthExtras(characters,t):
    # what to do if opponents have health > than what we've seen?

    # FIND GAPS
    print "// Gap detection"
    in_order = ["A","B","C","D"]
    gaps = []
    max_health = find_max_health()
    for c in range(len(in_order)):
        for i in range(find_health(characters[c])-1, max_health+1):
            if i != find_health(characters[c]):
                gaps += [in_order[c].lower() + "_hea = " + str(i)]

    # print Guard-comm to send gaps to gap_fixing states

    print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0",
    for c in range(len(gaps)):
        if c == 0:
            print "& (" + gaps[c],
        elif c < len(gaps)-1:
            print "|", gaps[c],
        else:
            print "|", gaps[c] + ") ->"

    print "\t\t\t\t1 : (attack' =", str(s.keys()[s.values().index("gap_fix")]) + ") ;"
    print "// Gap solution"

    # Naive strat from gap_fixing state
    print "// naive with attack = gap_fix "
    seed_strat.run(characters, t, "none", s.keys()[s.values().index("gap_fix")])

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
                        print_wGuardComms(a,b,c,d,team)
                    else:
                        status[1] += 1
    if not against_wizard(characters,team):
        print_wizardExtras(characters, team)
    print_healthExtras(characters,team)
    print "//", status

# run(["K", "A", "K", "W"], "tmp", 1)
