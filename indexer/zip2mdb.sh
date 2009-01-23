#i!/bin/bash
for i in $(ls *zip | awk -F "." '{print $1}'); do mkdir $i; unzip $i.zip -d $i; done

