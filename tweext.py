import sys, re

def convert(file):
	''' Converts a plain text file into Twee format, to be used by Twine. '''
	filename = file.replace(".txt", '')

	infile = open(file,'r')

	contents = infile.read()
	infile.close()

	title = findTitle(contents)
	author = findAuthor(contents)

	contents = filterHeader(contents, title)
	contents = re.split("\n\n|\r\n\r\n", contents) # split up paragraphs. grr windows line breaks

	paras = [] # put whole paragraph on one line
	for para in contents:
		para = para.replace('\r\n', ' ').replace('\n', ' ') # both types of line breaks
		paras.append(para.strip())
	infile.close()

	outfile = open(filename + ".tw",'w')

	setTitle(title, outfile)
	setAuthor(author, outfile)

	for i in range(len(paras)):
	#if para[i] != "":
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

def filterHeader(contents,title):
	''' Separates the Gutenberg.org-style header and footer from the text body. '''
	# find starting point of actual book text
	line1 = "*** START OF THIS PROJECT GUTENBERG EBOOK " + title.upper().strip() + " ***"
	index1 = contents.find(line1)
	if index1 == -1:
		startpos = 0 # don't cut out any header
	else:
		startpos = index1 + len(line1) # + number of blank lines. or that's what we want at least


	# find first occurrence of title ("start" of book)
	# get this working(?):
	# start1 = re.search(title, contents, re.IGNORECASE)
	start1 = contents.lower().find(title.lower(), startpos)
	if start1 == -1:
		start1 = startpos # lol ur screwed

	# now, try to do better: look for author? or "by [author]", or if not, just "by "?
	# even better - "contents" or "table of contents"
	# orrr... {CHAPTER/PART} {1/ONE/I}(.)
	# we should actually check these first in reverse order, only dealing with the 'worse' cases (earlier on) if we have to.

	start2 = contents.find("\n\n\n", start1)
	if start2 == -1:
		start2 = contents.find("\r\n\r\n\r\n", start1) # try windows line breaks too
	# if still -1, just try for 2 or 1 line break...
	if start2 == -1:
		start2 = contents.find("\n\n", start1)
	if start2 == -1:
		start2 = contents.find("\r\n\r\n", start1)
	if start2 == -1:
		start2 = contents.find("\n", start1)
	if start2 == -1:
		start2 = contents.find("\r\n", start1)

	if start2 != -1:
		startpos = start2 # set startpos to our "real" starting point

	# now for the ending point

	#line2 = "*** END OF THIS PROJECT GUTENBERG EBOOK " + title.upper().strip() + " ***"
	line2 = "End of the Project Gutenberg EBook "
	endpos = contents.find(line2)

	if startpos == 0 and endpos == -1: # avoid returning contents[-1:-1] if no author/title found
		return contents
	elif endpos == -1:
		return contents[startpos:] # don't cut out any footer
	else:
		return contents[startpos:endpos] # normal, incl. case where startpos = 0 (index1 = -1)

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
	for word in words:
	#if word != "":
		# if it's the last word, make it a link to the next paragraph
		# (using tiddlywiki syntax), accounting for the period
		# stuff after the 'and' for dealing with last para
		if word == lastword and i != len(paras)-1:
			if word.strip() == "": # line break
				outfile.write("[[...|" + str(i+1) + "]]")
			else: # regular linking way
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