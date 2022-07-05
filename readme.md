# _SWEEP_: a utility for seismic waveform discovery, extraction and processing

## What it does
* Search + fetch + process seismic waveforms from online repositories
* Anywhere on Earth* for any time period and search radius
* Prepare and QA waveforms for various analyses, in particular earthquake source estimation 

(*NEXT: Earth's Moon and Mars)

## How it works
0. check for earthquakes automatically* or enter earthquake information manually
1. fetch all possible waveform data across open networks (and some closed networks)
2. Perform various checks on the data and prepare the waveforms for analysis

(*Using a built-in utility, or coupling with an external one)

## Installation
``
git clone git@github.com:celsoa/sweep.git
``

## Usage
```
cd sweep
python run_sweep.py <inputfile>
```
* This command will extract the waveforms for the geographic location and time listed in ``inputfile``
* When the script finishes, it will save the waveforms in a folder with the same name as the time listed in ``inputfile``
* For example, if the time is ``2000-12-24T23:59:00`` the output folder will be named ``20001224235900``

## Waveform corrections, QA checks, summary reports
* correct for instrument response
* demean, detrend (linear, quadratic, etc)
* resample
* pre- and post-filter waveforms (causal, acausal, lowpass, highpass, etc)
* interpolate missing data
* rescale waveform amplitudes (mm, cm, m, etc) 
* various status/summary/QA reports: waveform quality, SNR, spectrograms, instrument response, station map, station .xml file 

## Waveform processing for earthquake analysis 
* rotate to source-receiver frame (RTZ) using sensor orientations
* rotate to UVW triaxial orthogonal frame of the T120PH Nanometrics sensor (useful for isolating spurious signals to sensor components)
* add null traces so that there are always 3 components (required when rotating)
* access embargoed data sets (requires user name and password)
* write SAC files with headers
* interface with other databases (see below)

## Interface with various data centers and databases
### Open data centers 
* IRIS
* EIDA
* NORSAR
* Raspberry Shake

### Restricted data centers or embargoed datasets (usually require a password)
* IMS
* ?

### The LLNL database of nuclear explosion and earthquake waveforms
*  An assembled western United States dataset for regional seismic analysis
  ISSO 9660 CD, LLNL release UCRL-MI-222502, W. Walter et al. (2006)
* The database can be downloaded from IRIS DMC at
  https://ds.iris.edu/mda/18-001
* The package needed to access these waveforms is here:
   https://github.com/krischer/llnl_db_client
* Follow the install instructions, then set a symbolic link as
   ``ln -s /PATH_TO_LLNL_CLIENT/llnl_db_client .``

