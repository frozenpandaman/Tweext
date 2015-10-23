# Tweext

A small utility for converting plain text files (short stories, books in the public domain, etc.) into Twee files, for use with [Twine](http://twinery.org/).

The basic Twee story format can be seen [here](http://twinery.org/wiki/writing_source_code_files).

I'll probably rename this project at some point (or at the very least, remove this line regarding the potential renaming.)

## Usage

Run the following from the command line:

    python convert.py your_filename.txt

This will output ``your_filename.tw`` which can then be imported, read, and compiled by Twine into a .html story. Currently, the last word of every paragraph is converted into a link leading to the next paragraph. The [twee utility](https://github.com/tweecode/twee) can do this from the command line, so I plan to integrate this in the future.