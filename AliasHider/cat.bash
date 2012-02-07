#!/bin/bash
_cat() {
    cat $1 | sed -e '/haxor:/d' | sed -e '/BLAH.....:/d'
}

_cat $1