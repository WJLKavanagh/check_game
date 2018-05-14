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
            print ",".join(values[:4]) + "," + ",".join(values[-2:])
    return states

def populate_transitions(file):
    return None

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
    return False

def find_command(a,b,c,d,states,transitions):
    if True:
        return "A_B"
    else:
        return None

def print_command(command):
    print "\t\t\t\t1 : (attack' = ", command, ");"

def print_GuardComm(a,b,c,d,t):
    print_guard(a,b,c,d,t)
    comm = find_command(a,b,c,d,t)
    if comm != None:
        print_command(comm)

def print_wGuardComms(a,b,c,d,t):
    return None

def run(characters, file, team):
    global s, info, minD, maxD
    s = {}              # STATE DICTIONARY
    transitions = populate_transitions(file)
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
                        if characters[team*2 - 2] == "W" or characters[team*2 - 1] == "W":
                            print_wGuardComms(a,b,c,d,team)
                        else:
                            print_GuardComm(a,b,c,d,team)
                    else:
                        status[1] += 1
    print "//", status


run(["K","A","K","A"], "tmp", 1)
