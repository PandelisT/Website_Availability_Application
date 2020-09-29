def instructions():
    print("""
This is a Python 3 based OOP terminal application which tests the availability of your website and performs a health check which is sent to your email address through the SendGrid API. The program also includes automated tests and a CI/CD pipeline using GitHib actions.
The repository for this application can be found here: https://github.com/PandelisT/Website_Availability_Application.git.

Set up your Python virtual environment:
pip install -r requirements.txt

Export your API keys for all APIs:
export API_KEY=<API_KEY>

Run:
python3.8 main.py

There are three different APIs used in this program.

1) [Google PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started). Please create an [API key](https://console.developers.google.com/apis/credentials).
The PageSpeed Insights API used to make GET requests and receive responses for the page performance and other key metrics such as First Meaningful Paint, Speed Index and Time to interactive. All of these gives the user information about the speed and performance of the webpage.
2) [Auth0 Signals API](https://auth0.com/signals/docs/). Sign up to create an [API key](https://auth0.com/signup).
The Auth0 Signals API is used to check if an IP address is blacklisted. The range of responses from the GET request is approximately -4 to 0, with 0 being the highest confidence.
3) [SendGrid API](https://sendgrid.com/docs/API_Reference/api_v3.html). Create an account and go to the [API key settings](https://app.sendgrid.com/settings/api_keys).
The SendGrid API is used to make a POST request to send an email report to the user about the health check performance.  
""")
