
"""
miscellaneous helper utilities

20160919 cralvizuri <cralvizuri@alaska.edu>
"""

from copy import deepcopy
from obspy.core import UTCDateTime
import glob
import obspy

def otime2eid(otime):
    """
    Convert origin time to origin ID. The origin ID has format: YYYYMMDDHHMMSSsss
    See also eid2otime.

    Example
        otime = "2009-04-07T20:12:55"
        eid = otime2eid(otime)
        print(otime, eid)
    """

    yy = UTCDateTime(otime).year
    mo = UTCDateTime(otime).month
    dd = UTCDateTime(otime).day
    hh = UTCDateTime(otime).hour
    mm = UTCDateTime(otime).minute
    ss = UTCDateTime(otime).second
    ms = int(UTCDateTime(otime).microsecond / 1000.0) # mili?
    eid = '%04d%02d%02d%02d%02d%02d%03d' % (yy, mo, dd, hh, mm, ss, ms)
    return eid

def eid2otime(eid):
    """
    Convert event ID to origin time. 
    See also otime2eid.

    Example
        eid = "20090407201255000"
        otime = eid2otime(eid)
        print(eid, otime)
    """

    part1 = "%s" % eid[:-3]
    part2 = "%s" % eid[-3:]
    eid = part1 + '.' + part2
    otime = UTCDateTime(eid)
    return(otime)


def copy_trace(stream, component=None):
    """ Copies given component from stream
    """
    if len(stream) == 0:
        raise Exception("Cannot extract trace from empty stream")

    if not component:
        return deepcopy(stream[0])
    else:
        trace = stream.select(component=component)[0]
        return deepcopy(trace)


def remove_trace(stream, component=None):
    """ Removes given component from stream
    """
    try:
        trace = stream.select(component=component)[0]
        stream.remove(trace)
    except:
        return stream


def get_streams_from_dir(ddir):
    '''
    Get streams from dir (created by mass downloader)
    mseed to stream
    '''
    from obspy.core import Trace, Stream

    st = Stream()
    tr = Trace()

    for mseed_trace in glob.iglob(ddir + '/*.mseed'):
        tr = obspy.read(mseed_trace)
        st.append(tr[0])

    return st

def get_inventory_from_xml(ddir):
    '''
    Return combined inventory multiple xml files 
    (created by mass downloader)

2021-05-17 NOTE the whole getwaveform suite crashes because some xml files might be missing data.
    Added try/except. But not sure if should add:
        continue OR stninv = [] 
---8<---8<---8<---
  File "/home/calvizur/UTILS/anaconda3/envs/seis38/lib/python3.8/site-packages/obspy/core/inventory/response.py", line 296, in normalization_frequency
    self._normalization_frequency = Frequency(value)
  File "/home/calvizur/UTILS/anaconda3/envs/seis38/lib/python3.8/site-packages/obspy/core/util/obspy_types.py", line 237, in __new__
    if not cls._minimum <= float(value) <= cls._maximum:
TypeError: float() argument must be a string or a number, not 'NoneType'
    '''

    from obspy.core.inventory import Inventory

    inventory = Inventory(networks=[],source='ObsPy 1.0.3')
    #inventory = Inventory()
    for xmlfile in glob.iglob(ddir + '/*.xml'):
        stninv = obspy.read_inventory(xmlfile)
        inventory.networks.append(stninv[0])
        #inventory.__add__(stninv)

    for xmlfile in glob.iglob(ddir + '/*.xml'):
        try:
            stninv = obspy.read_inventory(xmlfile)
        except:
            print(xmlfile)
            #stninv = []
            continue    # 2021-05-17 17:31 TEST1: USE CONTINUE
        inventory.networks.append(stninv[0])
        #inventory.__add__(stninv)


    return inventory
