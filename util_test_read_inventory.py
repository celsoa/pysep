#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""


20210627 -- cralvizuri <celso.alvizuri@gmail.com>
"""
import glob
import obspy
from obspy.core.inventory import Inventory

ddir='20210224100557024/mass_downloader/stations'
ddir='testxml'
#stninv=None

inventory = Inventory(networks=[],source='ObsPy 1.0')
for xmlfile in glob.iglob(ddir + '/*.xml'):
    try:
        stninv = obspy.read_inventory(xmlfile)
        inventory.networks.append(stninv[0])
    except:
        print('ERROR. unable to append file', xmlfile)
    #    #continue        # TEST 1. 2021-05-17 17:31 USE CONTINUE. DOESNT WORK.
    #    #stninv = []     # TEST 2. 2021-05-18 TEST2. DOESNT WORK
    #    #stninv = []     # TEST 3 apply both? set null in case it's needed further down (where?). But continue ?? DOESNT WORK
    #    #continue   
    ##inventory.__add__(stninv)

#return inventory
