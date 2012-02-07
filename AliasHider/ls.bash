#!/bin/bash
_ls() {
    if [[ $1 =~ 'l' ]]
    then
        ls $1 | sed -e '/AliasHider.py/d'
    else
        ls $1 | sed -e '/AliasHider.py/d' | sed ':a;N;$!ba;s/\n/ /g'
    fi
}

_ls $1
