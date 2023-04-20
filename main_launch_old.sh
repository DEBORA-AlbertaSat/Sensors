#! /bin/bash

echo "Commencing sensor data acquisition .... "

#Launch each sensor script in the background

python3 ./Sensor_scripts/icm20948_collect.py &

python3 ./Sensor_scripts/bme280_collect.py &

python3 ./Sensor_scripts/gps_collect.py &
wait

#Wait ensures that the script does not stop until all python scripts are finished (never)