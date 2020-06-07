#!/bin/bash
src="/fso-weather-data"
dest="/home/pi/fso-weather-data"
#year=$(date "+%Y")
#day=$(date "+%Y-%m-%d")

if [ $# -ne 1 ];then
  echo "usage: ./savefile.sh date(xxxx-xx-xx)"
  echo "example: ./savefile.sh 2019-09-30"
  exit 0
fi

day=$1
year=`echo $day|cut -d '-' -f 1`

if [ ! -d $src/$year ]; then
  mkdir -p -m 777 $src/$year
fi
if [ ! -f $src/$year/fso-weather-$day.csv ];then
  echo "source file: $src/$year/fso-weather-$day.csv is not exist!"
  exit 1
fi

if [ ! -d $dest/$year ]; then
  mkdir -p -m 777 $dest/$year
fi
if [ ! -f $dest/$year/fso-weather-$day.csv ];then
  touch $dest/$year/fso-weather-$day.csv
fi
sudo comm -23 $src/$year/fso-weather-$day.csv $dest/$year/fso-weather-$day.csv >>  $dest/$year/fso-weather-$day.csv

#sudo cp -f /fso-weather-data/$year/fso-weather-$(date "+%Y-%m-%d").csv /home/pi/fso-weather-data/$year/
