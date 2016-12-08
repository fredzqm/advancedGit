import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tree", help="List of commits", action='append')
parser.add_argument("-o", "--output", help="The name of the branch")
args = parser.parse_args()

def getOutput(command):
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    return [line.decode('utf-8') for line in proc.stdout]

print(args.tree)

com = None
for tree in reversed(args.tree):
    if com == None:
        com = getOutput(['git', 'commit-tree', tree, '-m', 'alternative start'])
    else:
        com = getOutput(['git', 'commit-tree', tree, '-p', com[0][0:-1], '-m', 'alternative follow'])

getOutput(['git', 'update-ref', "refs/heads/"+args.output, com[0][0:-1]]);
