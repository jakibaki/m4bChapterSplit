import os
import sys
from subprocess import Popen, PIPE, STDOUT


def q(str):
	return ('"' + str + '"')

def runCmd(cmd):
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	return str(p.stdout.read())


def splitFile(inputPath,outputPath):
	if not os.path.exists(inputPath):
		print("ERROR: The input-file does not exits!")
		exit(1)
	chapters = getChapters(inputPath)
	
	for i, chapter in enumerate(chapters):
		startSec = str(chapter[0]/1000)
		chapterLen = str((chapter[1]-chapter[0])/1000)
		chapterNum = str(i).zfill(3)
		chapterOutputPath = outputPath + "/" + inputPath.split("/")[-1][:-4] + " - " + chapterNum + ".aac"
		print("Writing " + chapterOutputPath + " ...")
		runCmd('ffmpeg -ss ' + startSec + ' -i ' + q(inputPath) + " -t " + chapterLen + " -acodec copy " + q(chapterOutputPath) )

def getChapters(file):
	a = runCmd("ffmpeg -i " + q(file) + " -f ffmetadata -")
	a = a.split("\\n")
	chapters = []
	for i, line in enumerate(a):
		if line.startswith("[CHAPTER]"):
			start = int(a[i+2][len("START="):])
			end = int(a[i+3][len("END="):])
			chapters.append([start,end])
	return chapters
		
if __name__ == '__main__':
	if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
		print("Usage: python3 split.py FILE.m4b output-path")
		exit(1)
	if len(sys.argv) < 3:
		outputPath = sys.argv[1][:-4]
	else:
		outputPath = sys.argv[2]
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)

	splitFile(sys.argv[1],outputPath)
