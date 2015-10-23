# Tweext

A utility for converting plain text files (short stories, books, etc.) into Twee files, for use with [Twine](http://twinery.org/), a UI for creating hypertext stories.

The basic Twee story format can be seen [here](http://twinery.org/wiki/writing_source_code_files).

I'll probably rename this project at some point (or at the very least, remove this line regarding the potential renaming.)

## Usage

Run the following from the command line:

    python tweext.py your_filename.txt

This will output ``your_filename.tw`` which can then be imported, read, and compiled by Twine/Twee. Currently, the last word of every paragraph is converted into a link leading to the next paragraph. In the future, I hope to incorporate synctactic category identification (part-of-speech tagging) to create a better, smarter, more dynamic linking system.

The [twee utility](https://github.com/tweecode/twee) can compile from the command line (an easier, more automatic alternative to using the Twine application/GUI), so I plan to integrate this in the future as well.

## A note

Any texts uploaded to this repository are provided by [Project Gutenberg](http://www.gutenberg.org/) and are in the public domain.