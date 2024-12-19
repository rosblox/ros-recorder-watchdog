#!/bin/bash

REPOSITORY_NAME="$(basename "$(dirname -- "$( readlink -f -- "$0"; )")")"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export HOST_UID=$(id -u)

docker compose -f $SCRIPT_DIR/docker-compose.yml run \
--remove-orphans \
--volume $(pwd)/ros_recorder_watchdog_buzzer:/colcon_ws/src/ros_recorder_watchdog_buzzer \
${REPOSITORY_NAME} bash
