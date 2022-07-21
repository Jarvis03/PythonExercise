#!/bin/bash

# combine same type files together

if [ $# -gt 2 ]
then
echo "parameter number invalid"
exit -1
fi

if [ $# -eq 2 ]
then
echo "uncompress..."
src_files=$(ls *.$2)
for fil in $src_files
do
	echo -e "\t$fil"
	tar -zxf $fil
	mv usrdata/imu/* .
	rm $fil
done
rm -rf usrdata
fi

obj_files=$(ls *.$1 | grep -v all)
tmp_file=tmp
out_file=all

echo -e "obj_files:"
for fil in $obj_files
do
	echo -e "\t$fil"
done

echo -e "out_file:\n\t$out_file.$1"

if [ -f $out_file.$1 ]
then
	rm $out_file.$1
fi

cat $obj_files > $tmp_file
mv $tmp_file $out_file.$1
