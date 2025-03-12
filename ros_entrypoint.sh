#!/bin/bash
set -e

id -u ros &>/dev/null || adduser --quiet --disabled-password --gecos '' --uid ${UID:=1000} ros

getent group dialout || groupadd -g 20 dialout
usermod -aG dialout ros

source /opt/ros/${ROS_DISTRO}/setup.bash
source /colcon_ws/install/setup.bash || true

exec "$@"
