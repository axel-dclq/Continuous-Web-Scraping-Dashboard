#!/bin/bash

url="https://countrymeters.info/en/World"
html=$(curl -s "$url")

datetime=$(date +"%Y-%m-%d %H:%M:%S")
world_population=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp1">)[^<]+')
male_population=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp2">)[^<]+')
female_population=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp3">)[^<]+')
birth_year_to_date=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp6">)[^<]+')
birth_today=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp7">)[^<]+')
deaths_year_to_date=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp8">)[^<]+')
deaths_today=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp9">)[^<]+')
population_growth_year_to_date=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp12">)[^<]+')
population_growth_today=$(echo "$html" | grep -Po '(?<=<td class="counter"><div id="cp13">)[^<]+')


echo "$datetime;$world_population;$male_population;$female_population;$birth_year_to_date;$birth_today;$deaths_year_to_date;$deaths_today;$population_growth_year_to_date;$population_growth_today"
