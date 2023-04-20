#! /bin/bash

echo "Displaying most recent data values from each sensor output file... "

echo "GPS:  $(tail -1 ~/DEBORA/Sensors/Data/gps_data/test_data.csv)"
echo "Temp: $(tail -1 ~/DEBORA/Sensors/Data/bme280_data/test_data.csv)"
echo "Acel: $(tail -1 ~/DEBORA/Sensors/Data/icm20948_data/test_data.csv)"

# find all files, then get their human readable size
find ~/DEBORA/Sensors/Data -type f -exec du -h {} +