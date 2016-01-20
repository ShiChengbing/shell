#!/usr/bin/python


import os,sys
import string

import vaconf_db
import vaconf_p_cam

def parse_F50():
    try:
        if len(vaconf_db.F50_lines)==0: 
            return None
        #vaconf_db.dbgDumpLines('[F50]', vaconf_db.F50_lines);
        
    except BaseException, e:
         print 'Unknown error (',str(e),') happened in parse_F50'
    return None


