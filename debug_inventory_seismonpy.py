#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
Code to get IMS waveforms and correct for instrument response.
Use with seismonpy-IMS client 

CURRENTLY DOESN'T WORK.

refs
https://docs.obspy.org/master/packages/autogen/obspy.core.stream.Stream.remove_response.html?highlight=remove_response#obspy.core.stream.Stream.remove_response


20220708 -- cralvizuri <celso.alvizuri@gmail.com>
"""

from obspy import UTCDateTime
from seismonpy.utils.ims_request import IMS_Client as Client

#-----------------------------------------------------------\
path_to_nms_client = '/nobackup/celso/REPOSITORIES/IMS-nms_client3/nms_client3'
station = "USRK"
channel = "BHZ"
t1 = UTCDateTime('2022-07-07T00:00:00')
t2 = UTCDateTime('2022-07-07T01:00:00')
#-----------------------------------------------------------\

client = Client(nms_path=path_to_nms_client)
inventory=client.get_stations(station=station, channel=channel)
st = client.get_waveforms(station=station, channel=channel, starttime=t1, endtime=t2)
print(inventory)
type(inventory)

inv0 = inventory[0]
print(inv0)
#	Network IM (IMS network)
#	        Station Count: None/None (Selected/Total)
#	        -- - --
#	        Access: UNKNOWN
#	        Contains:
#	                Stations (2):
#	                        IM.USA0B (USSURIYSK ARRAY ELEMENT USA0B)
#	                        IM.USRK (USSURIYSK ARRAY, Russian Federation.)
#	                Channels (2):
#	                        IM.USA0B..BHZ (2x)
#	

resp = inv0.get_response('IM.USA0B..BHZ', t1)
print(resp)
#	Channel Response
#	        From M/S (Velocity in Meters per Second) to COUNTS (Digital Counts)
#	        Overall Sensitivity: 1.98944e+10 defined at 1.000 Hz
#	        8 stages:
#	                Stage 1: PolesZerosResponseStage from M/S to V, gain: 20000
#	                Stage 2: PolesZerosResponseStage from V to V, gain: 1
#	                Stage 3: PolesZerosResponseStage from V to V, gain: 1
#	                Stage 4: CoefficientsTypeResponseStage from V to COUNTS, gain: 1e+06
#	                Stage 5: FIRResponseStage from COUNTS to COUNTS, gain: 1
#	                Stage 6: FIRResponseStage from COUNTS to COUNTS, gain: 1
#	                Stage 7: FIRResponseStage from COUNTS to COUNTS, gain: 1
#	                Stage 8: FIRResponseStage from COUNTS to COUNTS, gain: 1


#-----------------------------------------------------------
# CORRECTING FOR RESPONSE WITH OBSPY WORKS DIRECTLY WITH THIS COMMAND
# (ultimately this is the command needed)
# tr.remove_response(inventory=stations, water_level=water_level, pre_filt=pre_filt, output=outformat)
#
# WITH SEISMONPY IT DOESN'T WORK
# See the following examples
# TODO Check with Andreas K / Hakon
# 2022-07-08
#-----------------------------------------------------------

## CORRECT RESPONSE FROM STREAM 
#print('TRY STREAM 1')  # doesnt work with seismonpy
## ValueError: No matching response information found.
#st.remove_response(inventory)

#print('TRY STREAM 2')  # doesnt work with seismonpy
## ValueError: No matching response information found.
#st.remove_response(inventory, t1)

print('TRY STREAM 3')  # doesnt work with seismonpy
#st.remove_response(inventory[0].get_response('USRK.USA0B..BHZ', t1))    # Exception: No matching response information found.
st.remove_response(inventory[0].get_response('IM.USA0B..BHZ', t1))      # TypeError: 'Response' object is not iterable

## CORRECT RESPONSE FROM TRACE
tr = st[0]  # Out[179]: USRK.USA0B..BHZ | 2022-07-07T00:00:00.000000Z - 2022-07-07T00:59:59.975000Z | 40.0 Hz, 144000 samples
print('TRY TRACE 1')  # doesnt work with seismonpy
# TypeError: 'Response' object is not iterable
tr.remove_response(inventory=inv0.get_response('IM.USA0B..BHZ', t1), output='VEL', water_level=60, pre_filt=None, zero_mean=True, taper=True, taper_fraction=0.05, plot=False, fig=None)

print('TRY TRACE 2')  # doesnt work with seismonpy
# Exception: No matching response information found.
tr.remove_response(inventory=inv0.get_response('USRK.USA0B..BHZ', t1), output='VEL', water_level=60, pre_filt=None, zero_mean=True, taper=True, taper_fraction=0.05, plot=False, fig=None)

