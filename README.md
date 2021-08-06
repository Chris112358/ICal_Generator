# ICal_Generator
generator for ical events used for inconsistent repetative events

This is a Python script to write iCal files with some events.
To use this script set the variable NAME to the name of the file e.g. NAME = xy to name the file xy.ics.

Further the dictionarys (LOC, SUM, DES, START_Y, START_MD, START_TIME, END_Y, END_MD, END_TIME) accept either single strings or lists of strings for each key.
If you use lists make sure they are the same length for each key or of length 1. As for the _TIME dictionarys you have to use exactly 6 numbers representing hours, minuts and seconds. The _Y vaiables accept only years (for example '2021') and the _MD variables accept only months and days with exactly 4 numbers, e.g. use '0402' for the second day of april.
