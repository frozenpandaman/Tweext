import sys

def convert(file):
	infile = open(file,'r')
	filename = file.replace(".txt", '')

	contents = infile.read()
	infile.close()
	contents = contents.split("\n\n") # split up paragraphs

	paras = [] # put whole paragraph on one line
	for para in contents:
		para = para.replace('\n', ' ')
		paras.append(para.strip())
	infile.close()

	outfile = open(filename + ".tw",'w')

	for i in range(len(paras)): # append Twee paragraph headings
		outfile.write(":: " + str(heading(i)) + "\n")

		# format links at end of paragraph
		words = paras[i].split(' ')
		lastword = words[-1]
		for word in words:
			if word == lastword and i != len(paras)-1:
				# if it's the last word, use twine link syntax, accounting for the period
				# and case for dealing with last para
				outfile.write("[[" + word[:-1] + "|" + str(i+1) + "]].")
			else:
				outfile.write(word + " ")

		outfile.write("\n\n")

	outfile.close()

def heading(n):
	if n == 0:
		return "Start"
	else:
		return n

convert(sys.argv[1])