import requests
from prometheus_client import start_http_server, Gauge
import logging
import time

logging.basicConfig(level=logging.INFO)

# Define the metric you want to expose
MAILHOG_EMAIL_COUNT = Gauge(
    'mailhog_email_count', 'Number of emails received by MailHog', ['to_address'])

# MailHog API URL
MAILHOG_API_URL = 'http://mailhog:8025/api/v2'


def scrape_mailhog():
    """Scrape MailHog's API and expose the metrics."""
    try:
        # Fetch email data from MailHog API
        response = requests.get(f"{MAILHOG_API_URL}/messages")
        response.raise_for_status()
        messages = response.json()

        # Clear existing metrics
        MAILHOG_EMAIL_COUNT.clear()

        # Count emails for each recipient
        email_count = {}
        logging.info(messages)
        for message in messages['items']:
            for recipient in message['To']:
                # Ensure 'recipient' is the email address (Access 'Address' key inside the dictionary)
                if isinstance(recipient, dict) and 'Address' in recipient:
                    email_address = recipient['Address']
                    email_count[email_address] = email_count.get(email_address, 0) + 1

        # Update Prometheus metrics
        for recipient, count in email_count.items():
            MAILHOG_EMAIL_COUNT.labels(to_address=recipient).set(count)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping MailHog API: {e}")


def main():
    """Start the HTTP server and periodically scrape MailHog."""
    # Start the Prometheus HTTP server
    start_http_server(9114)

    # Scrape MailHog every 60 seconds
    while True:
        scrape_mailhog()
        time.sleep(60)  # Sleep for 60 seconds before scraping again


if __name__ == '__main__':
    main()
