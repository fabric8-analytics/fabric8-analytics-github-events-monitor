#!/bin/bash

set -ex

prep() {
    yum -y update
    yum -y install epel-release https://centos7.iuscommunity.org/ius-release.rpm
    yum -y install python36 which
}

check_python_version() {
    python3 tools/check_python_version.py 3 6
}

prep
check_python_version
./qa/check-docstyle.sh
