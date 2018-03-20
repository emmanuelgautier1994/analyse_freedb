# analyse_freedb
I made this tool to analyse data about music albums from the freedb database, which is distributed under GNU/GPL license at http://www.freedb.org/en/. Credits to the team who makes the database : http://www.freedb.org/en/about_freedborg.2.html

In particular, I wanted to figure out whether my intuition, that Taylor Swift's 2017 album *__reputation__* had particularly uniform track lengths (spoiler: it does). I didn't intend to share the code at first, but then I shared my findings on Quora (https://www.quora.com/What-is-so-irritating-that-you-had-to-write-a-non-trivial-program-to-solve-it/answer/Emmanuel-Gautier) and some people asked for the code. Here it is, sparsely commented and unclean. It should run - in theory.

The people at freedb also wrote server software for hosting and querying the database, which I haven't tried.

This software is distributed under GNU/GPL v3.0. That means you can do many things with it as long as, if you redistribute it, you do so under the same license.

## Dependencies ##
* macOS or Linux [1]
* Python >=3.4
* numpy, pandas, matplotlib.pyplot, seaborn - all of which are available on pip :
```
pip install numpy pandas matplotlib seaborn
```

[1] : Sorry, Windows users, the software uses glob.iglob, an iterator, to read the massive freedb database file by file without sucking up all of your computer's memory. I haven't found a Windows equivalent yet and don't have a Windows machine I could test it on.

## Use ##
1. Install dependencies
2. Clone this repo wherever you like
2. Download freedb from http://ftp.freedb.org/pub/freedb/ (the latest version at the time of writing this is "freedb-complete-20180301.tar.bz2"
3. Unzip it to this repo's folder
4. Edit demo.py to set \_ROOT\_ to the repo's directory.
5. Run demo.py

This should run and display a nice visualization of the coefficient of variation of the genres in the database, along with Taylor Swift's data. You can then tinker with the viz however you like, using seaborn.

If you want to do more analysis, engine.py provides a number of functions for reading the database and parsing its files.

## Future ##
I don't plan to maintain this code, but I may pop in sometimes to fix issues. I'd also be happy to point to any fork that does interesting stuff on top of my code.
