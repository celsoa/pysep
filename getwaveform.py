#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tools for interfacing IRIS data, ObsPy, and SAC input/output.
"""
from __future__ import print_function

import os, sys
from copy import deepcopy

import obspy
from obspy.clients.fdsn import Client
from obspy.clients import fdsn
from obspy.core.event import Event, Origin, Magnitude, Catalog

from scipy import signal
import pickle

from util_write_cap import *
from util_helpers import get_streams_from_dir, get_inventory_from_xml
from obspy.taup import TauPyModel
from obspy.geodetics import kilometer2degrees
import math

from obspy.clients.fdsn.mass_downloader import CircularDomain, \
    RectangularDomain, Restrictions, MassDownloader

def checkpoint():
    """TODO: Docstring for checkpoint.

    :arg1: TODO
    :returns: TODO

    """
    yesno = input('continue? (y/n)\n')
    if 'y' in yesno.lower(): 
        pass
    else: 
        print('stopped.'); sys.exit()
    pass

class getwaveform:
    def __init__(self):
        """
        ---------------- copied from old getwaveform.py ----------------------
        min_dist - minimum station distance (default = 20)
        max_dist - maximum station distance (default =300)
        before -   time window length before the event time (default= 100)
        after  -   time window length after the event time (default = 300)
        network -  network codes of potential stations (default=*)
        channel -  component(s) to get, accepts comma separated (default='BH*')
        ifresample_TF   - Boolean. Request resample or not. Default = False
        resample_freq   - sampling frequency to resample waveforms (default 20.0)
        ifrotate - Boolean, if true will output sac files rotated to baz
        unrotated sac files will also be written
        ifCapInp - Boolean, make weight files for CAP
        ifEvInfo - Boolean, output 'ev_info.dat' containg event info (True)
        ifRemoveResponse - Boolean, will remove response (True)
        ifDetrend - Boolean, will remove linear trend from data (True)
        ifDemean  - Boolean, will insult the data (True)
        scale_factor - scale all data by one value (10.0**2)
        This usually puts the data in the units required by CAP
        From m/s to cm/s
        pre_filt  - list, corner frequencies of filter to apply before deconv
        a good idea when deconvolving (ifRemoveResponse=True)
        """
        # DEFAULT SETTINGS
        self.ifph5 = False   # PH5 data format from PASSCAL (Denali nodal data)
        self.client_name = 'IRIS'  # IRIS, LLNL, NCEDC
        # idb = database index: OBSOLETE -- use client_name instead
        self.idb = None  # =1-IRIS (default); =2-AEC; =3-LLNL; =4-Geoscope

        # event parameters
        self.use_catalog = 1 # =1: use an existing catalog (=1); =0: specify your own event parameters (see iex=9)
        self.sec_before_after_event = 10 # time window to search for a target event in a catalog
        self.tbefore_sec = 100
        self.tafter_sec = 300
        # These are used only if self.use_catalog = 0
        self.evname = None
        self.otime = None
        self.elat = None
        self.elon = None
        self.edep = None
        self.emag = None
        # Refernce origin (dummy values)
        self.rlat = None
        self.rlon = None
        self.rtime = None
        # event objects
        self.ev = Event()
        self.ref_time_place = Event()

        # station parameters
        self.network = '*'                   # all networks
        self.station = '*'                   # all stations
        self.exclude_net = ''                # except these networks 
        #self.station = '*,-PURD,-NV33,-GPO'  # all stations except -(these)
        self.channel = '*'                   # all channels    
        self.location = '*'                  # all locations
        self.min_dist = 0 
        self.max_dist = 20000
        self.min_az = 0 
        self.max_az = 360
        self.min_lat = None
        self.max_lat = None
        self.min_lon = None
        self.max_lon = None
        self.overwrite_ddir = 1              # 1 = delete data directory if it already exists
        self.icreateNull = 0                 # create Null traces so that rotation can work (obspy stream.rotate require 3 traces)
                                             # this might be helpful if missing a vertical component only
        self.phase_window = False            # Grab waveforms using phases #WARNING this will cut the waveform to be near the phase arrival
        self.phases = ["P","P"]              # Phases to write to sac files or grab data from
        self.write_sac_phase = False         # put phase information in sac files
        self.taupmodel= "ak135"
        # Filter parameters
        self.ifFilter = False 
        #------Filter--------------
        # for 'bandpass' both f1 and f2 are used
        # for 'lowpass' only f2 is used
        # for 'highpass' only f1 is used
        #
        # EXAMPLES
        #                                   ifFilter  zerophase  remove_response  ipre_filt
        # A. CAP-ready waveforms [DEFAULT]: False     NA         True             1
        # B. plot-ready waveforms, acausal: True      True       True             2
        # C. plot-ready, causal waveforms:  True      False      True             0
        # D. possible sensor issues:        True      False      False            NA
        #
        self.filter_type = 'bandpass'
        # f1 should consider the requested length of the time series
        # f2 should consider the sampling rate for the desired channels
        self.f1 = 1/40 # fmin - highpass will keep frequencies larger than fmin
        self.f2 = 1/10 # fmax - lowpass will keep frequencies lower than fmax
        self.zerophase = True             # = False (causal/one-pass), = True (acausal/two-pass)
        # 4 pole filter is more sharper at the edges than 2 pole
        self.corners = 4                  # Is corner in Obspy same as Pole in SAC?
        
        # Pre-filter parameters
        self.ipre_filt = 1                # =0 No pre_filter
                                          # =1 default pre_filter (see getwaveform_iris.py)
                                          # =2 user-defined pre_filter (use this if you are using bandpass filter)
        # For tapering down the pre-filter
        # Perhaps you want to set ipre_filt = 0 to prevent extra filtering
        # pre-filter for deconvolution
        # https://ds.iris.edu/files/sac-manual/commands/transfer.html
        # Pre-filter will not be applied if remove_response = False 
        self.f0 = 0.5*self.f1
        self.f3 = 2.0*self.f2
        self.pre_filt=(self.f0, self.f1, self.f2, self.f3)    # applies for ipre_filt = 2 only
        # self.pre_filt = (0.005, 0.006, 10.0, 15.0) # BH default
        self.water_level = 60

        # For CAP
        self.resample_TF = False          # if False then resample_freq is taken from SAC files
        self.resample_freq = 50           # 0 causes errors. Use resample_TF instead
        self.scale_factor = 1             # for CAP use 10**2  (to convert m/s to cm/s)

        # Pre-processing (mainly for CAP)
        self.output_cap_weight_file = True# output cap weight files
        self.detrend = True               # detrend waveforms
        self.demean = True                # demean waveforms
        self.taper = False                # this could also be a fraction between 0 and 1 (fraction to be tapered from both sides)
        self.output_event_info = True     # output event info file
        self.outformat = 'VEL'            # Instrument-response-removed waveforms saved as VEL, DISP, or ACC
        self.ifsave_sacpaz = False        # save sac pole zero (needed as input for MouseTrap module)
        self.remove_response = True       # remove instrument response 
        self.iplot_response = False       # plot response function
        self.ifplot_spectrogram = False   # plot spectrograms 
        self.ifsave_stationxml = True     # save station xml file (for adjoint tomo)

        # options for rotation and for writing sac files
        self.rotateRTZ = True             # Rotate and save the RTZ components
        self.rotateUVW = False            # Rotate and save the UVW components
        self.isave_raw = False            # save raw waveforms
        self.isave_raw_processed = True   # save processed waveforms just before rotation to ENZ
        self.rotateENZ = True             # rotate extracted waveforms to ENZ
        self.isave_ENZ = True             # save ENZ

        # username and password for embargoed IRIS data
        # Register here: http://ds.iris.edu/ds/nodes/dmc/forms/restricted-data-registration/
        self.user = None
        self.password = None

        # To output lots of processing info
        self.ifverbose = True

        # save RTZ as asdf files
        self.ifsave_asdf = False

        # Use mass downloader instead
        self.ifmass_downloader = False

    def run_get_waveform(self):
        """
        Get SAC waveforms for an event
        
        basic usage:
        run_get_waveform(event)
        
        c              -  client
        event          -  obspy Event object
        ref_time_place -  reference time and place (other than origin time and place - for station subsetting)
        """
        
        #c = self.client
        event = self.ev
        ref_time_place = self.ref_time_place

        evtime = event.origins[0].time
        reftime = ref_time_place.origins[0].time

        #-----------------------------------------------------------
        # BEGIN OPTIONS MASS DOWNLOADER
        #-----------------------------------------------------------
        #if self.ifmass_downloader is True:
        if self.idb is not None and self.ifmass_downloader is True:
            domain = CircularDomain(
                    latitude =self.elat, 
                    longitude=self.elon,
                    minradius=kilometer2degrees(self.min_dist), 
                    maxradius=kilometer2degrees(self.max_dist))
            print('DEBUG. domain radius (deg) min/max %f/%f (input %f km)' %
                    (domain.minradius, domain.maxradius, self.max_dist))
            print('DEBUG. lon/lat %f/%f' %
                    (domain.longitude, domain.latitude))
            
            restrictions = Restrictions(
                starttime = reftime - self.tbefore_sec,
                endtime = reftime + self.tafter_sec,
                #station_starttime = None,
                #station_endtime = None,
                station_starttime = reftime - self.tbefore_sec,  # 2021-06-25 TEST. only query stations available during the event times.
                station_endtime = reftime + self.tafter_sec,
                chunklength_in_sec = None,
                network = self.network,
                station = self.station,
                location = self.location,
                channel = self.channel,
                exclude_networks = self.exclude_net,
                #exclude_stations = (),
                #limit_stations_to_inventory=None,
                reject_channels_with_gaps=False,
                minimum_length = 0.0,
                sanitize = True,
                minimum_interstation_distance_in_m = 100,   # 2021-07-13 avoid using same station with different names
                #channel_priorities=(),
                #location_priorities=())
		)

            mdl = MassDownloader()
            
            outdir = './' + self.evname
            mdl.download(domain=domain, restrictions=restrictions, 
                         mseed_storage=outdir+"/mass_downloader/waveforms", 
                         stationxml_storage=outdir+"/mass_downloader/stations", 
                         download_chunk_size_in_mb=20, threads_per_client=3, print_report=True)

            inventory = get_inventory_from_xml(outdir+"/mass_downloader/stations")
            stream_raw = get_streams_from_dir(outdir+"/mass_downloader/waveforms")

            print(inventory)
            phases = self.phases
          
            t1s, t2s= get_phase_arrival_times(inventory,event,self.phases,
                                              self.phase_window,self.taupmodel,
                                              reftime,self.tbefore_sec,self.tafter_sec)
        # End mass downloader
        #-----------------------------------------------------------

        #-----------------------------------------------------------
        # Pick client
        #-----------------------------------------------------------
        # Add deprecation warning
        if self.idb is not None:
            print('WARNING: Instead of idb use which client you want to use \n'\
                  '         By default ev_info.client_name is set to IRIS')
            if self.idb == 3:
                self.client_name = "LLNL"
            
        # 2022-07-18 TEST USE INSTEAD: if self.client_name != "LLNL" and self.ifmass_downloader is False:
        #if self.client_name != "LLNL" and self.client_name != "NORSAR" and self.ifmass_downloader is False:
        #if self.client_name != "LLNL" and self.client_name != "IMS-SMP" and self.ifmass_downloader is False and self.client_name != "local":
        if self.client_name != "LLNL" and self.client_name != "IMS-SMP" and self.ifmass_downloader is False and self.client_name != "local" and self.client_name != 'NIEP':
            # Send request to client
            # There might be other way to do this using 'RoutingClient'
            print("Sending request to client: %s" % self.client_name)
            c = self.client
            print(c)
            
            # Check if stations chosen are correct
            # Example: NCEDC does not understand '-XXX' station code
            if self.client_name == "NCEDC":
                if '-' in self.station:
                    raise ValueError("NCEDC client does not take '-' in station code")

            if self.client_name == "IRIS":
                if '*' in self.network:
                    print("WARNING: You have chosen to search ALL networks at IRIS." \
                          "This could take long!")
            #-----------------------------
            if self.ifph5:
                STATION = 'http://service.iris.edu/ph5ws/station/1'
                c = fdsn.client.Client('http://service.iris.edu',
                                       service_mappings={
                                       'station': STATION
                                       },
                                       debug=True
                                   )

            #-----------------------------------------------------------
            # Download stations
            #-----------------------------------------------------------
            print("Download stations...")
            stations = c.get_stations(network=self.network, location=self.location,
                                      station=self.station, channel=self.channel,
                                      starttime=reftime - self.tbefore_sec, 
                                      endtime=reftime + self.tafter_sec,
                                      minlatitude=self.min_lat,
                                      maxlatitude=self.max_lat,
                                      minlongitude=self.min_lon,
                                      maxlongitude=self.max_lon,
                                      level="response")
            inventory = stations    # so that llnl and iris scripts can be combined

            if self.ifverbose:
                print("Printing stations")
                print(stations)
                print("Done Printing stations...")

            sta_limit_distance(ref_time_place, 
                               stations, 
                               min_dist=self.min_dist, 
                               max_dist=self.max_dist, 
                               min_az=self.min_az, 
                               max_az=self.max_az,
                               ifverbose=self.ifverbose)
            #print("Printing stations NEW")
            #print(stations)
            #print("Done Printing stations...")
            
            #stations.plotprojection="local")
            # Find P and S arrival times
            phases = self.phases
          
            t1s, t2s= get_phase_arrival_times(stations,event,self.phases,
                                              self.phase_window,self.taupmodel,
                                              reftime,self.tbefore_sec,self.tafter_sec)
 
            print("Downloading waveforms...")
            # this needs to change
            bulk_list = make_bulk_list_from_stalist(stations,t1s,t2s, 
                                                    channel=self.channel)

            if self.ifph5:
                DATASELECT = 'http://service.iris.edu/ph5ws/dataselect/1'
                c = fdsn.client.Client('http://service.iris.edu',
                                       service_mappings={
                                           'dataselect': DATASELECT
                                       },
                                       user = self.user,password = self.password,
                                       debug=True
                                   )
                stream_raw = c.get_waveforms(network=self.network, location=self.location,
                                             station=self.station, channel=self.channel,
                                             starttime=reftime - self.tbefore_sec, 
                                             endtime=reftime + self.tafter_sec)
            else:
                stream_raw = c.get_waveforms_bulk(bulk_list)
            
            # save ev_info object
            pickle.dump(self,open(self.evname + '/' + 
                                  self.evname + '_ev_info.obj', 'wb'))    
            

        #-----------------------------------------------------------
        # 2023-06-14 TEST GET DATA FROM ORFEUS NETWORK

        elif self.idb is None and self.client_name == 'NIEP':
            #===================================
            # SNIPPET FROM JOHANNES
            starttime = reftime - self.tbefore_sec
            endtime   = reftime + self.tafter_sec
            client = Client('NIEP', force_redirect=True)
            token = '/staff/johannes/eidatoken'
            client.set_eida_token(token)
            print("\n** WARNING ** Preparing request for client\n", client)
            print("Downloading stations...")
            stations = client.get_stations(network   = 'Y8,MD,UD', 
                                      station   = '*',
                                      location  = '*',
                                      channel   = self.channel,
                                      starttime = starttime,
                                      endtime   = endtime,
                                      level     = 'response')
            #===================================
            #-----------------------------------------------------------
            inventory = stations    
            sta_limit_distance(ref_time_place, 
                               stations, 
                               min_dist=self.min_dist, 
                               max_dist=self.max_dist, 
                               min_az=self.min_az, 
                               max_az=self.max_az,
                               ifverbose=self.ifverbose)
            #-----------------------------------------------------------
            print("Downloading waveforms...")
            stream_raw = client.get_waveforms(
                                              network         = 'Y8,MD,UD',
                                              #station         = inventory,
                                              station         = '*',
                                              location        = '*',
                                              channel         = self.channel,   # FUTURE: ok to exclude this.
                                              starttime       = starttime, 
                                              endtime         = endtime,
                                              attach_response = True,
                                              )
         
        elif self.client_name=="LLNL" and self.ifmass_downloader is False:
            #client_name = "LLNL"
            print("Preparing request for LLNL ...")
            
            # Get event an inventory from the LLNL DB.
            event_number = int(event.event_descriptions[0].text)
            # event = llnl_db_client.get_obspy_event(event)
            inventory = c.get_inventory()
 
            nsta_llnl = len(inventory.get_contents()["stations"])
            print("--> Total stations in LLNL DB: %i" % nsta_llnl)
            sta_limit_distance(event, inventory, 
                    min_dist=self.min_dist, 
                    max_dist=self.max_dist, 
                    min_az=self.min_az, 
                    max_az=self.max_az)
            print("--> Stations after filtering for distance: %i" % (
                    len(inventory.get_contents()["stations"])))
            
            stations = set([sta.code for net in inventory for sta in net])
            
            _st = c.get_waveforms_for_event(event_number)
            stream_raw = obspy.Stream()
            for tr in _st:
                if tr.stats.station in stations:
                    stream_raw.append(tr)

        #-----------------------------------------------------------
        # 20220718 TODO: ADD OPTION FOR CLIENT NORSAR-SEISMONPY
        #-----------------------------------------------------------
            ## 20220224 calvizuri --  TEST 
            #from seismonpy.norsardb import Client as NORclient
            # 2022-07-12 TRY2
            #
            ## THE FOLLOWING SNIPPETS WERE MOVED FROM THE SMP-IMS CLIENT WHICH
            ## EVOLVED FROM OLD SNIPPETS FOR THE NORSAR CLIENT
            #
            # 2022-03-02 may not need the following - 
            #inventory = IMSclient.get_array_inventory("ARCES", time=starttime)
            #inventory = IMSclient.get_array_inventory("NOA", time=starttime)
            #print("DEBUG. done. inventory: ", inventory)
            #stream_raw = IMSclient.get_waveforms("NAO01", "BHZ", UTCDateTime(2017, 10, 29, 1, 0, 0), UTCDateTime(2017, 10, 29, 1, 0, 0)+3600)
            # 
            # OPTIOM 3 -faster? read_inventor(path2/db/inventory_seed..etc)
            #
            #stream_raw = IMSclient.get_waveforms("AR{A,B,C}*", "BHZ", starttime, endtime, attach_response=True) 
            #print("DDDDDDDDDDDDDDDDDD", starttime, endtime) = 2017-09-03T03:28:21.760000Z 2017-09-03T04:03:21.760000Z
            # USA0B
            #stream_raw = IMSclient.get_array_waveforms("ARCES", "BHZ", starttime, endtime)  # TEST 2022-03-02. issue with ARCES: ValueError: did not find matching array 
            #stream_raw = IMSclient.get_array_waveforms("NOA", "*Z", starttime, endtime)     # TEST 2022-03-02. same issue as above but with NOA array
            #print("IMS-SMP client: done. Waveforms: ", stream_raw.__str__(extended=True))
        #===========================================================

        #-----------------------------------------------------------
        # 2022-07-18 INTERFACE NORSAR-SEISMONPY AND IMS-NMS CLIENT
        #-----------------------------------------------------------
        elif self.client_name == "IMS-SMP" and self.ifmass_downloader is False:
            from seismonpy.utils.ims_request import IMS_Client

            path_to_nms_client = '/nobackup/celso/REPOSITORIES/IMS-nms_client3/nms_client3'
            IMSclient = IMS_Client(nms_path=path_to_nms_client)

            print("\nPreparing request for IMS data ...")
            starttime = reftime - self.tbefore_sec
            endtime   = reftime + self.tafter_sec
            print("IMS-SMP client: requesting station data for network/station/channel(s): %s/%s/%s ..." % (self.network, self.station, self.channel))
            inventory = IMSclient.get_stations(network = self.network, 
                                         station    = self.station, 
                                         channel    = self.channel,
                                         starttime  = starttime, 
                                         endtime    = endtime,
                                         longitude  = self.elon,
                                         latitude   = self.elat,
                                         minradius  = kilometer2degrees(self.min_dist),
                                         maxradius  = kilometer2degrees(self.max_dist),
                                         use_cache  = True,    # 2022-07-19 NOTE! unable to get station info if using local cache! either sta data changed in the last few days or there is a bug in cached file!
                                         #use_cache  = False,   # 2022-08-05 NOTE: use. else error: Error requesting waveforms for station AKASG
                                         #cache_file = '/nobackup/celso/REPOSITORIES/pysep-dev-IMS/ims_full_inventory.p'
                                         )
            print("IMS-SMP client: done. Stations: ", inventory)
            #
            print("IMS-SMP client: fetching waveform data ...")
            ## OPTION 1. request IMS data one station at a time
            ## REFERENCE FOR get_waveforms: /vcs/celso/seismon_py/seismonpy/utils/ims_request.py
            #stream_raw = IMSclient.get_waveforms(station = self.station, 
            #                        channel              = self.channel, 
            #                        starttime            = starttime, 
            #                        endtime              = endtime,
            #                        #attach_response      = True,
            #                        #set_ims_network_code = True
            #                        )
            #
            #-----------------------------------------------------------
            # OPTION 2: (DEFAULT) use inventory to request data recursively one station at a time.
            # Works with list of stations preselected by region+radius
            # 2022-09-12 WORKS. Tested on Kiruna event.
            #stream_raw = obspy.Stream()
            #for net in inventory:
            #    print('Number of stations found: ', len(inventory[0]))
            #    for sta in net:
            #        print("IMS-SMP client: fetching waveform data for %s ..." % sta.code)
            #        stream_raw += IMSclient.get_waveforms(station = sta.code, 
            #                                channel               = self.channel,
            #                                starttime             = starttime, 
            #                                endtime               = endtime,
            #                                #attach_response      = True,
            #                                #set_ims_network_code = True
            #                                )
            ##-----------------------------------------------------------
            # OPTION 3. Feed inventory directly into get_waveforms
            # 2022-09-13. Works- need to specify channel. But latest revision (AK) seems to fix this.
            stream_raw = IMSclient.get_waveforms(station = inventory,
                                    channel               = self.channel,   # FUTURE: ok to exclude this.
                                    starttime             = starttime, 
                                    endtime               = endtime,
                                    #attach_response      = True,
                                    #set_ims_network_code = True
                                    )

        #-----------------------------------------------------------
        # 2023-07-21 the following is needed since UIB etc no longer support MASS_DOWNLOADER.
        #-----------------------------------------------------------
        elif self.client_name == "UIB-NORSAR" and self.ifmass_downloader is False:
            client = Client(self.client_name)

            print("\nPreparing request for UIB-NORSAR data ...")
            starttime = reftime - self.tbefore_sec
            endtime   = reftime + self.tafter_sec
            print("UIB-NORSAR client: requesting station data for network/station/channel(s): %s/%s/%s ..." % (self.network, self.station, self.channel))
            inventory = Client.get_stations(network = self.network, 
                                         station    = self.station, 
                                         channel    = self.channel,
                                         starttime  = starttime, 
                                         endtime    = endtime,
                                         longitude  = self.elon,
                                         latitude   = self.elat,
                                         minradius  = kilometer2degrees(self.min_dist),
                                         maxradius  = kilometer2degrees(self.max_dist),
                                         )
            print("UIB-NORSAR client: done. Stations: ", inventory)
            #
            print("UIB-NORSAR client: fetching waveform data ...")
            st = client.get_waveforms(network='*', station='*', location='*', channel='*', starttime=t1, endtime=t2)

        ##-----------------------------------------------------------
        ## 2023-11-06 RASPISHAKE
        ##-----------------------------------------------------------
        #elif self.client_name == "RASPISHAKE" and self.ifmass_downloader is False:
        #    client = Client(self.client_name)

        #    print("\nPreparing request for RASPISHAKE data ...")
        #    starttime = reftime - self.tbefore_sec
        #    endtime   = reftime + self.tafter_sec
        #    print("RASPISHAKE client: requesting station data for network/station/channel(s): %s/%s/%s ..." % (self.network, self.station, self.channel))
        #    inventory = Client.get_stations(network = 'AM',
        #                                 station    = self.station, 
        #                                 channel    = self.channel,
        #                                 starttime  = starttime, 
        #                                 endtime    = endtime,
        #                                 longitude  = self.elon,
        #                                 latitude   = self.elat,
        #                                 minradius  = kilometer2degrees(self.min_dist),
        #                                 maxradius  = kilometer2degrees(self.max_dist),
        #                                 )
        #    print("RASPISHAKE client: done. Stations: ", inventory)
        #    #
        #    print("RASPISHAKE client: fetching waveform data ...")
        #    st = client.get_waveforms(network='AM', station='*', location='*', channel='*', starttime=t1, endtime=t2)
        #-----------------------------------------------------------
        ## OBSPY ROUTINES TO CONVERT STREAM 
        #-----------------------------------------------------------
        ## ~/miniconda3/envs/seismonpy_dev/lib/python3.7/site-packages/obspy/io/sac/sactrace.py
        ## https://docs.obspy.org/master/packages/autogen/obspy.io.sac.sactrace.html?highlight=sactrace#module-obspy.io.sac.sactrace
        #sachdr = _io.header_arrays_to_dict(self._hf, self._hi, self._hs,
        #                                   nulls=debug_headers,
        #                                   encoding=encoding)
        #stats = _ut.sac_to_obspy_header(sachdr)

        #-----------------------------------------------------------
        # OPTION X: READ DATA FROM LOCAL DATABASE. 
        # EXPECTS DATA IN OBSPY FORMATS: INVENTORY, STREAM
        # BE SURE TO SPECIFY: client_name="local" self.ifmass_downloader=False
        #-----------------------------------------------------------
        elif self.client_name=="local" and self.ifmass_downloader is False:
            from obspy.core.inventory.inventory import read_inventory
            from obspy import read

            starttime = reftime - self.tbefore_sec
            endtime   = reftime + self.tafter_sec

            ## TODO declare these from gw_X scripts
            ## NORDSTREAM DATA
            #path2inv = "20220926--nord_stream_data--Sweden_seismo_network/inventory_swedish_net"
            #path2str = "20220926--nord_stream_data--Sweden_seismo_network/ev1/*"    # EVENT 1
            #path2str = "20220926--nord_stream_data--Sweden_seismo_network/ev2/*"    # EVENT 2

            # KIRUNA EVENT
            path2dir = '/nobackup/celso/QUAKES/20200518011155328--sweden_kiruna_mine_collapse/data_SNSS_bjorn/data'
            path2inv = "%s/inventory_swedish_net" % path2dir
            path2str = "%s/*mseed"  % path2dir

            ## NWRussia mining event
            #path2inv = "/nobackup/celso/QUAKES/20220305001326100--mine_collapse_NW_russia/analysis/an20230714-01_BEAM_DATA_TORMOD/prepare_response_data/NB201.SEED"
            #path2str = "/nobackup/celso/QUAKES/20220305001326100--mine_collapse_NW_russia/analysis/an20230714-01_BEAM_DATA_TORMOD/CELSO_KHIBINY/beam_NO.NB201..BH*.sac" 

            stream_raw = read(path2str)
            inventory = read_inventory(path2inv)
            stream_raw.trim(starttime=starttime, endtime=endtime)
            print(inventory)
            print(stream_raw.__str__(extended=True))
            #sys.exit('stop')

        #-----------------------------------------------------------
        # NEXT: PROCESS THE STREAM AND INVENTORY
        #-----------------------------------------------------------

        # set reftime
        stream = obspy.Stream()
        stream = set_reftime(stream_raw, evtime)

        nsta = len(stream)
        if nsta < 1:
            print('STOP. No waveforms to process. N stations = %d\n' % nsta)
            sys.exit()

        #-----------------------------------------------------------
        # ADD SAC METADATA
        #-----------------------------------------------------------
        st2 = add_sac_metadata(stream, client_name=self.client_name, ev=event, 
                               inventory=inventory, taup_model= self.taupmodel, 
                               )
                               #phases=phases, phase_write = self.write_sac_phase)
        print('done adding SAC metadata. stalist inventory:\n', inventory)
        if(len(st2)<1):
            print('STOP. No waveforms left to process.')
            sys.exit()
        
        # Do some waveform QA
        do_waveform_QA(st2, self.client_name, event, evtime, 
                       self.tbefore_sec, self.tafter_sec)
        
        if self.demean:
            st2.detrend('demean')
            
        if self.detrend:
            st2.detrend('linear')
            
        if self.ifFilter:
            prefilter(st2, self.f1, self.f2, 
                    self.zerophase, self.corners, self.filter_type)
            
        if self.remove_response:
            resp_plot_remove(st2, self.ipre_filt, self.pre_filt, 
                    self.iplot_response, self.water_level,
                    self.scale_factor, 
                    inventory, self.outformat, self.ifverbose)
        # 20220718 TODO: ADD OPTION FOR CLIENT NORSAR-SEISMONPY
        #if self.remove_response and self.client_name != "NORSAR":
        #elif self.remove_response and self.client_name == "NORSAR":
        #    #response_remove_NORSAR(st2, self.ipre_filt, self.pre_filt, 
        #    response_remove_NORSAR(st2, self.ipre_filt, self.pre_filt, 
        #            self.iplot_response, self.water_level,
        #            self.scale_factor, 
        #            inventory, self.outformat, self.ifverbose)
        #        #tr.remove_response(inventory=stations, water_level=water_level, pre_filt=pre_filt, \
        #        #        output=outformat)
        else:
            # output RAW waveforms
            decon=False
            print("WARNING -- NOT correcting for instrument response")

        if self.scale_factor > 0:
            amp_rescale(st2, self.scale_factor)
            if self.client_name == "LLNL":
                amp_rescale_llnl(st2, self.scale_factor)


        # Set the sac header KEVNM with event name
        # This applies to the events from the LLNL database
        # NOTE this command is needed at the time of writing files, so it has to
        # be set early
        st2, evname_key = rename_if_LLNL_event(st2, evtime)
        self.evname = evname_key

        # SAVE STATION PLOT
        # Note: Plotted are stations in the inventory and NOT the ones with the traces
        # It could be possible that there might not be waveforms for some of these stations.
        print('plotting station map ...')
        try:
            fig = inventory.plot(projection="local", resolution="i", label = False, show=False)
            Catalog([self.ev]).plot(fig=fig, outfile=self.evname + '/station_map.pdf')
        except Exception as e:
            print("WARNING: Unable to create station map: ", e)

        # Get list of unique stations + locaiton (example: 'KDAK.00')
        print('creating list of unique stations ...')
        stalist = []
        for tr in stream.traces:
            #if self.ifverbose: print(tr)   # 2022-07-29 this is just creating a list. no processing. no need to print.
            station_key = "%s.%s.%s.%s" % (tr.stats.network, tr.stats.station,
                    tr.stats.location, tr.stats.channel[:-1])
            stalist.append(station_key)

        # Crazy way of getting a unique list of stations
        stalist = list(set(stalist))

        #  Resample
        if self.resample_TF == True:
            print('\nRESAMPLING DATA\n')
            print("New sample rate %f Hz" % self.resample_freq)
            # NOTE !!! tell the user if BOTH commands are disabled NOTE !!!
            if (self.client_name == "IRIS"):
                resample(st2, freq=self.resample_freq)
            elif (self.client_name == "LLNL"):
                resample_cut(st2, self.resample_freq, evtime, self.tbefore_sec, self.tafter_sec)
        else:
            print("WARNING. Will not resample. Using original rate from the data: %f Hz" % self.resample_freq)

        # match start and end points for all traces
        st2 = trim_maxstart_minend(stalist, st2, self.client_name, event, evtime, 
                self.resample_TF, self.resample_freq, 
                self.tbefore_sec, self.tafter_sec, self.ifverbose)
        if len(st2) == 0:
            raise ValueError("no waveforms left to process!")

        # save raw waveforms in SAC format
        if self.isave_raw:
            path_to_waveforms = evname_key + "/RAW"
            write_stream_sac_raw(stream_raw, path_to_waveforms, 
                                 evname_key, self.client_name, event, stations=inventory)

        # Taper waveforms (optional; Generally used when data is noisy- example: HutchisonGhosh2016)
        # https://docs.obspy.org/master/packages/autogen/obspy.core.trace.Trace.taper.html
        # To get the same results as the default taper in SAC, use max_percentage=0.05 and leave type as hann.
        # Note: Tapering also happens while resampling (see util_write_cap.py)
        if self.taper:
            st2.taper(max_percentage=self.taper, type='hann',max_length=None, side='both')

        # save processed waveforms in SAC format
        # evname_key/RAW_processed = traces after waveform_QA + demean + detrend +
        #                            resample + remove response + filtering +
        #                            resampling + scaling + tapering
        # NOTE: The orientation is same as that of extracted waveforms
        #       Waveforms are rotated to ENZ, in case they are not already orientated,
        #       in the next step (self.rotateRTZ)
        if self.isave_raw_processed:
            path_to_waveforms = os.path.join(evname_key, 'RAW_processed')
            write_stream_sac(st2, path_to_waveforms, evname_key)

        # Rotate to ENZ (save: optional)
        #if self.rotateENZ:
        #st2 = rotate2ENZ(st2, evname_key, self.isave_ENZ, self.icreateNull, self.ifverbose)

        print ('\nBEGIN ROTATE COMPONENTS ...')
        if self.rotateENZ:
            st2 = rotate2ENZ(st2, evname_key, self.isave_ENZ, self.icreateNull, self.ifverbose)

        # rotate to UVW and save
        if self.rotateUVW:
            rotate2UVW(st2, evname_key) 

        # Rotate to RTZ and save
        if self.rotateRTZ:
            rotate2RTZ(st2, evname_key, self.ifverbose) 
            
        # save CAP weight files
        if self.output_cap_weight_file:
            write_cap_weights(st2, evname_key, self.client_name, event, self.ifverbose)

        # save event info
        if self.output_event_info:
            write_ev_info(event, evname_key)

        # Plot spectrograms
        if self.ifplot_spectrogram:
            plot_spectrogram(st2, evname_key)

        # save pole zero file (Needed for MouseTrap)
        if self.ifsave_sacpaz:
            write_resp(inventory,evname_key)

        # save station inventory as XML file
        if self.ifsave_stationxml:
            xmlfilename = evname_key + "/stations.xml"
            try:
                inventory.write(xmlfilename, format="stationxml", validate=True)
            except:
                print('Could not create stationxml file')
        
        # Path to the asdf_converter script        
        if self.ifsave_asdf:
            # save RTZ
            asdf_filename = evname_key + "/" + evname_key + ".h5"
            os.system("../asdf_converters/asdf_converters/sac2asdf.py "
                      + evname_key + " " + asdf_filename + " observed")
            # save NEZ
            nez_dir = evname_key + "/ENZ/"
            nez_asdf_filename = nez_dir + evname_key + ".h5"
            os.system("../asdf_converters/asdf_converters/sac2asdf.py "
                      + nez_dir + " " + nez_asdf_filename + " observed")

        print ('\nDone. Waveform data saved to directory %s/\n' % evname_key)

    def copy(self):
        '''
        create of copy of itself
        '''
        return deepcopy(self)

    def reference_time_place(self):
        '''
        returns an event object with different origin time and location 
        (i.e. not centered around the earthquake). Stations will be subsetted
        based on reference origin time and location
        '''

        self.ref_time_place = self.ev.copy()
        self.ref_time_place.origins[0].latitude = self.rlat
        self.ref_time_place.origins[0].longitude = self.rlon
        self.ref_time_place.origins[0].time = self.rtime

    def get_event_object(self):
        '''
        update events otime,lat,lon and mag with IRIS (or any other clients) catalog
        '''
        
        # get parameters from the cataog
        if self.use_catalog == 1:
            print("WARNING using event data from the IRIS catalog")
            cat = self.client.get_events(
                starttime = self.otime - self.sec_before_after_event,
                endtime = self.otime + self.sec_before_after_event)
            self.ev = cat[0]
            
            # use catalog parameters
            self.otime = self.ev.origins[0].time
            self.elat = self.ev.origins[0].latitude
            self.elon = self.ev.origins[0].longitude
            self.edep = self.ev.origins[0].depth
            self.emag = self.ev.magnitudes[0].mag
            
        # use parameters from the input file
        else:
            print("WARNING using event data from user-defined catalog")
            #self.ev = Event()
            org = Origin()
            org.latitude = self.elat
            org.longitude = self.elon
            org.depth = self.edep
            org.time = self.otime
            mag = Magnitude()
            mag.mag = self.emag
            mag.magnitude_type = "Mw"
            self.ev.origins.append(org)
            self.ev.magnitudes.append(mag)
    
    def get_events_client(self):
        '''
        get absolute and reference event object
        20220718 TODO: ADD OPTION FOR CLIENT NORSAR-SEISMONPY (LOCALLY ACCESSIBLE NORSAR DATA)
        '''

        # 2022-10-17 option to read local datasets
        if self.client_name == "local":
            self.get_event_object()

            # use a different reference time and place for station subsetting
            if self.rlat is not None:
                self.reference_time_place()
            # or use reference same as the origin
            else:
                self.ref_time_place = self.ev

        # Option for INTERFACE NORSAR-SEISMONPY AND IMS-NMS CLIENT
        elif self.client_name == "IMS-SMP":
            #self.client = NORclient(self.client_name)
            #self.client = client()

            # get event object
            self.get_event_object()

            # use a different reference time and place for station subsetting
            if self.rlat is not None:
                self.reference_time_place()
            # or use reference same as the origin
            else:
                self.ref_time_place = self.ev
        
        # LLNL
        elif self.client_name == "LLNL":
            import llnl_db_client
            self.client = llnl_db_client.LLNLDBClient(
                "/store/raw/LLNL/UCRL-MI-222502/westernus.wfdisc")

            # get event time and event ID
            cat = self.client.get_catalog()
            mintime_str = "time > %s" % (self.otime - 
                                         self.sec_before_after_event)
            maxtime_str = "time < %s" % (self.otime + 
                                         self.sec_before_after_event)
            print(mintime_str + "\n" + maxtime_str)

            self.ev = cat.filter(mintime_str, maxtime_str)
        
            if len(self.ev) > 0:
                self.ev = self.ev[0]
                # Nothing happens here.  We can change later
                self.ref_time_place = self.ev
                print(len(self.ev))
            else:
                print("WARNING. No events in the catalog for the given time period")
                #sys.exit()
        # IRIS
        #if self.client_name != "LLNL":
        else:
            # import functions to access waveforms
            if not self.user and not self.password:
                self.client = Client(self.client_name,debug=True, timeout=600)
            else:
                self.client = Client(self.client_name, user=self.user, 
                                     password=self.password, debug=True, timeout=600)
                # will only work for events in the 'IRIS' catalog
                # (future: for Alaska events, read the AEC catalog)

            # get event object
            self.get_event_object()

            # use a different reference time and place for station subsetting
            if self.rlat is not None:
                self.reference_time_place()
            # or use reference same as the origin
            else:
                self.ref_time_place = self.ev

        # print client and event info
        print(self.ev)

    def save_extraction_info(self):
        # track git commit
        os.system('git log | head -12 > ./' + self.evname + 
                  '/' + self.evname + '_last_2git_commits.txt')
        # save filenames in a file for checking
        fname = self.evname + '/' + self.evname + '_all_filenames'
        fcheck = open(fname,'w')

        os.system('ls -1 ' + self.evname + '/* > ' +  fname)
