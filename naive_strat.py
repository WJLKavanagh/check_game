import sys

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

team_1 = [sys.argv[1], sys.argv[2]]
team_2 = [sys.argv[3], sys.argv[4]]

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

first_t2 = -1
for i in range(len(s.values())):
    if s.values()[i][0] == "C":
        first_t2 = i
        break;

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
        return "(a_stun' = false) & (b_stun' = false)"
    else:
        return "(c_stun' = false) & (d_stun' = false)"


def generate_moves(team, opps, n):
    start = 1
    possible_actions = s.values()[start:first_t2]
    op = [0,1]
    if n == 2:
        start = first_t2
        possible_actions = s.values()[first_t2:standard_states]
        op = [2,3]
    act_start(n==2)

    # 0 elims
    print "a_hea > 0 & b_hea > 0 & c_hea > 0 & d_hea > 0",
    if "W" in opps and n == 1:
        print "& a_stun = false & b_stun = false",
    elif "W" in opps and n == 2:
        print "& c_stun = false & d_stun = false",
    print "->\n\t\t\t\t",
    to_disp = []
    for c in team:
        if c != "A":
            to_disp += [start]
            to_disp += [start + 1]
            start = start + 2
        else:
            to_disp += [start]
            start = start + 1
    for i in range(len(to_disp)):
        if "W" in opps:
            print "1/" + str(len(to_disp)) + " : (attack' = " + str(to_disp[i]) + ") & " + reset_stuns(n),
        else:
            print "1/" + str(len(to_disp)) + " : (attack' = " + str(to_disp[i]) + ")",
        if i < len(to_disp) - 1:
            print "+\n\t\t\t\t",
        else:
            print ";"

    # 1 elim
    for it in range(4):
        Cs = ["A", "B", "C", "D"]
        truth = [True, True, True, True]
        truth[it] = False
        act_start(n==2)
        if "W" in opps:
            if n==2:
                for i in range(2):
                    if truth[i]:
                        print Cs[i].lower() + "_hea > 0",
                    else:
                        print Cs[i].lower() + "_hea <= 0",
                    if i < len(truth)-1:
                        print "&",
                for i in range(2,4):
                    if truth[i]:
                        print Cs[i].lower() + "_hea > 0 & " + Cs[i].lower() + "_stun = false",
                    else:
                        print "(" + Cs[i].lower() + "_hea <= 0 | " + Cs[i].lower() + "_stun = true)",
                    if i < len(truth)-1:
                        print "&",
            else:
                for i in range(2):
                    if truth[i]:
                        print Cs[i].lower() + "_hea > 0 & " + Cs[i].lower() + "_stun = false",
                    else:
                        print "(" + Cs[i].lower() + "_hea <= 0 | " + Cs[i].lower() + "_stun = true)",
                    if i < len(truth)-1:
                        print "&",
                for i in range(2,4):
                    if truth[i]:
                        print Cs[i].lower() + "_hea > 0",
                    else:
                        print Cs[i].lower() + "_hea <= 0",
                    if i < len(truth)-1:
                        print "&",
        else:
            for i in range(len(truth)):
                if truth[i]:
                    print Cs[i].lower() + "_hea > 0",
                else:
                    print Cs[i].lower() + "_hea <= 0",
                if i < len(truth)-1:
                    print "&",
        print "->\n\t\t\t\t",
        legal_acts = []
        for action in possible_actions:
            if action[-3:] == "opp":
                if truth[Cs.index(action[0])]:
                    legal_acts += [action]
            elif action[1] == "_":
                if truth[Cs.index(action[0])] and truth[Cs.index(action[-1])]:
                    legal_acts += [action]
        for i in range(len(legal_acts)):
            target = str(find_index(legal_acts[i]))
            if "W" in opps:
                print "1/" + str(len(legal_acts)) + " : (attack' = " + target + ") & " + reset_stuns(n),
            else:
                print "1/" + str(len(legal_acts)) + " : (attack' = " + target + ")",
            if i < len(legal_acts) - 1:
                print "+\n\t\t\t\t",
            else:
                print ";"

    # 2 elims
    for first_it in range(2):
        for second_it in range(2):
            Cs = ["A", "B", "C", "D"]
            truth = [True, True, True, True]
            truth[first_it] = False
            truth[second_it+2] = False
            act_start(n==2)
            if "W" in opps:
                if n==2:
                    for i in range(2):
                        if truth[i]:
                            print Cs[i].lower() + "_hea > 0",
                        else:
                            print Cs[i].lower() + "_hea <= 0",
                        if i < len(truth)-1:
                            print "&",
                    for i in range(2,4):
                        if truth[i]:
                            print Cs[i].lower() + "_hea > 0 & " + Cs[i].lower() + "_stun = false",
                        else:
                            print "(" + Cs[i].lower() + "_hea <= 0 | " + Cs[i].lower() + "_stun = true)",
                        if i < len(truth)-1:
                            print "&",
                else:
                    for i in range(2):
                        if truth[i]:
                            print Cs[i].lower() + "_hea > 0 & " + Cs[i].lower() + "_stun = false",
                        else:
                            print "(" + Cs[i].lower() + "_hea <= 0 | " + Cs[i].lower() + "_stun = true)",
                        if i < len(truth)-1:
                            print "&",
                    for i in range(2,4):
                        if truth[i]:
                            print Cs[i].lower() + "_hea > 0",
                        else:
                            print Cs[i].lower() + "_hea <= 0",
                        if i < len(truth)-1:
                            print "&",
            else:
                for i in range(len(truth)):
                    if truth[i]:
                        print Cs[i].lower() + "_hea > 0",
                    else:
                        print Cs[i].lower() + "_hea <= 0",
                    if i < len(truth)-1:
                        print "&",
            print "->\n\t\t\t\t",
            legal_acts = []
            for action in possible_actions:
                if action[-3:] == "opp":
                    if truth[Cs.index(action[0])] and (truth[op[0]] or truth[op[1]]):
                        legal_acts += [action]
                elif action[1] == "_":
                    if truth[Cs.index(action[0])] and truth[Cs.index(action[-1])]:
                        legal_acts += [action]
            for i in range(len(legal_acts)):
                target = str(find_index(legal_acts[i]))
                if "W" in opps:
                    print "1 : (attack' = " + target + ") & " + reset_stuns(n),
                else:
                    print "1 : (attack' = " + target + ")",
                if i < len(legal_acts) - 1:
                    print "+\n\t\t\t\t",
                else:
                    print ";"

    if "W" in opps:
        te = ["a", "b"]
        act_start(n==2)
        if team == team_2:
            te = ["c", "d"]
        print "(" + te[0] + "_hea <= 0 & " + te[1] + "_stun = true) | (" +te[1] + "_hea <= 0 & " + te[0] + "_stun = true) ->"
        print "\t\t\t\t1 : (attack' = " + str(states) + ") & " + reset_stuns(n) + " ;"


team = sys.argv[5]
if team == "2":
    generate_moves(team_2, team_1, 2)
else:
    generate_moves(team_1, team_2, 1)

print
