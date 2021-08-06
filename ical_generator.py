# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 17:50:38 2021

@author: chris

Generator for iCal data with uncommonly frequencies
"""

import datetime 
import io


class MYexeption(Exception):
    pass


########################## DATA FOR THE CALENDAR ###########################

NAME = "Events"

LOC = { #ID:location 
       1:"Event1",
       2:"Event2"
       }

SUM = {  #ID:summary
       1:"summary1",
       2:"summary2"
       }

DES = {  #ID_description
       1:"description 1",
       2:"other description"
       }

START_Y = {  #ID:startyear
            1:"2021",
            2:"2021"
            }

START_MD = {  # ID:start month + day
        1:["0930", "1204", "1021"],
        2:"1114"
        }

START_TIME = {  #ID:Hour + Minute + Second (at total 6 numbers)
            1:"150000",
            2:["110000"]
            }

END_Y = START_Y #like START_Y

END_MD = START_MD #like START_MD

END_TIME = {    #ID:Hour + Minute + Second (at total 6 numbers)
            1:"170000",
            2:"120000"
            } 

########################## END DATA FOR CALENDAR ###########################


FILE = NAME + ".ics"

DATE_FORMAT = "%Y%m%dT%H%M%S"
TODAY = datetime.datetime.now().strftime(DATE_FORMAT)

HEAD = "BEGIN:VCALENDAR\n" \
     + "VERSION:2.0\n" \
     + "PRODID:IDentity\n" \
     + "METHOD:PUBLISH\n"

TIMEZONE = "BEGIN:VTIMEZONE\n" \
         + "TZID:Europe/Berlin\n" \
         + "X-LIC-LOCATION:Europe/Berlin\n" \
         + "BEGIN:DAYLIGHT\n" \
         + "TZOFFSETFROM:+0100\n" \
         + "TZOFFSETTO:+0200\n" \
         + "TZNAME:CEST\n" \
         + "DTSTART:19700329T020000\n" \
         + "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=3\n" \
         + "END:DAYLIGHT\n" \
         + "BEGIN:STANDARD\n" \
         + "TZOFFSETFROM:+0200\n" \
         + "TZOFFSETTO:+0100\n" \
         + "TZNAME:CET\n" \
         + "DTSTART:19701025T030000\n" \
         + "RRULE:FREQ=YEARLY;BYDAY=-1SU;BYMONTH=10\n" \
         + "END:STANDARD\n" \
         + "END:VTIMEZONE\n"


def next_num():
    n = 0
    while True:
        n = n + 1
        yield str(n)
    

def append_event(loc, summ, des, start, end, EVENT, number):
    EVENT += "BEGIN:VEVENT\n" \
           + "UID:" + TODAY + next(number) + "@some.id\n" \
           + "LOCATION:" + loc + "\n" \
           + "SUMMARY:" + summ + "\n" \
           + "DESCRIPTION:" + des + "\n" \
           + "CLASS:PUBLIC\n" \
           + "DTSTART;TZID=Europe/Berlin:" + start + "\n" \
           + "DTEND;TZID=Europe/Berlin:" + end + "\n" \
           + "DTSTAMP:" + TODAY + "\n" \
           + "END:VEVENT\n"
    return EVENT


def check_MD(value): #checks if a given month day pair is valid
    month = int(value[0:2])
    day = int(value[2:4])
    if month in [1,3,5,7,8,10,12]:
        if day >= 32 or day <= 0:
            return False
        else:
            return True
    elif month in [4,6,9,11]:
        if day >= 31 or day <= 0:
            return False
        else:
            return True
    elif month == 2 :
        if day >= 30 or day <= 0:
            return False
        else:
            return True
    else:
        return False
    

def check_values():
    #check if there are problems with the deliverd data
    #check if every dic has the same amount of keys
    keys = LOC.keys()
    if keys != SUM.keys() or keys != DES.keys() or keys != START_Y.keys() \
        or keys != START_MD.keys() or keys != START_TIME.keys() \
        or keys != END_Y.keys() or keys != END_MD.keys() or keys != END_TIME.keys():
        
            raise MYexeption("Error in the given keys of the data, maybe " \
                             + "there are not equal or some dictionary has " \
                             + "more elements than the others")

    list_lens = {key:1 for key in keys}

    for key in keys:
        if isinstance(LOC[key], list) and list_lens[key] == 1:
            list_lens[key] = len(LOC[key])
        elif isinstance(LOC[key], list) and list_lens[key] != len(LOC[key]):
            raise MYexeption("Error in LOC, with key {}, wrong number of elements".format(key))
            
        if isinstance(SUM[key], list) and list_lens[key] == 1:
            list_lens[key] = len(SUM[key])
        elif isinstance(SUM[key], list) and list_lens[key] != len(SUM[key]):
            raise MYexeption("Error in SUM, with key {}, wrong number of elements".format(key))
            
        if isinstance(DES[key], list) and list_lens[key] == 1:
            list_lens[key] = len(DES[key])
        elif isinstance(DES[key], list) and list_lens[key] != len(DES[key]):
            raise MYexeption("Error in DES, with key {}, wrong number of elements".format(key))
            
        if isinstance(START_Y[key], list) and list_lens[key] == 1:
            list_lens[key] = len(START_Y[key])
        elif isinstance(START_Y[key], list) and list_lens[key] != len(START_Y[key]):
            raise MYexeption("Error in START_Y, with key {}, wrong number of elements".format(key))
        if isinstance(START_Y[key], list):
            for idx in range(len(START_Y[key])):
                if len(str(START_Y[key][idx])) != 4 : raise MYexeption("Not a year in START_Y")
                try: (int(START_Y[key][idx])/0) if int(START_Y[key][idx]) <= 0 else 1
                except: raise MYexeption('START_Y must be natural numbers')
        else: 
            if len(str(START_Y[key])) != 4 : raise MYexeption("Not a year in START_Y")
            try: (int(START_Y[key])/0) if int(START_Y[key]) <= 0 else 1
            except: raise MYexeption('START_Y must be natural numbers')
        
            
        if isinstance(START_MD[key], list) and list_lens[key] == 1:
            list_lens[key] = len(START_MD[key])
        elif isinstance(START_MD[key], list) and list_lens[key] != len(START_MD[key]):
            raise MYexeption("Error in START_MD, with key {}, wrong number of elements".format(key))
        if isinstance(START_MD[key], list):
            for idx in range(len(START_MD[key])):
                if len(str(START_MD[key][idx])) != 4 : raise MYexeption("elements must be of length 4 in START_MD")
                try: (int(START_MD[key][idx])/0) if int(START_MD[key][idx]) <= 0 else 1
                except: raise MYexeption('START_MD must be natural numbers')
                if not check_MD(str(START_MD[key][idx])): raise MYexeption('not a valid month day pair')
        else: 
            if len(str(START_MD[key])) != 4 : raise MYexeption("elements must be of length 4 in START_MD")
            try:(int(START_MD[key])/0) if int(START_MD[key]) <= 0 else 1
            except: raise MYexeption('START_MD must be natural numbers')
            if not check_MD(str(START_MD[key])): raise MYexeption('not a valid month day pair')
        
            
        if isinstance(START_TIME[key], list) and list_lens[key] == 1:
            list_lens[key] = len(START_TIME[key])
        elif isinstance(START_TIME[key], list) and list_lens[key] != len(START_TIME[key]):
            raise MYexeption("Error in START_TIME, with key {}, wrong number of elements".format(key))
        if isinstance(START_TIME[key], list):
            for idx in range(len(START_TIME[key])):
                if len(str(START_TIME[key][idx])) != 6 : raise MYexeption("elements must be of length 6 in START_TIME")
                try: (int(START_TIME[key][idx])/0) if int(START_TIME[key][idx]) <= 0 else 1
                except: raise MYexeption('START_TIME must be natural numbers')
        else: 
            if len(str(START_TIME[key])) != 6 : raise MYexeption("elements must be of length 6 in START_TIME")
            try: (int(START_TIME[key])/0) if int(START_TIME[key]) <= 0 else 1
            except: raise MYexeption('START_TIME must be natural numbers')
        
            
        if isinstance(END_Y[key], list) and list_lens[key] == 1:
            list_lens[key] = len(END_Y[key])
        elif isinstance(END_Y[key], list) and list_lens[key] != len(END_Y[key]):
            raise MYexeption("Error in END_Y, with key {}, wrong number of elements".format(key))
        if isinstance(END_Y[key], list):
            for idx in range(len(END_Y[key])):
                if len(str(END_Y[key][idx])) != 4 : raise MYexeption("Not a year in END_Y")
                try: (int(END_Y[key][idx])/0) if int(END_Y[key][idx]) <= 0 else 1
                except: raise MYexeption('END_Y must be natural numbers')
        else: 
            if len(str(END_Y[key])) != 4 : raise MYexeption("Not a year in END_Y")
            try: (int(END_Y[key])/0) if int(END_Y[key]) <= 0 else 1
            except: raise MYexeption('END_Y must be natural numbers')
        
            
        if isinstance(END_MD[key], list) and list_lens[key] == 1:
            list_lens[key] = len(END_MD[key])
        elif isinstance(END_MD[key], list) and list_lens[key] != len(END_MD[key]):
            raise MYexeption("Error in END_MD, with key {}, wrong number of elements".format(key))
        if isinstance(END_MD[key], list):
            for idx in range(len(END_MD[key])):
                if len(str(END_MD[key][idx])) != 4 : raise MYexeption("elements must be of length 4 in END_MD")
                try: (int(END_MD[key][idx])/0) if int(END_MD[key][idx]) <= 0 else 1
                except: raise MYexeption('END_MD must be natural numbers')
                if not check_MD(str(END_MD[key][idx])): raise MYexeption('not a valid month day pair')
        else: 
            if len(str(END_MD[key])) != 4 : raise MYexeption("elements must be of length 4 in END_MD")
            try: (int(END_MD[key])/0) if int(END_MD[key]) <= 0 else 1
            except: raise MYexeption('END_MD must be natural numbers')
            if not check_MD(str(END_MD[key])): raise MYexeption('not a valid month day pair')
        
            
        if isinstance(END_TIME[key], list) and list_lens[key] == 1:
            list_lens[key] = len(END_TIME[key])
        elif isinstance(END_TIME[key], list) and list_lens[key] != len(END_TIME[key]):
            raise MYexeption("Error in END_TIME, with key {}, wrong number of elements".format(key))
        if isinstance(END_TIME[key], list):
            for idx in range(len(END_TIME[key])):
                if len(str(END_TIME[key][idx])) != 6 : raise MYexeption("elements must be of length 6 in END_TIME")
                try: (int(END_TIME[key][idx])/0) if int(END_TIME[key][idx]) <= 0 else 1
                except: raise MYexeption('END_TIME must be natural numbers')
        else: 
            if len(str(END_TIME[key])) != 6 : raise MYexeption("elements must be of length 6 in END_TIME")
            try: (int(END_TIME[key])/0) if int(END_TIME[key]) <= 0 else 1
            except: raise MYexeption('END_TIME must be natural numbers')

    return list_lens


def main():
    Length = check_values() 
    print("Checked the values")
    
    EVENT = HEAD + TIMEZONE
    num = next_num()
    
    for key in Length.keys():
        for idx in range(Length[key]):
            
            location = LOC[key][idx] if isinstance(LOC[key], list) else str(LOC[key])
            summary = SUM[key][idx] if isinstance(SUM[key], list) else str(SUM[key])
            description = DES[key][idx] if isinstance(DES[key], list) else str(DES[key])
            
            s_y = START_Y[key][idx] if isinstance(START_Y[key], list) else str(START_Y[key])
            s_md = START_MD[key][idx] if isinstance(START_MD[key], list) else str(START_MD[key])
            s_t = START_TIME[key][idx] if isinstance(START_TIME[key], list) else str(START_TIME[key])
    
            e_y = END_Y[key][idx] if isinstance(END_Y[key], list) else str(END_Y[key])
            e_md = END_MD[key][idx] if isinstance(END_MD[key], list) else str(END_MD[key])
            e_t = END_TIME[key][idx] if isinstance(END_TIME[key], list) else str(END_TIME[key])
            
            start = s_y + s_md + "T" + s_t
            end = e_y + e_md + "T" + e_t
    
            EVENT = append_event(location, summary, description, start, end, EVENT, num)
            
        print("Wrote {} event(s) for key {}".format(idx + 1, key))
    
    EVENT += "END:VCALENDAR"
    
    with io.open(FILE, "w", encoding="utf-8") as f:
#        f.write(EVENT)
        pass
    print("Finished writing file {}".format(FILE))
    
    
    
if __name__ == "__main__":
    main()
    
    