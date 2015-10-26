import re

contents = "CHAPTER 1 HELLO HELLO HELLO chapter I HELLO SECTION 1 LOL"

search = []
stringz = [
	"CHAPTER I","CHAPTER ONE","CHAPTER 1",
	"PART ONE","PART I","PART 1",
	"SECTION I","SECTION ONE","SECTION 1",
	"TABLE OF CONTENTS", "CONTENTS",
	"by " + author, title,
	"\n\n\n","\r\n\r\n\r\n",
	"\n\n","\r\n\r\n",
	"\n","\r\n"
	"blah"]
for i in range(len(stringz)):
	res = re.search(stringz[i], contents, re.IGNORECASE)
	if res != None:
		search.append(res.start())

print min(search)