import requests
from bs4 import BeautifulSoup
from collections import Counter
import datetime
import calendar
import pandas as pd
import plotly.express as px

# Constants
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
BASE_URL = "https://www.dav.org/events-calendar/list/"

# Defining your event categories and associated keywords
EVENT_KEYWORDS = {
    'Job Fair': ['job fair', 'career'],
    'Information Seminar': ['seminar', 'workshop', 'conference', 'symposium', 'boot camp'],
    'Testimonial Dinner': ['dinner'],
    'Convention': ['department', 'convention']
    # Add more categories as necessary
}


# Function to categorize event based on keywords
def categorize_event(event_title):
    for category, keywords in EVENT_KEYWORDS.items():
        if any(keyword.lower() in event_title.lower() for keyword in keywords):
            return category
    return 'Other'  # If event title doesn't match any keyword


# Function to process each page and return a list of events
def process_page(url):
    events_data = []
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    events = soup.find_all('article', class_='tribe-events-calendar-list__event')

    for event in events:
        event_title = event.find('h3', class_='tribe-events-calendar-list__event-title').text.strip()
        event_date_str = event.find('time')['datetime']
        event_date = datetime.datetime.fromisoformat(event_date_str)
        events_data.append({
            'title': event_title,
            'category': categorize_event(event_title),
            'date': event_date
        })

    return events_data


# Main function to get event data and plot figures
def get_event_data_and_figures():
    all_events_data = []
    current_url = BASE_URL

    while current_url:
        events_data = process_page(current_url)
        all_events_data.extend(events_data)

        # Find the 'next' page link and update current_url
        response = requests.get(current_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        next_page_link = soup.find('a', class_='tribe-events-c-nav__next')
        current_url = next_page_link['href'] if next_page_link and 'href' in next_page_link.attrs else None

    # Create counters for event types and months
    event_types = Counter([event['category'] for event in all_events_data])
    events_by_month = Counter([event['date'].month for event in all_events_data])

    # Convert month numbers to names for readability
    events_by_month_named = {calendar.month_name[month]: count for month, count in events_by_month.items()}

    # Create plots
    fig_event_types = create_bar_chart(event_types)
    fig_events_by_month = create_pie_chart(events_by_month_named)
    fig_histogram = create_histogram(events_by_month)
    fig_sunburst = create_sunburst(all_events_data)

    return all_events_data, fig_event_types, fig_events_by_month, fig_histogram, fig_sunburst


# Functions to create plots
def create_bar_chart(event_types):
    fig = px.bar(
        color=event_types,
        x=list(event_types.keys()),
        y=list(event_types.values()),
        labels={'x': 'Event Categories', 'y': 'Counts'},
        title='Categorized Event Types Distribution'
    )
    return fig


def create_pie_chart(events_by_month):
    fig = px.pie(
        names=list(events_by_month.keys()),
        values=list(events_by_month.values()),
        title='Proportion of Events by Month'
    )
    return fig

def create_histogram(events_by_month):
    # Convert the events_by_month counter into a list for histogram
    month_labels = [calendar.month_name[month] for month in events_by_month]
    month_values = [events_by_month[month] for month in events_by_month]
    fig = px.histogram(x=month_labels, y=month_values, labels={'x': 'Month', 'y': 'Event Count'}, title='Events by Month', color=month_labels)
    fig.update_traces(marker_line_width=0)  # Remove lines between bars
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},  # Sort by descending order
        bargap=0.05  # Set a small gap between bars
    )
    return fig

# Function to create a sunburst chart
# Function to create a sunburst chart
def create_sunburst(events_data):
    # Convert events_data into the required DataFrame format for sunburst chart
    df = pd.DataFrame(events_data)

    # Aggregate data for sunburst chart
    # We group by both 'date' (more specifically, month) and 'category' and count the occurrences
    sunburst_data = df.groupby([df['date'].dt.strftime('%B'), 'category']).size().reset_index(name='Count')

    # Now create the sunburst chart using the aggregated data
    fig = px.sunburst(
        sunburst_data,
        path=['date', 'category'],
        values='Count',
        title='Events Sunburst by Month and Type'
    )
    return fig

# If you want to test the scraping and plotting directly
#if __name__ == "__main__":
    #event_data, bar_fig, pie_fig, hist_fig, sunburst_fig = get_event_data_and_figures()
    #bar_fig.show()
    #pie_fig.show()
    #hist_fig.show()
    #sunburst_fig.show()
