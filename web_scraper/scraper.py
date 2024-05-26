import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Scrape the data from Panorama website
def scrape_panorama_news():
    url = 'https://www.panorama.com.al'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    headlines = []
    dates = []
    
    # Articles are within 'div' elements with class 'td-block-span6'
    for item in soup.find_all('div', class_='td-block-span6'):
        headline = item.find('h3', class_='entry-title')
        if headline:
            headlines.append(headline.get_text(strip=True))
        
        date = item.find('time', class_='entry-date')
        if date:
            dates.append(date.get('datetime'))
        else:
            dates.append('No Date')
    
    return headlines, dates

# Step 2: Clean and preprocess the data
def preprocess_data(headlines, dates):
    data = pd.DataFrame({
        'headline': headlines,
        'date': dates
    })
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.dropna(subset=['date'], inplace=True)
    return data

# Step 3: Generate visual reports
def generate_visual_reports(data):
    if data.empty:
        print("No data to plot.")
        return
    
    # Group by date and count the number of headlines per date
    data['date_only'] = data['date'].dt.date
    article_counts = data.groupby('date_only').size()
    
    if article_counts.empty:
        print("No articles to plot.")
        return
    
    # Plot the number of articles per day
    plt.figure(figsize=(10, 6))
    article_counts.plot(kind='bar')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.title('Number of Articles Published per Day on Panorama')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    headlines, dates = scrape_panorama_news()
    if not headlines or not dates:
        print("Failed to scrape any data.")
        return
    data = preprocess_data(headlines, dates)
    generate_visual_reports(data)

if __name__ == "__main__":
    main()
