import sys, random

# TODO: Fix this to deal with A in pos 1. (generates strategies for act = {1,2,3} not act = {1,3,4})

info = open("char_info.txt", "r").readlines()
chars = []
s = {}              # STATE DICTIONARY

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

def find_health(C):
    return find_attribute(C, "hea")

def act_start(b):
    if not b:
        print "\t[team_1_turn] turn_clock = 1 & attack = 0 &",
    else:
        print "\t[team_2_turn] turn_clock = 2 & attack = 0 &",

def find_index(a):
    for i in s.keys():
        if s[i] == a:
            return i

def reset_stuns(n):
    if n==1:
        return "(a_stun' = false) & (b_stun' = false);"
    else:
        return "(c_stun' = false) & (d_stun' = false);"

def random_action(a,b,c,d,t):
    # What states are there (1-9 depending on wizards)
    wizard_placement = ["W" in team_1, "W" in team_2]
    states = [[a,b,c,d,false,false,false,false]] # no stuns, always reachable.
    if wizard_placement[0] and wizard_placement[1]:       # if wizard on either side:
        states += [[a,b,c,d,true,false,true,false]]
        states += [[a,b,c,d,true,false,false,true]]
        states += [[a,b,c,d,false,true,true,false]]
        states += [[a,b,c,d,false,true,false,true]]
    if wizard_placement[0]:
        states += [[a,b,c,d,false,false,true,false]]
        states += [[a,b,c,d,false,false,false,true]]
    if wizard_placement[1]:
        states += [[a,b,c,d,true,false,false,false]]
        states += [[a,b,c,d,false,true,false,false]]
    # Generate legal actions for player t in each state
    for decision_state in states:
        act_start(b)
        print "a_hea =", decision_state[0], "& b_hea =", decision_state[1], "& c_hea =", decision_state[2],
        print "& d_hea = " + str(decision_state[3]) + " & a_stun = " + str(decision_state[4]) + " & b_stun = " + str(decision_state[5]),
        print "& c_stun = " + str(decision_state[6]) + " & d_stun = " + str(decision_state[7]) + " ->"
        legal_acts = []
        team_chars = team_2
        team_pos = ["C","D"]
        if t == 1:
            team_chars = team_1
            team_pos = ["A","B"]
        for i in range(len(team_chars)):
            pos = (t-1)*2 + i                                                   # index of character in decision_state[]
            if team_chars[i] == "A" and decision_state[pos] > 0 and decision_state[pos+4] == "false":                # ... and player is alive and an archer
                legal_acts += [(2*(i+1))-1]                                     # Add char_opp to possible actions
            elif decision_state[pos] > 0 and decision_state[pos+4] == "false":
                if team_chars == team_2:                                    # Add char_t and char_t+1 if valid.
                    if decision_state[0] > 0:
                        legal_acts += [(2*(i+1))-1]
                    if decision_state[1] > 0:
                        legal_acts += [2*(i+1)]
                else:
                    if decision_state[2] > 0:
                        legal_acts += [(2*(i+1))-1]
                    if decision_state[3] > 0:
                        legal_acts += [2*(i+1)]
        if team_chars == team_2:
            for i in range(len(legal_acts)):
                legal_acts[i]+=4
        # pick one at random and write it out
        if len(legal_acts) > 0:
            print "\t\t1 : (attack' = " + str(random.choice(legal_acts)) + ") &",
            print reset_stuns(t)
        else:
            print "\t\t1 : (attack' = 10) &",
            print reset_stuns(t)

def run(characters, team, pref_move):
    global chars, first_t2, team_2, team_1, states
    chars = []
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

    for a in range(-2, find_health(characters[0]) + 1):
        for b in range(-2, find_health(characters[1]) + 1):
            for c in range(-2, find_health(characters[2]) + 1):
                for d in range(-2, find_health(characters[3]) + 1):
                    if (a > 0 or b > 0) and (c > 0 or d > 0):
                        random_action(a,b,c,d,team)
    print

#USAGE: run(["K","A","K","W"], 2, "None")
