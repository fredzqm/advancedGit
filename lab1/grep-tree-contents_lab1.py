import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tree", help="Hash of a tree")
parser.add_argument("-s", "--search-term", help="The string to search for")
args = parser.parse_args()

def getOutput(command):
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    return [line.decode('utf-8') for line in proc.stdout]

def parseTreeLine(treeLine):
    ls = treeLine.split(" ")
    ls2 = ls[2].split("\t")
    return ls[1] == "tree", ls2[0]

def printResult(match):
    print(match, end='')

def processBlob(root_sha, search_string):
    output = getOutput(["git", "cat-file", "-p", root_sha])
    for line in output:
        if search_string in line:
            printResult(line)

def processTree(root_sha, search_string):
    output = getOutput(["git", "cat-file", "-p", root_sha])
    for line in output:
        isTree, sha = parseTreeLine(line)
        if isTree:
            processTree(sha, search_string)
        else:
            processBlob(sha, search_string)

processTree(args.tree, args.search_term)
