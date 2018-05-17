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
    f = open("char_prac.txt","r+")
    info = f.readlines()
    num = find_attribute(character, attribute)
    f.close()
    f = open("char_prac.txt", "w")
    for i in range(len(info)):
        if i != num:
             f.write(info[i])
        else:
             f.write(b + "\n")


    f.close()

rewrite("W", "acc", "0.234")
"""

SOMETHING LIKE:

candidates_for_att1 = [7,8,9,10]

for att1 in candidates_for_att1:
    change att1
    for att2 in range(given by input):
        change att2
        for att3 in range(given by input):
            change att3
            DO_SCIENCE()
"""
