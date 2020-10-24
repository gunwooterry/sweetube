#!/usr/bin/env bash

WORKDIR=$(cd `dirname ${BASH_SOURCE[0]}`; pwd)
poetry run python -W ignore -m sweetube.cli.cli "${WORKDIR}/sweetube/cli/cli.py" "$1"
