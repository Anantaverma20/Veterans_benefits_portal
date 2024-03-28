from fastapi import FastAPI,  HTTPException
from fastapi.responses import HTMLResponse
import json
from typing import List, Dict
import chardet
from Web_crawling import get_event_data_and_figures
import plotly

app = FastAPI()


with open('title-38.json', 'rb') as file:
    rawdata = file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

with open('title-38.json', 'r', encoding=encoding) as file:
    data = json.load(file)
# Load JSON data
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Your JSON data containing the URLs
part_links_data = load_json_data("part_links.json")

@app.get("/", response_class=HTMLResponse)
def main_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Main Page</title>
        <style>
            body, html {
                height: 100%;
                margin: 0;
                font-family: Arial, sans-serif;
                background: rgba(255, 255, 255, 0.45) url('https://advocacy.sba.gov/wp-content/uploads/2020/11/person-holding-usa-american-flag-on-sunset-background-picture-id1188704306.jpg') no-repeat center center fixed;
                background-size: cover;
                position: relative;
            }
            body::before {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                background: rgba(255, 255, 255, 0.60); 
                z-index: -1;
            }
            nav ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: rgba(51, 51, 51, 0.60); /* 60% transparency */
                position: fixed;
                top: 0;
                width: 100%;
            }
            nav li {
                float: left;
            }
            nav li a {
                display: block;
                color: white;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
                font-family: 'Times New Roman', Times, serif;
            }
            nav li a:hover {
                background-color: #111;
            }
            .content {
                padding-top: 60px; /* Adjusted to push the content down below the fixed navbar */
                text-align: center;
            }
            .content h1 {
                font-family: 'Times New Roman', Times, serif;
                font-size: 48px; /* Increased font size */
                color: white; /* Better visibility against the background */
                text-shadow: 2px 2px 4px #000000; /* Text shadow for better readability */
            }
        </style>
    </head>
    <body>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/benefits-overview">Benefits Overview</a></li>
                <li><a href="/search">Disability Information Search</a></li>
                <li><a href="/search-url">Search CFR Link</a></li>
                <li><a href="/events-report">Insights</a></li>
            </ul>
        </nav>
        <div class="content">
            <h1>Welcome to the Veterans' Disability Benefits Portal</h1>
        </div>
    </body>
    </html>
    """


@app.get("/benefits-overview", response_class=HTMLResponse)
def benefits_overview():
    # Benefits overview content with styled HTML
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Benefits Overview</title>
        <style>
            body {
                font-family: 'Verdana', sans-serif;
                margin: 0;
                padding: 0;
                background: #f0f0f0;
                color: #333;
            }
            .container {
                width: 80%;
                margin: auto;
                background: white;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: justify;
            }
            header {
                background: #004f00;
                color: white;
                padding: 10px 0;
                text-align: center;
            }
            section {
                margin: 20px 0;
            }
            h1 {
                color: white;
                font-weight: bold;
                padding: 10px 0;
            }
            h2 {
                color: #004f00;
                font-weight: bold;
                padding: 10px 0;
            }
            p, li {
                font-size: 16px;
                line-height: 1.6;
                color: #666;
            }
            a {
                color: #004f00;
                text-decoration: underline;
            }
            footer {
                background: #004f00;
                color: white;
                text-align: center;
                padding: 10px 0;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Benefits Overview Page</h1>
        </header>
        <div class="container">
            <section>
                <h2>Summary of VA Benefits</h2>
                <p>The Veterans' Benefits Administration provides a variety of benefits and services to service members, veterans, and their families. These benefits include comprehensive healthcare services, financial assistance, and support through a variety of programs designed to help you lead a better life. Whether you're looking to further your education through the GI Bill, seeking home loan guarantees for purchasing, building, or repairing your home, or exploring disability compensation for service-connected disabilities, our aim is to serve those who have served our country with honor.</p>
                <p>For veterans transitioning back to civilian life, there are employment and career resources available to assist in finding new opportunities and navigating the job market. Understanding that the sacrifices made by veterans and their families are immeasurable, there are also pension programs and dependents' educational assistance for those who qualify. Our commitment is to ensure that you have the resources and support needed to thrive post-service. From navigating the complexities of applying for benefits to accessing healthcare and educational opportunities, we stand ready to help you maximize the benefits you have earned.</p>
            </section>
            <section>
                <h2>Eligibility Requirements</h2>
                <p>Eligibility for veterans' benefits is typically based on service history, discharge status, and the nature of any disability you may have. To qualify for most benefits, you must have served on active duty, active duty for training, or inactive duty training, and received an honorable discharge. However, exceptions often apply for those who have faced hardship or have medical discharges.</p>
                <ol>
                    <li>Healthcare Benefits: To use healthcare services, you need to have served at least 24 continuous months or the full period for which you were called to active duty.</li>
                    <li>Education Benefits: The Post-9/11 GI Bill requires 90 days of aggregate service or 30 continuous days if you were discharged for a service-connected disability.</li>
                    <li>Disability Compensation: This is available if you have a service-related injury or illness, regardless of your time in service.</li>
                    <li>Home Loan Guarantees: Eligibility often requires 90 consecutive days of service during wartime or 181 days during peacetime.</li>
                    <li>Pension Programs: These are for wartime veterans who meet certain age or disability requirements, with an honorable discharge and limited income.</li>
                </ol>
                <p>Some benefits extend to family members, including spouses, children, and sometimes parents. It's important to check the latest guidelines from the U.S. Department of Veterans Affairs, as eligibility criteria can change and additional requirements may apply for specific benefits.</p>
            </section>
            <section>
                <h2>How to Apply</h2>
                <p>Applying for veterans' benefits is a process that can unlock a variety of resources tailored to those who have served in the military. Here’s a streamlined guide to get you started:</p>
                <ol>
                    <li>Gather Documentation: Collect necessary records such as your DD214 or other service documents, medical records, and financial statements. These documents will support your eligibility and claims for benefits.</li>
                    <li>Determine Your Benefit Programs: Review the benefits available and determine which ones apply to your situation. Consider healthcare, disability compensation, education, pension, or home loans, among others.</li>
                    <li>Use Online Resources: The U.S. Department of Veterans Affairs (VA) website is the primary portal for applying. Create an account at the <a href="https://www.va.gov/" target="_blank">VA's online portal</a> to submit applications for benefits such as health care, education benefits, or VA disability compensation.</li>
                    <li>Seek Assistance: If you need help with your application or aren't sure about the process, reach out to a Veterans Service Officer (VSO). These individuals are trained and accredited to assist with navigating the VA system and can provide invaluable help with filling out forms and understanding what's needed for a successful application.</li>
                    <li>Submit Your Application: Depending on the benefit, applications can often be submitted online, through mail, in person at a VA office, or with the help of a VSO. Ensure you keep copies of all submissions for your records.</li>
                    <li>Await Confirmation: After submitting your application, you will receive confirmation from the VA. The time frame for processing can vary, so be prepared to wait, but you can usually check the status of your application online.</li>
                    <li>Follow Up: If you receive a request for additional information or documentation, respond as quickly as possible. Keep a record of all correspondence and always ask for clarification if you receive a decision that is not clear.</li>
                </ol>
                <p>Remember, each benefit may have its specific application procedure, so it is crucial to follow the instructions provided for each individual benefit program.</p>
            </section>
            <section>
                <h2>Resources and Support</h2>
                <p>Navigating the array of veterans' benefits can be challenging, but a wealth of resources and support networks are available to assist you through every step:</p>
                <ol>
                    <li>VA Facilities Locator: Find facilities near you for healthcare, benefits assistance, and more, by using the <a href="https://www.va.gov/find-locations/" target="_blank">VA Locator tool</a>.</li>
                    <li>VA Benefits Hotline: For immediate assistance or to ask questions about your benefits, call the VA hotline at 1-800-827-1000.</li>
                    <li>Veterans Service Organizations (VSOs): VSOs can provide personalized help with applying for benefits, understanding eligibility, and appealing decisions. Organizations like the <a href="https://www.legion.org/" target="_blank">American Legion</a>, <a href="https://www.vfw.org/" target="_blank">VFW</a>, and <a href="https://www.dav.org/" target="_blank">Disabled American Veterans</a> have representatives nationwide.</li>
                    <li>VA Caregiver Support: If you’re a caregiver for a veteran, you can find resources and support programs through the <a href="https://www.caregiver.va.gov/" target="_blank">VA Caregiver Support Program</a>.</li>
                    <li>Mental Health Resources: Confidential support is available 24/7 for veterans and their families by contacting the <a href="https://www.veteranscrisisline.net/" target="_blank">Veterans Crisis Line</a> at 1-800-273-8255 and pressing 1, texting to 838255, or via the website.</li>
                    <li>Educational and Career Counseling: Services such as career counseling and educational advice are accessible through the VA's <a href="https://www.benefits.va.gov/vocrehab/" target="_blank">Vocational Rehabilitation and Employment (VR&E)</a> services.</li>
                    <li>National Resource Directory: Connect to a network of national, state, and local services through the <a href="https://nrd.gov/" target="_blank">National Resource Directory</a>, including resources for homelessness, substance abuse, and more.</li>
                </ol>
                <p>Ensure you reach out to these resources for support and guidance as you explore and utilize the benefits you have earned through your service.</p>
            </section>
        </div>
        <footer>
            <p>&copy; Veterans' Disability Benefits Portal</p>
        </footer>
    </body>
    </html>
    """


# This endpoint will serve the main HTML page and include JavaScript for the search functionality
@app.get("/search-url", response_class=HTMLResponse)
async def search_url():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Disability Information Search</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                background-color: white; /* This is a placeholder white */
                color: #004f00;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            .search-container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            .search-box {
                padding: 12px 20px;
                
                margin-bottom: 20px; /* Space between input and button */
            }
            .search-button {
                padding: 14px 20px;
                margin: 8px 0;
                font-size: 1em;
                background-color: #006400; 
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 4px;
            }
            .search-button:hover {
                background-color: #004f00; /* Slightly darker grey on hover */
            }
            h1 {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Professional-looking font */
                font-size: 2.5em;
            }
            input[type=text] {
                width: 50%;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
                border: 2px solid #004f00;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="search-container">
            <h1>Disability Information Search</h1>
            <input type="text" class="search-box" id="disability" placeholder="Enter a disability" autofocus>
            <button class="search-button" onclick="searchDisability()">Search</button>
        </div>
        <div id="results"></div>

        <script>
            async function searchDisability() {
                var disability = document.getElementById('disability').value;
                if (disability) {
                    const response = await fetch('/get-urls/?disability=' + encodeURIComponent(disability));
                    const items = await response.json();
                    const resultsDiv = document.getElementById('results');
                    resultsDiv.innerHTML = ''; // Clear previous results
                    items.forEach(item => {
                        resultsDiv.innerHTML += `<p><strong>${item.title}</strong>: <a href="${item.url}" target="_blank" style="color: #ADD8E6">${item.url}</a></p>`;
                    });
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# This endpoint will be called by JavaScript from the frontend
@app.get("/get-urls/", response_model=List[Dict[str, str]])
async def get_urls(disability: str):
    # Find titles and URLs matching the disability keyword
    matched_items = [{"title": title, "url": url} for title, url in part_links_data.items() if disability.lower() in title.lower()]

    # Return only the first three results
    return matched_items[:3]


@app.get("/search", response_class=HTMLResponse)
def search_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Disability Information Search</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: white;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            h1 {
                color: #004f00; /* A color that represents the veterans */
                font-size: 2.5em;
            }
            input[type=text] {
                width: 50%;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
                border: 2px solid #004f00;
                border-radius: 4px;
            }
            button {
                background-color: #006400; /* Dark green color */
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 1em;
            }
            button:hover {
                background-color: #004f00;
            }
        </style>
    </head>
    <body>
        <h1>Disability Information Search</h1>
        <input type="text" id="disability" placeholder="Enter a disability" autofocus>
        <button onclick="searchDisability()">Search</button>
        <div id="results"></div>

        <script>
            async function searchDisability() {
                var disability = document.getElementById('disability').value;
                if(disability) {
                    const response = await fetch('/search_disability/?disability=' + encodeURIComponent(disability));
                    const data = await response.json();
                    const results = document.getElementById('results');
                    results.innerHTML = ''; // Clear previous results
                    if(data.detail) {
                        results.innerHTML = '<p>' + data.detail + '</p>';
                    } else {
                        data.forEach(d => {
                            results.innerHTML += '<p>' + d.label + ' - ' + (d.label_description || 'No description available') + '</p>';
                        });
                    }
                }
            }
        </script>
    </body>
    </html>
    """

def find_disability_info(data, disability_keyword, collected_info=None):
    if collected_info is None:
        collected_info = []

    # Search the label description for the keyword
    description = data.get('label_description', '').lower()
    if disability_keyword.lower() in description:
        collected_info.append(data)
        if len(collected_info) >= 3:  # Stop if we have 3 matches
            return collected_info

    # Recurse through children if we haven't found 3 matches yet
    if len(collected_info) < 3:
        for child in data.get('children', []):
            find_disability_info(child, disability_keyword, collected_info)
            if len(collected_info) >= 3:  # Stop if we have 3 matches
                break

    return collected_info


@app.get("/search_disability/", response_model=List[Dict])
def search_disability_endpoint(disability: str):
    disability_info = find_disability_info(data, disability)
    if not disability_info:
        raise HTTPException(status_code=404, detail="Disability information not found")
    return disability_info[:3]  # Return only the first three results


@app.get("/events-report", response_class=HTMLResponse)
async def events_report():
    # Get data and figures from web_crawling.py
    event_data, bar_fig, pie_fig, hist_fig, sunburst_fig = get_event_data_and_figures()

    # Convert the plotly figures to JSON for rendering in the HTML
    bar_fig_json = json.dumps(bar_fig, cls=plotly.utils.PlotlyJSONEncoder)
    pie_fig_json = json.dumps(pie_fig, cls=plotly.utils.PlotlyJSONEncoder)
    hist_fig_json = json.dumps(hist_fig, cls=plotly.utils.PlotlyJSONEncoder)
    sunburst_fig_json = json.dumps(sunburst_fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Assuming 'events' is a list of dictionaries where each dictionary has event details
    events_html_list = '\n'.join([f"<li>{event['title']} - {event['date'].strftime('%B %d, %Y')}</li>" for event in event_data])

    # Create the HTML content with dynamic data
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Events Report</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            h1, h2, h3 {{
                font-size: 2em; /* This sets the size of h1, h2, and h3 to be the same */
            }}
            .Recommendations {{
                font-size: 1.5em; /* This sets the size of the recommendations class */
            }}
        </style>
    </head>
    <body>
        <h1>Events from DAV Website</h1>
        <ul>
            {events_html_list}
        </ul>
        <hr>
        <h2>Plots</h2>
        <div id="bar-plot"></div>
        <div id="pie-plot"></div>
        <div id="hist-plot"></div>
        <div id="sunburst-plot"></div>
        <hr>
        <h3>Recommendations</h3>
        <div class="recommendations">
            <ul>
                <li>Seasonal Trends: The histogram indicates there are peak months (June for the year 2024 with a total of 34 events) where more events are hosted. For veterans planning their schedules or organizations aiming to reach out to this community, it’s recommended to focus on these peak months to engage with the maximum number of participants or attendees.</li>
                <li>Event Types: The bar chart shows that certain event types, like 'Job Fairs', are much more common than others. This could suggest a strong focus or need for career transition services within the veteran community. Job seekers should prioritize these months and organizations might consider hosting more events of the less frequent types to diversify the support to veterans.</li>
                <li>Engagement Opportunities: The pie chart indicates the distribution of events throughout the year. Organizers can use this information to identify less busy months where new events might stand out more and capture greater attention due to less competition.</li>
                <li>Holistic Overview: The Events Sunburst provides a detailed breakdown of events by type across different months. It helps in identifying not only when events are happening but also what kinds of events. This can aid veterans in finding events that cater to their specific interests and needs throughout the year.</li>
            </ul>
            <p>These insights can guide both veterans and service providers in planning and optimizing their engagement with events tailored to the veteran community.</p>
        </div>      
        <script>
            var barFig = {bar_fig_json};
            var pieFig = {pie_fig_json};
            var histFig = {hist_fig_json};
            var sunburstFig = {sunburst_fig_json};

            Plotly.newPlot('bar-plot', barFig.data, barFig.layout);
            Plotly.newPlot('pie-plot', pieFig.data, pieFig.layout);
            Plotly.newPlot('hist-plot', histFig.data, histFig.layout);
            Plotly.newPlot('sunburst-plot', sunburstFig.data, sunburstFig.layout);
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)
