#!/bin/bash

python2 -m SimpleHTTPServer 8000 &
~/node_modules/.bin/babel --presets react --watch src --out-dir dist
