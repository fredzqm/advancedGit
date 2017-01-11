import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--use", help="to use this commit")
parser.add_argument("-c", "--commentify", help="to have this commit's content in comments")
parser.add_argument("-b", "--branch", help="the branch to save in")
parser.add_argument("-p", "--prefix", help="the prefix for the comment")
args = parser.parse_args()

def getOutput(command):
    proc = subprocess.Popen(command, stdout = subprocess.PIPE)
    return [line for line in proc.stdout]


NO_CONFLICT = 1
OURS = 2
THEIRS = 3
def processConflictFile(file, prefix):
	print(file)
	getOutput(['mv', file, file+'.old'])
	read = open(file+'.old', 'r')
	write = open(file, 'w')
	mode = NO_CONFLICT
	for f in read:
		if mode == NO_CONFLICT:
			if f.startswith('<<<<<<<'):
				mode = OURS
			else:
				write.write(f)
		elif mode == OURS:
			if f.startswith('======='):
				mode = THEIRS
			else:
				write.write(f)
		elif mode == THEIRS:
			if f.startswith('>>>>>>>'):
				mode = NO_CONFLICT
			else:
				write.write(prefix + f)
	read.close()
	write.close()
	getOutput(['rm', file+'.old'])

getOutput(['git', 'checkout', args.use, '-b', args.branch])
getOutput(['git', 'merge', args.commentify])

conflicts = [x.strip() for x in getOutput(['git', 'diff', '--name-only', '--diff-filter=U'])]

for conf in conflicts:
	processConflictFile(conf, args.prefix)
