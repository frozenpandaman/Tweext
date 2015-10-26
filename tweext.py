import sys, re

def convert(file):
	''' Converts a plain text file into Twee format, to be used by Twine. '''
	filename = file.replace(".txt", '')

	infile = open(file,'r')

	contents = infile.read()
	infile.close()

	title = findTitle(contents)
	author = findAuthor(contents)

	contents = filterHeader(contents, title, author)
	contents = re.split("\n\n|\r\n\r\n", contents) # split up paragraphs. grr windows line breaks

	paras = [] # put whole paragraph on one line
	for para in contents:
		para = para.replace('\r\n', ' ').replace('\n', ' ') # both types of line breaks
		paras.append(para.strip())
	infile.close()

	outfile = open(filename + ".tw",'w')

	setTitle(title, outfile)
	setAuthor(author, outfile)

 	# don't parse line breaks, and don't let our paras count go up for these
	paras[:] = (para for para in paras if para.strip() != "")

	for i in range(len(paras)):
		if paras[i].strip() != "":
			outfile.write(":: " + str(heading(i)) + "\n") # append Twee paragraph headings
			formatLinks(paras, i, outfile) # make the last word of each paragraph a link
			outfile.write("\n\n")

	outfile.close()


def findTitle(contents):
	''' Finds the title of a book (Gutenberg.org format) '''
	result = re.search("\nTitle: (.*)\n", contents)
	try:
		result = result.group(1)
		return result
	except:
		return "Unknown"

def findAuthor(contents):
	''' Finds the author of a book (Gutenberg.org format) '''
	result = re.search("\nAuthor: (.*)\n", contents)
	try:
		result = result.group(1)
		return result
	except:
		return "Unknown"

def filterHeader(contents, title, author):
	''' Separates the Gutenberg.org-style header and footer from the text body. '''

	# find the ending point first (to not have to search legal jargon @ bottom)
	endpossib = []
	endpossib.append(contents.find("End of the Project Gutenberg EBook "))
	endpossib.append(contents.find("*** END OF THIS PROJECT GUTENBERG EBOOK "))
	endpossib.append(contents.find("End of Project Gutenberg's "))
	for n in endpossib:
		if n == -1:
			endpossib.remove(-1)
	if len(endpossib) != 0:
		endpos = min(endpossib)
	else:
		endpos = -1


	# now find the starting point of the actual book text
	line1 = "*** START OF THIS PROJECT GUTENBERG EBOOK " + title.upper().strip() + " ***"
	index1 = contents.find(line1)
	if index1 == -1:
		startpos = 0 # don't cut out any header
	else:
		startpos = index1 + len(line1) # + number of blank lines. or that's what we want at least

	startpos += refineHeader(contents, title, author, startpos, endpos)


	if startpos == 0 and endpos == -1: # avoid returning contents[-1:-1] if no author/title found
		return contents
	elif endpos == -1:
		return contents[startpos:] # don't cut out any footer
	else:
		return contents[startpos:endpos] # normal, incl. case where startpos = 0 (index1 = -1)

def refineHeader(contents, title, author, startpos, endpos):
	search = [0]
	stringz = [
		"CHAPTER I","CHAPTER ONE","CHAPTER 1",
		"PART ONE","PART I","PART 1",
		"SECTION I","SECTION ONE","SECTION 1",
		"TABLE OF CONTENTS", "CONTENTS",
		"by " + author, title,
		"\n\n\n","\r\n\r\n\r\n",
		"\n\n","\r\n\r\n",
		"\n","\r\n" ]
	for i in range(len(stringz)):
		res = re.search(stringz[i], contents[startpos:endpos], re.IGNORECASE)
		if res != None:
			search.append(res.start())
	return max(search)

def heading(n):
	''' Returns the passage heading name (number). '''
	if n == 0:
		return "Start"
	else:
		return n

def formatLinks(paras, i, outfile):
	''' Converts the last word of each paragraph into a link to the next paragraph. '''
	words = paras[i].split(' ')
	lastword = words[-1]
	try:
		lastchar = lastword[-1]
		try:
			if lastword[-2:] == ".\"":
				lastchar = ".\""
		except:
			pass
	except:
		lastchar = ""
	lc = len(lastchar)

	# if i == len(paras) or i == len(paras)-1:
	# 	print words[-1]
	# for getting verylastword

	for word in words:
	#if word != "":
		# if it's the last word, make it a link to the next paragraph
		# (using tiddlywiki syntax), accounting for the period
		# stuff after the 'and' for dealing with last para
		if word.strip() == lastword.strip() and i != len(paras)-1 and word.strip() != "":
			if lastchar.isalpha() or lastchar == "*": # SO hacky. there has to be a better fix...
				outfile.write("[[" + word[:-lc] + lastchar + "|" + str(i+1) + "]]")
			else:
				outfile.write("[[" + word[:-lc] + "|" + str(i+1) + "]]" + lastchar)
		else: # regular word, not at end - no link
			outfile.write(word + " ")

def setTitle(title, outfile):
	''' Sets the title of the book (in the sidebar, or wherever StoryTitle is displayed). '''
	outfile.write(":: StoryTitle\n")
	outfile.write(title + "\n\n")

def setAuthor(author, outfile):
	''' Sets the title of the book (in the sidebar, or wherever StoryAuthor is displayed). '''
	outfile.write(":: StoryAuthor\n")
	outfile.write(author + "\n\n")


convert(sys.argv[1])