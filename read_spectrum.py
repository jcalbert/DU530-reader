#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 17:39:16 2018

@author: jcalbert
"""

import serial
import pandas as pd

#Defaults
kwds = {'port'    : '/dev/ttyUSB0',
        'baudrate' : 19200,
        'parity'  : serial.PARITY_EVEN,
        'bytesize': 8,
        'stopbits': 1,
        'timeout' : 1.0} #seconds

def parse_scan_lambda(fname):
    
    # DU530 S/N: 0012U3002245 1.04
    # 07-OCT-18  16:10:05  SCAN
    # Group 1076  Sample 0001  
    # 350-1100 nm  Step 1.0 nm
    # scan info
    with open(fname, 'r') as f:
        l = ''
        while True:
            l = f.readline().strip()
            if l.startswith('Wavelength'):
                header = map(str.strip, l.split('  '))
                header.remove('')
                f.readline() # ignore crossbar
                break
        
        df = pd.read_table(f, sep='\s+', names=header, index_col=0,
                           usecols=[0,1])
        
    return df
    
if __name__ == '__main__':
    ser = serial.Serial(**kwds)
   
    # wait for connection
    ser.timeout = None    
    l = ser.readline().rstrip()
    ser.timeout = kwds['timeout']

    #discard blank lines
    while not l:
        l = ser.readline().rstrip()
    
    while True:
        l = ser.readline()
        if l.startswith('\x03') or l == '':
            break
        print l.rstrip()
