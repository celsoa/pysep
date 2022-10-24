#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""


20220923 -- cralvizuri <celso.alvizuri@gmail.com>
"""

import pickle
import sys

sys.stderr.write('reading inventory\n')
inventory = pickle.load(open('ims_full_inventory.p','rb'))
#print(inventory)

sys.stderr.write('processing inventory\n')
for net in inventory:
    for sta in net.stations:
        print(sta.code, sta.longitude, sta.latitude, sta.site.name)

