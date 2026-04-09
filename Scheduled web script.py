import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from datetime import datetime
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import schedule
import time


def scrape_data():
    def get_headlines():
        url = "https://www.ft.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines_element = soup.find_all("div", class_="headline")

        headlines = []
        for element in headlines_element:
            headline = element.text.strip()
            headlines.append(headline)

        # Create a DataFrame with date and headline columns
        df = pd.DataFrame({"Date": [date.today()] * len(headlines), "Headline": headlines})
        return df

    # Update headlines daily and store in a DataFrame
    df_headlines = get_headlines()

    # Append the new headlines to an existing DataFrame (if available)
    try:
        existing_df = pd.read_csv("FT_headlines.csv")
        df_headlines = pd.concat([existing_df, df_headlines], ignore_index=True)
    except FileNotFoundError:
        pass

    # Save the DataFrame to a CSV file
    df_headlines.to_csv("FT_headlines.csv", index=False)

    def get_tech_headlines():
        url = "https://www.ft.com/technology-sector"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        headlines_element = soup.find_all('a', class_='js-teaser-heading-link')

        headlines = []
        for element in headlines_element:
            headline = element.text.strip()
            headlines.append(headline)

        # Create a DataFrame with date and headline columns
        df = pd.DataFrame({"Date": [date.today()] * len(headlines), "Headline": headlines})
        return df

    df_tech_headlines = get_tech_headlines()

    # Append the new headlines to an existing DataFrame (if available)
    try:
        existing_df = pd.read_csv("FT_tech_headlines.csv")
        df_tech_headlines = pd.concat([existing_df, df_tech_headlines], ignore_index=True)
    except FileNotFoundError:
        pass
    # Save the DataFrame to a CSV file
    df_tech_headlines.to_csv("FT_tech_headlines.csv", index=False)


schedule.every().day.at("22:00").do(scrape_data)

while True:
    schedule.run_pending()
    time.sleep(1)
