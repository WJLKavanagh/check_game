import sys

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


def act_start(b):
    if not b:
        print "\t[team_1_turn] turn_clock = 1 & attack = 0 &",
    else:
        print "\t[team_2_turn] turn_clock = 2 & attack = 0 &",

def find_index(a):
    for i in s.keys():
        if s[i] == a:
            return i

def generate_moves(team, opps, n):
    start = 1
    possible_actions = s.values()[start:first_t2]
    op = [2,3]
    if n == 2:
        start = first_t2
        possible_actions = s.values()[first_t2:standard_states]
        op = [0,1]
    Cs = ["A", "B", "C", "D"]
    for act in possible_actions:
        if act == "not_used":
            continue
        act_start(n == 2)
        if act[-3:] != "opp":
            print act[0].lower() + "_hea > 0 & " + act[0].lower()  + "_stun = false & " + act[-1].lower() + "_hea > 0 ->"
        elif act[-3:] == "opp":
            print act[0].lower() + "_hea > 0 & " + act[0].lower()  + "_stun = false & (" + Cs[op[0]].lower() + "_hea > 0 | " + Cs[op[1]].lower() + "_hea > 0) ->"
        print "\t\t\t\t(attack' = " + str(find_index(act)) + ") & (" + Cs[2*(n-1)].lower() + "_stun' = false) & (" + Cs[2*(n-1)+1].lower() + "_stun' = false) ;"
        fr = [possible_actions[0], possible_actions[2]]
    act_start(n==2)
    print "(" + fr[0][0].lower() + "_hea <= 0 | " + fr[0][0].lower() + "_stun  = true) &",
    print "(" + fr[1][0].lower() + "_hea <= 0 | " + fr[1][0].lower() + "_stun = true) ->\n\t\t\t\t",
    print "(attack' = " + str(states) + ") & (" + Cs[2*(n-1)].lower() + "_stun' = false) & (" + Cs[2*(n-1)+1].lower() + "_stun' = false) ;"

def run(characters, team):
    global s, first_t2, standard_states, states
    info = open("char_info.txt", "r").readlines()
    chars = []
    s = {}              # STATE DICTIONARY
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
    #state dict FINISHED

    first_t2 = -1
    for i in range(len(s.values())):
        if s.values()[i][0] == "C":
            first_t2 = i
            break;

    if team == 2:
        generate_moves(team_2, team_1, 2)
    else:
        generate_moves(team_1, team_2, 1)
    print
