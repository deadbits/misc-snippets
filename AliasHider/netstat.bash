#!/bin/bash
_netstat() {
        netstat $1 | sed '/10.0.1.38/d'
}

_netstat $1