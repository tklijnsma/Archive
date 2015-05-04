#!/bin/bash

# grid-control: https://ekptrac.physik.uni-karlsruhe.de/trac/grid-control

echo "Searching for CMSSW environment..."
if [ -n "$VO_CMS_SW_DIR" ]; then
	echo "[CMS-SITE] Using $VO_CMS_SW_DIR"
else
	# Fallback - try different default values for CMSSW directory

	# Fix for OSG sites
	if [ -n "$OSG_APP" -a -d "$OSG_APP" ]; then
		export VO_CMS_SW_DIR="$OSG_APP/cmssoft/cms"
		echo "[OSG-SITE] Using $VO_CMS_SW_DIR"

	# User forced directories / known during development
	elif [ -n "$CMSSW_DIR_USER" -a -d "$CMSSW_DIR_USER" ]; then
		export VO_CMS_SW_DIR="$CMSSW_DIR_USER"
		echo "[USER-SITE] Using $VO_CMS_SW_DIR"
	elif [ -n "$CMSSW_DIR_PRO" -a -d "$CMSSW_DIR_PRO" ]; then
		export VO_CMS_SW_DIR="$CMSSW_DIR_PRO"
		echo "[PROJ-SITE] Using $VO_CMS_SW_DIR"

	# Try other software directories
	elif [ -d "/afs/cern.ch/cms" ]; then
		export VO_CMS_SW_DIR="/afs/cern.ch/cms"
		echo "[AFS-SITE] Using $VO_CMS_SW_DIR"
	fi
fi
