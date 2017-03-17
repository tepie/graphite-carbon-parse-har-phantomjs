#!/bin/bash
while true
do
	cat url.txt | xargs -I "@" phantomjs ../phantomjs/examples/netsniff.js "@" > initPayment.har 
	python har_parse_total_size.py initPayment.har
	sleep 300
done
