#!/bin/sh
# David D. Dalton

_green=$(tput setaf 76)
_reset=$(tput sgr0)
_purple=$(tput setaf 171)
_red=$(tput setaf 1)
_tan=$(tput setaf 3)
_blue=$(tput setaf 38)
_bold=$(tput bold)
_underline=$(tput sgr 0 1)

function _success()
{
    printf "${_green} %s${_reset}\n" "$@"
}

function _bolded()
{
    printf "${_bold} %s${_reset}\n" "$@"
}

function _start()
{
	printf "${_blue} %s${_reset}\n" "$@"
}

function _warning()
{
    printf "${_red}! %s${_reset}\n" "$@"
}


function main()
{
	_start "Applying Stored Procedures"
	cd ~/Ambilight/db/sp/
	for file in *.sql; do
	  _bolded $file
	  mysql -uapp -ptabard5]deathblows -hlocalhost Sensor < $file
	done
	cd 
	_success "Finished Applying Stored Procedures"
}

main