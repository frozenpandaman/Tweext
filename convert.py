import sys

def convert(file):
	infile = open(file,'r')
	filename = file.replace(".txt", '')

	title = "Call of the Wild" # test
	author = "Jack London"

	contents = infile.read()
	infile.close()
	contents = contents.split("\n\n") # split up paragraphs

	paras = [] # put whole paragraph on one line
	for para in contents:
		para = para.replace('\n', ' ')
		paras.append(para.strip())
	infile.close()

	outfile = open(filename + ".tw",'w')

	for i in range(len(paras)):
		outfile.write(":: " + str(heading(i)) + "\n") # append Twee paragraph headings
		formatLinks(paras, i, outfile) # make the last word of each paragraph a link
		outfile.write("\n\n")

	setTitle(title, outfile)
	setAuthor(author, outfile)

	outfile.close()

def heading(n):
	if n == 0:
		return "Start"
	else:
		return n

def formatLinks(paras, i, outfile):
	words = paras[i].split(' ')
	lastword = words[-1]
	for word in words:
		if word == lastword and i != len(paras)-1:
			# if it's the last word, make it a link to the next paragraph
			# (using tiddlywiki syntax), accounting for the period
			# stuff after the 'and' for dealing with last para
			outfile.write("[[" + word[:-1] + "|" + str(i+1) + "]].")
		else:
			outfile.write(word + " ")

def setTitle(title, outfile):
	outfile.write(":: StoryTitle\n")
	outfile.write(title + "\n\n")

def setAuthor(author, outfile):
	outfile.write(":: StoryAuthor\n")
	outfile.write(author + "\n\n")


convert(sys.argv[1])