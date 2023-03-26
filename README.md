# **Continuous Web Scraping Dashboard**
This project is designed to provide up-to-date information from continuous scraping of a website and display it on an online dashboard. The dashboard is built using Python and the Dash package.

### **Requirements**
Bash
Python 3.x
Dash
Cron


### **Getting Started**
Find a website with dynamic information that changes regularly. We recommend using a website with a stable HTML structure, such as https://countrymeters.info/en/World.
Use Bash to retrieve the specific information you want to display and save it to a CSV file.
Use Python and the Dash package to create a dashboard that displays the information in an easy-to-read format.
Include a graph that displays the time series of the data you've scraped.
Use cron to update the dashboard every 5 minutes.
Include a daily report that's updated at 8 pm each day. This report should contain several metrics that provide insight into the data you've scraped.
Additional features are welcome if they add value to the dashboard.

### **Usage**
Clone this repository.
Set up a cron job to run the scrape.sh script at the desired interval.
Run the app.py file to start the dashboard.
View the dashboard in a web browser by navigating to http://localhost:8050.

### **License**
This project is licensed under the MIT License - see the LICENSE file for details.