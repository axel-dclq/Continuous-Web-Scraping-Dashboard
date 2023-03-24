#!/bin/bash

url="https://countrymeters.info/en/World"
html=$(curl -s "$url")

population=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp1">)[^<]+')
label=$(echo "$html" | grep -Po '(?<=<td class="data_name"><b>)[^<]+')

echo "La ${label,,} est de ${population} personnes."
