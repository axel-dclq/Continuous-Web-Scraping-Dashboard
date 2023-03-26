# **Continuous Web Scraping Dashboard**
This project is designed to provide up-to-date information from continuous scraping of a website and display it on an online dashboard. The dashboard is built using Python and the Dash package.

### **Requirements**
- Bash
- Python 3.9.7
- Dash
- Plotly
- Cron

### **Getting Started**
Find a website with dynamic information that changes regularly. We recommend using a website with a stable HTML structure, such as https://countrymeters.info/en/World.
<br>Use Bash to retrieve the specific information you want to display and save it to a CSV file.
<br>Use Python and the Dash package to create a dashboard that displays the information in an easy-to-read format.
<br>Include a graph that displays the time series of the data you've scraped.
<br>Use cron to update the dashboard every 5 minutes.
<br>Include a daily report that's updated at 8 pm each day. This report should contain several metrics that provide insight into the data you've scraped.
<br>Additional features are welcome if they add value to the dashboard.

### **Usage**
Clone this repository.
<br>Set up a cron job to run the get_informations.sh script at the desired interval.
<br>Run the main.py file to start the dashboard.
<br>View the dashboard in a web browser by navigating to http://13.50.232.166:8050/.

### **Note about application stability and data sourcing**
Please note that due to the use of multiple callbacks, the application may experience occasional bugs or slow response times. I am continually working to optimize the performance of the application, but please be patient if you experience any issues.

Additionally, I would like to note that the decision to scrape population data every 5 minutes may not be the most efficient way to highlight the data. I am constantly evaluating different methods for data sourcing and will adjust our approach as necessary to improve the accuracy and stability of the application.

Thank you for your understanding and please feel free to reach out to me with any feedback or questions.

