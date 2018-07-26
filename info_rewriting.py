import sys

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
    return i + index_diff

def rewrite(character, attribute, b):
    global info
    f = open("char_info.txt","r+")
    info = f.readlines()
    num = find_attribute(character, attribute)
    f.close()
    f = open("char_info.txt", "w")
    for i in range(len(info)):
        if i != num:
             f.write(info[i])
        else:
             f.write(b + "\n")
    f.close()

def readsource():
    f = open("source.csv", "r+")
    attributes = f.readline().split(",")
    nums = f.readlines()
    f.close()
    f.open("source.csv", "w")
    f.readline()
    lines_read = 0
    for line in f.readlines():
        if len num.split(",") < 10:
            lines_read = lines_read + 1
            continue
        for i in range(9):
            rewrite(attrib[i][0], attrib[i][2:], attributes[i]
        # OTHERWISE: we need to process the line...

        # Calculate OPtimal values for either player

        # If they are within acceptable bounds:
            # Then interate up to 10 times

            # ELSE don't bother

        # Rewrite the line, with the optimal values, iterated values and 'total', all comma-seperated.
        # move to next line (this requires no code, it's a for-loop)




for a in K_acc_range:
    rewrite("K", "acc", a)
    for b in W_acc_range:
        rewrite("W", "acc", b)
        for c in A_acc_range:
            rewrite("A", "acc", c)

"""
