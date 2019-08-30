#!/bin/bash

set -ex

here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

. ${here}/cico_setup.sh

${here}/qa/run-tests.sh

build_image

push_image
