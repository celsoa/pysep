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
from obspy.core.event import Event, Origin, Magnitude, Catalog

from obspy.clients.fdsn import RoutingClient    # 2019-06-18 FOR ALPARRAY DATA

from scipy import signal
import pickle

from util_write_cap import *
from obspy.taup import TauPyModel
from obspy.geodetics import kilometer2degrees
import math

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
        # DEFAULT SETTINGS (see getwaveform.py)
        self.idb = 1    # default: =1-IRIS; =2-AEC; =3-LLNL; =4-Geoscope
        self.client = Client()

        # event parameters
        self.use_catalog = 1              # use an existing catalog (=1) or specify your own event parameters (see iex=9)
        self.sec_before_after_event = 10  # time window to search for a target event in a catalog
        self.min_dist = 0 
        self.max_dist = 2000
        self.min_az = 0 
        self.max_az = 360
        self.min_lat = None
        self.max_lat = None
        self.min_lon = None
        self.max_lon = None
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
        self.station = '*,-PURD,-NV33,-GPO'  # all stations except -(these)
        self.channel = '*'                   # all channels     
        self.overwrite_ddir = 1              # 1 = delete data directory if it already exists
        self.icreateNull = 1                 # create Null traces so that rotation can work (obsby stream.rotate require 3 traces)
        self.phase_window = False            # Grab waveforms using phases
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
        self.f1 = 1/1000            # NOTE DOES NOT CHANGE WHEN ipre_filt=2
        self.f2 = 20                # NOTE DOES NOT CHANGE WHEN ipre_filt=2
        self.zerophase = True             # = False (causal), = True (acausal)
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

        # For CAP
        self.resample_TF = True           # if False then resample_freq is taken from SAC files
        self.resample_freq = 50           # 0 causes errors. Use resample_TF instead
        self.scale_factor = 1             # for CAP use 10**2  (to convert m/s to cm/s)

        # Pre-processing (manily for CAP)
        self.output_cap_weight_file = True# output cap weight files
        self.detrend = True               # detrend waveforms
        self.demean = True                # demean waveforms
        self.taper = False                # this could also be a fraction between 0 and 1 (fraction to be tapered from both sides)
        self.output_event_info = True     # output event info file
        self.outformat = 'VEL'            # Intrument response removed waveforms could be saved as 'VEL' 'DISP' 'ACC'
        self.ifsave_sacpaz = False        # save sac pole zero (needed as input for MouseTrap module)
        self.remove_response = True       # remove instrument response 
        self.iplot_response = False       # plot response function
        self.ifplot_spectrogram = False   # plot spectrograms 
        self.ifsave_stationxml = True     # save station xml file (for adjoint tomo)

        # Waveforms to be saved
        self.rotateRTZ = True             # Rotate and save the RTZ components
        self.rotateUVW = False            # Rotate and save the UVW components
        self.isave_raw = False            # save raw waveforms
        self.isave_raw_processed = False  # save processed waveforms just before rotation to ENZ
        #self.rotateENZ = True            # rotate extracted waveforms to ENZ
        self.isave_ENZ = True             # save ENZ

        # username and password for embargoed IRIS data
        # Register here: http://ds.iris.edu/ds/nodes/dmc/forms/restricted-data-registration/
        self.user = None
        self.password = None

        # To output lots of processing info
        self.ifverbose = False

    def run_get_waveform(self):
        """
        Get SAC waveforms for an event
        
        basic usage:
        run_get_waveform(event)
        
        c              -  client
        event          -  obspy Event object
        ref_time_place -  reference time and place (other than origin time and place - for station subsetting)
        """
        
        c = self.client
        event = self.ev
        ref_time_place = self.ref_time_place

        evtime = event.origins[0].time
        reftime = ref_time_place.origins[0].time
        
        if (self.idb == 1) or (self.idb == 5):
            # 2019-03-12 I added idb #5 here and not in a separate block since
            # the station retrieval is common to #1 and #5 and I rather not repeat the same block.
            # note that CH stations may not provide all sensor metadata (required when using idb #1) and this crashes with later requests in the code
            # another option is to add sta retrieval after #3 below but unsure if this creates conflicts.
            # TODO use 'is' instead of 'in' to avoid wrong calls (eg FZ or GFZ)
            if ("BK" in self.network) or ("BG" in self.network) or ("BP" in self.network):
                # NOTE BK network doesn't return data when using the IRIS client.
                # this option switches to NCEDC if BK is in networkname.
                client_name = "NCEDC"
            elif "CH" in self.network:
                client_name = "ETH" 
            elif "GFZ" in self.network:
                client_name = "GFZ" 
            elif "Z3" in self.network:      # 2019-07-31 for AlpArray
                client_name = "ORFEUS" 
                #client_name = "GFZ" 
                #client_name = "ETH" 
            elif "IV" in self.network:
                client_name = "INGV" 
            elif "DE" in self.network:
                client_name = "EMSC"     # or BGR GFZ LMU ...
            else:
                client_name = "IRIS"    # default

            c = Client(client_name)
            #-----------------------------------------------------------
            # Check if requesting AlpArray data
            # the following are ongoing TESTS (alparray data)
            #c = Client(client_name, password='895849_sed')
            #c = Client(client_name, password='420523_eth')
            #c = Client(client_name, password='908588_geod_res')
            #c = RoutingClient('iris-federator') # 2019-06-18 This downloads a list of station data, but no waveforms. Also it requires removing radius-related infor (below) and doesn't have a field for eidatoken.
            #c = RoutingClient('iris-federator', credentials={'EIDA_TOKEN': './eidatoken'}, debug=True) 
            #c = RoutingClient('iris-federator', credentials={'EIDA_TOKEN': './eidatoken'}) 
            #c = RoutingClient('eida-routing',   credentials={'EIDA_TOKEN': '/home/calvizur/.eidatoken'}, debug=True) # 2019-07-31 TEST?
            ## try again AlpArray, arclink
            # NB doesnt work. 'response' level is not accepted which means I would have to prepare data manually
            # option: use script similar to Veronica's
            #c = Client(user='895849_sed') # test, AlpArray Client
            #c.max_status_requests = 2000
            if "Z3" in self.network:
                # 2019-07-31 WORKS! (bondo event)
                # replace client if requesting AlpArray data
                c = RoutingClient('iris-federator', credentials={'EIDA_TOKEN': '/home/calvizur/.eidatoken'}, debug=True) 
            #-----------------------------------------------------------
            print(c)
            print("\n** WARNING ** Preparing request for client", client_name)
            print("Download stations...")
            if "Z3" in self.network:
                # *** alparray only ***
                stations = c.get_stations(
                        network     = self.network, 
                        station     = self.station,
                        channel     = self.channel,
                        starttime   = reftime - self.tbefore_sec, 
                        endtime     = reftime + self.tafter_sec,
                        level="response")
            else:
                # default
                stations = c.get_stations(
                        network     = self.network, 
                        station     = self.station,
                        channel     = self.channel,
                        starttime   = reftime - self.tbefore_sec, 
                        endtime     = reftime + self.tafter_sec,
                        #----------------------------------------------------------
                        # NOTE RoutingClient (AlpArray) does not have the following
                        minlatitude = self.min_lat,
                        maxlatitude = self.max_lat,
                        minlongitude = self.min_lon,
                        maxlongitude = self.max_lon,
                        longitude   = self.elon,  # required for maxradius
                        latitude    = self.elat,  # required for maxradius 
                        maxradius   = 18,         # note 18 deg ~ 2000 km
                        #----------------------------------------------------------
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
            t1s = []
            t2s = []
            phases = self.phases
            if self.phase_window:

                #model = TauPyModel(model=taupmodel)
                model = TauPyModel(model=self.taupmodel)
                
                for net in stations:
                    for sta in net:
                        dist, az, baz = obspy.geodetics.gps2dist_azimuth(
                        event.origins[0].latitude, event.origins[0].longitude, sta.latitude, sta.longitude)
                        dist_deg = kilometer2degrees(dist/1000,radius=6371)
                        Phase1arrivals = model.get_travel_times(source_depth_in_km=event.origins[0].depth/1000,distance_in_degree=dist_deg,phase_list=[phases[0]])
                        if len(Phase1arrivals)==0:
                            if phases[0]=="P":
                                phases[0]="p"
                            elif phases[0]=="p":
                                phases[0]="P"
                            elif phases[0]=="S":
                                phases[0]="s"
                            elif phases[0]=="s":
                                phases[0]="S"
                            Phase1arrivals = model.get_travel_times(source_depth_in_km=event.origins[0].depth/1000,distance_in_degree=dist_deg,phase_list=[phases[0]])

                        Phase2arrivals = model.get_travel_times(source_depth_in_km=event.origins[0].depth/1000,distance_in_degree=dist_deg,phase_list=[phases[1]])
                        if len(Phase2arrivals)==0:
                            if phases[1]=="P":
                                phases[1]="p"
                            elif phases[1]=="p":
                                phases[1]="P"
                            elif phases[1]=="S":
                                phases[1]="s"
                            elif phases[1]=="s":
                                phases[1]="S"
                            Phase2arrivals = model.get_travel_times(source_depth_in_km=event.origins[0].depth/1000,distance_in_degree=dist_deg,phase_list=[phases[1]])

                        #somearr = model.get_travel_times(source_depth_in_km=event.origins[0].depth/1000,distance_in_degree=dist_deg)
                        #print("Print arrivals")
                        #print(somearr)

                        try:
                            if Phase2arrivals[0].time < Phase1arrivals[0].time:
                                # You are assuming that the first index is the first arrival.  Check this later.
                                t1s.append(event.origins[0].time + Phase2arrivals[0].time - self.tbefore_sec)
                                t2s.append(event.origins[0].time + Phase1arrivals[0].time + self.tafter_sec)
                            else:
                                t1s.append(event.origins[0].time + Phase1arrivals[0].time - self.tbefore_sec)
                                t2s.append(event.origins[0].time + Phase2arrivals[0].time + self.tafter_sec)
                        except:
                            t1s.append(reftime - self.tbefore_sec)
                            t2s.append(reftime + self.tafter_sec)

            else:
                t1s = [reftime - self.tbefore_sec]
                t2s = [reftime + self.tafter_sec]
            
            print("Downloading waveforms...")
            # this needs to change
            bulk_list = make_bulk_list_from_stalist(stations,t1s,t2s, 
                    channel=self.channel)

            stream_raw = c.get_waveforms_bulk(bulk_list)
            # save ev_info object
            pickle.dump(self,open(self.evname + '/' + 
                                  self.evname + '_ev_info.obj', 'wb'))    
         
        elif self.idb==3:
            client_name = "LLNL"
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
        elif self.idb == 99:
            # IRIS federator to figure out who has waveform data for that
            # particular query and subsequently call the individual data
            # centers to actually get the data. 
            # https://docs.obspy.org/packages/obspy.clients.fdsn.html
            print("Preparing request through iris-federator")
            c = RoutingClient('iris-federator', debug=True)
            stations = c.get_stations(
                    #network     = self.network, 
                    #station     = self.station,
                    channel     = self.channel,
                    starttime   = reftime - self.tbefore_sec, 
                    endtime     = reftime + self.tafter_sec,
                    #minlatitude = self.min_lat,
                    #maxlatitude = self.max_lat,
                    #minlongitude = self.min_lon,
                    #maxlongitude = self.max_lon,
                    longitude   = self.elon,  # required for maxradius
                    latitude    = self.elat,  # required for maxradius 
                    #maxradius   = 18,         # note 18 deg ~ 2000 km
                    maxradius   = 18,         # note 18 deg ~ 2000 km
                    level="response")
            print("Downloading waveforms...")
            # this needs to change
            bulk_list = make_bulk_list_from_stalist(stations,t1s,t2s, 
                    channel=self.channel)

            stream_raw = c.get_waveforms_bulk(bulk_list)
            # save ev_info object
            pickle.dump(self,open(self.evname + '/' + 
                                  self.evname + '_ev_info.obj', 'wb'))    
        #-----------------------------------------------------------
         
        # set reftime
        stream = obspy.Stream()
        stream = set_reftime(stream_raw, evtime)
        
        print("--> Adding SAC metadata...")
        if self.ifverbose: print(inventory)
        st2 = add_sac_metadata(stream, idb=self.idb, ev=event, stalist=inventory, 
                               taup_model= self.taupmodel, phases=phases, 
                               phase_write = self.write_sac_phase)
        
        # Do some waveform QA
        do_waveform_QA(st2, client_name, event, evtime, 
                       self.tbefore_sec, self.tafter_sec)
        
        if self.demean:
            st2.detrend('demean')
            
        if self.detrend:
            st2.detrend('linear')
            
        if self.remove_response:
            resp_plot_remove(st2, self.ipre_filt, self.pre_filt, 
                    self.iplot_response, 
                    self.scale_factor, 
                    stations, self.outformat, self.ifverbose)
        else:
            # output RAW waveforms
            decon=False
            print("WARNING -- NOT correcting for instrument response")

        if self.ifFilter:
            prefilter(st2, self.f1, self.f2, 
                    self.zerophase, self.corners, self.filter_type)
            
        if self.scale_factor > 0:
            amp_rescale(st2, self.scale_factor)
            if self.idb ==3:
                amp_rescale_llnl(st2, self.scale_factor)


        # Set the sac header KEVNM with event name
        # This applies to the events from the LLNL database
        # NOTE this command is needed at the time of writing files, so it has to
        # be set early
        st2, evname_key = rename_if_LLNL_event(st2, evtime)
        self.evname = evname_key

        # save station plot
        # Note: Plotted are stations in the inventory and NOT the ones with the traces
        # It could be possible that there might not be waveforms for some of these stations.
        try:
            fig = inventory.plot(projection="local", resolution="i", label = False, show=False)
            Catalog([self.ev]).plot(fig=fig, outfile=self.evname + '/station_map.pdf')
        except:
            print("There is a problem with creating the station map!")

        # Get list of unique stations + locaiton (example: 'KDAK.00')
        stalist = []
        for tr in stream.traces:
            if self.ifverbose: print(tr)
            station_key = "%s.%s.%s.%s" % (tr.stats.network, tr.stats.station,
                    tr.stats.location, tr.stats.channel[:-1])
            stalist.append(station_key)

        # Crazy way of getting a unique list of stations
        stalist = list(set(stalist))

        #  Resample
        if self.resample_TF == True:
            # NOTE !!! tell the user if BOTH commands are disabled NOTE !!!
            if (client_name == "IRIS"):
                resample(st2, freq=self.resample_freq)
            elif (client_name == "LLNL"):
                resample_cut(st2, self.resample_freq, evtime, self.tbefore_sec, self.tafter_sec)
        else:
            print("WARNING. Will not resample. Using original rate from the data")

        # match start and end points for all traces
        st2 = trim_maxstart_minend(stalist, st2, client_name, event, evtime, 
                self.resample_TF, self.resample_freq, 
                self.tbefore_sec, self.tafter_sec, self.ifverbose)
        if len(st2) == 0:
            raise ValueError("no waveforms left to process!")

        # save raw waveforms in SAC format
        if self.isave_raw:
            path_to_waveforms = evname_key + "/RAW"
            write_stream_sac_raw(stream_raw, path_to_waveforms, 
                                 evname_key, self.idb, event, stations=inventory)

        # Taper waveforms (optional; Generally used when data is noisy- example: HutchisonGhosh2016)
        # https://docs.obspy.org/master/packages/autogen/obspy.core.trace.Trace.taper.html
        # To get the same results as the default taper in SAC, use max_percentage=0.05 and leave type as hann.
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
        st2 = rotate2ENZ(st2, evname_key, self.isave_ENZ, self.icreateNull, self.ifverbose)

        # rotate to UVW and save
        if self.rotateUVW:
            rotate2UVW(st2, evname_key) 

        # Rotate to RTZ and save
        if self.rotateRTZ:
            rotate2RTZ(st2, evname_key, self.ifverbose) 
            

        # save CAP weight files
        if self.output_cap_weight_file:
            write_cap_weights(st2, evname_key, client_name, event, self.ifverbose)

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
        print("### DEBUG ###")

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
        '''

        # IRIS
        if (self.idb == 1) or (self.idb == 5):
            # import functions to access waveforms
            if not self.user and not self.password:
                self.client = Client("IRIS")
            else:
                self.client = Client("IRIS", user=self.user, 
                                     password=self.password)
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
        
        # LLNL
        if self.idb == 3:
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
