#!/bin/bash

nmap -sV --script vulners $1 | grep -o -P "CVE-\d*-\d*" | sort | uniq
