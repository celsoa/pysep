import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        # DATA PREPARATION / PROCESSING
        ev_info.use_catalog = 0
        ev_info.ifmass_downloader = True
        #ev_info.iris_federator = True
        ev_info.idb = 1 # 1 IRIS
        ev_info.ifverbose = True    # output all proccessing steps

        #keep stations with missing components and fill the missing component with a null trace (MPEN)
        #Be sure to set the null component to 0 in the weight file when running cap
        #ev_info.icreateNull = 1
        ev_info.icreateNull = 1

        ev_info.overwrite_ddir = 0  

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False

        ##-----------------------------------------------------------
        ## EVENT INFO USGS
        ## 67.826°N 20.267°E 1.0 km depth , https://earthquake.usgs.gov/earthquakes/eventpage/us70009ja2/technical
        #ev_info.otime = obspy.UTCDateTime("2020-05-18T01:11:56") # 2020-05-18 01:11:56
        #ev_info.elon = 20.267
        #ev_info.elat = 67.826
        #ev_info.edep = 1000
        #ev_info.emag = 4.9

        ##-----------------------------------------------------------
        # EVENT INFO ISC CATALOG
        # http://www.isc.ac.uk/cgi-bin/web-db-run?event_id=618291845&out_format=ISF2&request=COMPREHENSIVE
        #
        # ISC 	2020/05/18 01:11:55.328 	67.7951 	20.1931 	0.0
        # 
        # NORSAR  http://www.norsardata.no/NDC/bulletins/regional/2020/05/22759.html
		#  Origin ID   22759 CENTRAL NORBOTTEN SWEDEN                                                        
		#      Origin time        Lat        Lon     Depth    Trms  Azrms  Nph  Nsta   Mag     Majax   Minax  Strike   Area
		#  2020-139:01.11.57.10  67.8404    20.2626   0.10    1.35 999.00   -1   30    4.72     -1.0    -1.0   -1.0      3.1 
        #
        # UPSALA
        # Date       Time        Err   RMS Latitude Longitude  Smaj  Smin  Az Depth   Err Ndef Nsta Gap  mdist  Mdist Qual   Author      OrigID
        # 2020/05/18 01:11:56.20   0.00 0.200  67.8400   20.2030  0.00   0.0  -1   0.0f             11                       se UPP         615403639
        #
        ##-----------------------------------------------------------
        ## ISC ORIGID: 616463727, ISC location
        ## I computed an FMT with this otime+hypocenter, using open+IMS stations. 
        ## Also shared with infrasound group.
        ## Keep for reference.
        #ev_info.otime = obspy.UTCDateTime("2020-05-18T01:11:55.328") # obtained on 2022-08-31 13:38
        #ev_info.elon = 20.1931
        #ev_info.elat = 67.7951
        #ev_info.edep = 0
        #ev_info.emag = 4.7 # MW  4.7 GCMT -- from the link above 
        #-----------------------------------------------------------
        ## 2022-10-10 use the UPPSALA location per Tormod's suggestion (SSA 2023 presentation)
        ## ISC ORIGID: 615403639, UPP location
        ## 2020/05/18 01:11:56.20   0.00 0.200  67.8400   20.2030  0.00   0.0  -1   0.0f             11                       se UPP         615403639
        #ev_info.otime = obspy.UTCDateTime("2020-05-18T01:11:56.20") # last checked 2022-10-10
        #ev_info.elon = 20.2030
        #ev_info.elat = 67.8400
        #ev_info.edep = 0
        #ev_info.emag = 4.1  # ML 4.1 UPP 615403639
        #-----------------------------------------------------------
        # 2023-07-21 latest from Bjorn Lunde:  2020-05-18 01:11:56.219     67.83965  20.20759
        #
        # From: Björn Lund <bjorn.lund@geo.uu.se>
        # Sent: Tuesday, 27 June 2023 08:22
        # To: Celso Alvizuri <Celso.Alvizuri@norsar.no>
        # Cc: Quentin Brissaud <Quentin.Brissaud@norsar.no>; Antoine Turquet <Antoine@norsar.no>
        # Subject: Re: Kiruna time and location
        # 
        # [You don't often get email from bjorn.lund@geo.uu.se. Learn why this is important at https://aka.ms/LearnAboutSenderIdentification ]
        # 
        # Hi Celso,
        # 
        # One of my contacts at LKAB is on holiday, and the other didn't know
        # about conversions between the coordinate systems, so you may just have
        # to go with the SNSN location and time. Our location includes the P- and
        # S-arrivals of the two closest stations, they saturated on the surface
        # waves so the arrivals are fine. That probably makes it the most
        # accurate, outside of the mine system. So I would go with:
        # 
        # 2020-05-18 01:11:56.219
        # 67.83965  20.20759  (obviously too high accuracy... )
        # The formal error ellipse has major axis 330 m at 324 deg azimuth and 240
        # m minor axis. Judging from the map I would say that the location is
        # likely within 500 m of the real hypocenter, but I don't know exactly
        # where that is.
        # 
        # Cheers,
        # Björn
        #
        ev_info.otime = obspy.UTCDateTime("2020-05-18T01:11:56.219") # 2023-07-21 LATEST. From Bjorn.
        ev_info.elon = 20.20759
        ev_info.elat = 67.83965
        ev_info.edep = 0
        ev_info.emag = 4.1  # ML 4.1 UPP 615403639
        #-----------------------------------------------------------

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.network = '*'
        ev_info.channel = 'BH?,HH?'
        ev_info.resample_TF = True
        ev_info.resample_freq = 20
        ev_info.scale_factor = 100
        #ev_info.phase_window = False

        ##-----------------------------------------------------------
        ## UIB-NORSAR REQUEST
        ##-----------------------------------------------------------
        #ev_info.client_name = "UIB-NORSAR" 
        #ev_info.ifmass_downloader = False

        ##-----------------------------------------------------------
        ## IMS REQUEST
        ## Be sure to specify each IMS station. wildcard '*' is not implemented.
        ##-----------------------------------------------------------
        #ev_info.idb = 0
        #ev_info.ifmass_downloader = False
        #ev_info.client_name = 'IMS-SMP'
        ##ev_info.station = 'FINES'
        ##ev_info.station = 'I37NO'
        #ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
        #                        # do not use '*' bc it finds BDF LDA data with no instrument response.
        ##ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        #ev_info.icreateNull = 1 # NOTE USE. Else vertical-components will not be saved.

        ##-----------------------------------------------------------
        ## LOCAL DATA REPOSITORY, e.g. for data from Swedish Network
        ##-----------------------------------------------------------
        #ev_info.idb = 0
        #ev_info.ifmass_downloader = False
        #ev_info.client_name = 'local'


    return(ev_info)
