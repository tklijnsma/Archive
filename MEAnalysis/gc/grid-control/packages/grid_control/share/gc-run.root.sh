#!/bin/sh

# grid-control: https://ekptrac.physik.uni-karlsruhe.de/trac/grid-control

# 110 - ROOT area not found

source $MY_LANDINGZONE/gc-run.lib || exit 101

echo "ROOT module starting"
echo
echo "---------------------------"

export ROOTSYS=$MY_ROOTSYS
export PATH="$PATH:$ROOTSYS/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$ROOTSYS/lib:$ROOTSYS/lib/root:."
echo -n "ROOT Version: "
$ROOTSYS/bin/root-config --version || fail 110
echo "---------------------------"
echo

eval $@
