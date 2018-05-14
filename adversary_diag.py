import sys

f = open(sys.argv[1], "r").readlines()

print "\nAdvanced strategy generated, diagnostic:", f[-2][3:],
