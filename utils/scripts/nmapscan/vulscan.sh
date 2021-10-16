#!/bin/bash

nmap -sV --script utils/scripts/nmap/vulscan/vulscan.nse $1 | grep -o -P "CVE-\d*-\d*" | sort | uniq
