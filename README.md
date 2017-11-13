# basic_level_spellcheck

This is a repository for python scripts that check for word spelling in basic\_level and word/object columns in basic level files. 

`spellcheck.py` accepts two arguments: *file* and *n*:
  - *file* is the absolute path to the basic\_level file the script will be checking
  - *n* is the number of words in the frequency-ordered list that the script will be using to do spell-checking
  - if only one argument recieved, the script would default n to be 10000

`spellcheck.py` would print out summary of spellchecking in the terminal and generate a log file in the same directory as the *file*. 
