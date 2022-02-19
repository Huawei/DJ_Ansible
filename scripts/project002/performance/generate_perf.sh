#!/bin/bash

su ossadm -c ". /opt/oss/manager/agent/bin/engr_profile.sh;python generate_perf_csv.py $*"