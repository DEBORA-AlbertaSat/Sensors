#! /bin/bash
echo ""

echo "Displaying most recent data values from each sensor output file... "

echo ""

echo "GPS:  $(tail -1 /home/albertasat/DEBORA/Sensors/Data/gps_data/gps_data.csv)"
echo "Temp: $(tail -1 /home/albertasat/DEBORA/Sensors/Data/bme280_data/bme_data.csv)"
echo "Acel: $(tail -1 /home/albertasat/DEBORA/Sensors/Data/icm20948_data/icm_data.csv)"

echo ""

# find all files, then get their human readable size
find /home/albertasat/DEBORA/Sensors/Data -type f -exec du -h {} +