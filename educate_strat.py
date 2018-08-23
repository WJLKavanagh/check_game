import sys, collections

def populate_state_dictionary(characters):
    global s
    team_1 = [characters[0], characters[1]]
    team_2 = [characters[2], characters[3]]
    states = 10
    s[0] = "none"
    curr = 1
    L_p = 0
    L = ["A","B","C","D"]
    for i in range(len(L)):
        if characters[i] == "A":
            s[curr] = L[i] + "_opp"
            s[curr+1] = "not_used"
            curr += 2
            L_p += 2
        elif characters[i] == "W" or characters[i] == "K":
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

def populate_states(file, team):
    states = {}
    for line in open(file+".sta", "r").readlines()[1:]:
        values = line.split("(")[1][:-1].split(",")
        if values[5] == "0" and values[4] == str(team):
            states[line.split("(")[0][:-1]] = ",".join(values).split(")")[0]
    return collections.OrderedDict(sorted(states.items(), key=lambda t: t[1]))

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
    for c in ["K","W","A"]:
            if find_attribute(c, "dmg") < min_damage:
                min_damage = find_attribute(c, "dmg")
    max_damage = 0
    for c in ["K","W","A"]:
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

def is_valid(state_info, characters):
    global minD, maxD
    state_info = state_info.split(",")
    a = int(state_info[0])
    b = int(state_info[1])
    c = int(state_info[2])
    d = int(state_info[3])
    a_stun = (state_info[6] == "true")
    b_stun = (state_info[7] == "true")
    c_stun = (state_info[8] == "true")
    d_stun = (state_info[9] == "true")
    if ((a <= 0 or a_stun) and (b <= 0 or b_stun)) or ((c <= 0 or c_stun) and (d <= 0 or d_stun)):
        return False
    return True

def print_guard(values):
    # a,b,c,d,t,a,aS,bS,cS,dS
    list_of_values = values.split(",")
    print "\t[team_" + list_of_values[4] + "_turn]\tturn_clock = " + list_of_values[4] + " & attack = 0",
    print "& a_hea =", list_of_values[0], "& b_hea =", list_of_values[1],
    print "& c_hea =", list_of_values[2], "& d_hea =", list_of_values[3],
    print "&\n\t\t\ta_stun =", list_of_values[6], "& b_stun =", list_of_values[7],
    print "& c_stun =", list_of_values[8], "& d_stun =", list_of_values[9],
    print "->"

def print_command(from_state):
    dec_state = transitions[from_state][0]
    comm_str = transitions[dec_state][1]
    comm_val = 0
    for elem in s.keys():
        if s[elem] == comm_str:
            break
        comm_val += 1
    ally = ["c", "d"]
    if states[from_state].split(",")[4] == "1":     # If t == 1:
        ally = ["a", "b"]
    print "\t\t\t\t1 : (attack' = " + str(comm_val) + ") & (" + ally[0] + "_stun' = false) & (" + ally[1] + "_stun' = false) ;"

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
        # If one is stunned and the other is dead, then skip..
        print "\t[team_"+str(t)+"_turn]\tturn_clock = " + str(t) + " & attack = 0 & (" + ally1 + "_hea",
        print "<= 0 & " + ally2 + "_stun = true) | (" + ally1 + "_stun = true &",
        print ally2 + "_hea <= 0) ->"
        print "\t\t\t\t1 : (attack' = " + str(s.keys()[s.values().index("next_turn")]) + ") &",
        print "(" + character + "_stun' = false) & (" + ally + "_stun' = false) ;"

def run(characters, file, team):
    global s, info, minD, maxD, states, transitions
    s = {}              # STATE DICTIONARY
    transitions = populate_transitions(file,team)
    states = populate_states(file,team)
    info = open("char_info.txt", "r").readlines()
    populate_state_dictionary(characters)
    minD, maxD = find_min_max_damage(characters)
    for line in states:
        if is_valid(states[line], characters):
            print_guard(states[line])
            print_command(line)
    print_wizardExtras(characters, team)
    print
# USAGE: run(["K", "A", "K", "W"], "tmp", 1)
