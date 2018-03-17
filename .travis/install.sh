#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    if [[ $? -eq 0 ]]; then
	brew install python
	if [[ $? -eq 0 ]]; then
		 curl -O http://python-distribute.org/distribute_setup.py
		 python distribute_setup.py
		 if [[ $? -eq 0 ]]; then
			 curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py	
			 python get-pip.py
		 fi
	fi
    fi
fi
