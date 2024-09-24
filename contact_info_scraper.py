import logging
from tld import get_tld
import requests
import re
import csv
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from googlesearch import search
import openpyxl
from openpyxl.styles import Font, PatternFill

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to remove duplicates
def remove_duplicates(data):
    return list(set(data))

def get_email(html):
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return set(re.findall(email_pattern, html))

def get_phone(html):
    phone_patterns = [
        r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        r"\d{2,3}[-.\s]?\d{3}[-.\s]?\d{4}",
        r"((?:\d{2,3}|\(\d{2,3}\))?(?:\s|-|\.)?\d{3,4}(?:\s|-|\.)?\d{4})",
        r"\d{4}[-.\s]?\d{3}[-.\s]?\d{3}",
        r"(\+\d{1,3}[- ]?)?\(?\d{1,4}?\)?[- ]?\d{1,4}[- ]?\d{1,4}[- ]?\d{1,4}",
    ]
    return set(num for pattern in phone_patterns for num in re.findall(pattern, html))

def log_no_results(info_type, source):
    logging.info(f"No {info_type} found on {source}.")
    print(f'No {info_type} found on {source}.')  # Print for CMD

def fetch_data_with_error_handling(url, headers):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()  # Raise an error for bad responses
        return res
    except requests.exceptions.RequestException as e:
        logging.warning("Error accessing URL: %s, Error: %s", url, e)
        return None

def find_contact_links(soup):
    return [a['href'] for a in soup.find_all('a', string=re.compile('contact', re.IGNORECASE)) if 'href' in a.attrs]

def extract_facebook_url(soup):
    fb_links = [a['href'] for a in soup.find_all('a', href=re.compile('facebook.com', re.IGNORECASE)) if 'href' in a.attrs]
    return fb_links[0] if fb_links else None

def search_google(company_name):
    query = f"{company_name} phone number"
    return list(search(query, num=5, stop=5, pause=2))

def get_phone_from_social_media(url):
    res = fetch_data_with_error_handling(url, headers={'User-Agent': 'Mozilla/5.0'})
    if res:
        return get_phone(BeautifulSoup(res.text, 'lxml').get_text())
    return []

def gather_contact_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = fetch_data_with_error_handling(url, headers)

    if res:
        logging.info('Searched home URL: %s', res.url)
        print(f'Searched home URL: {res.url}')  # Print for CMD
        info = BeautifulSoup(res.text, 'lxml')
        company_name = info.title.string if info.title else "Unknown Company"

        contacts_f = {
            'Website': res.url,
            'Email': remove_duplicates(list(get_email(info.get_text()))),
            'Phone': remove_duplicates(list(get_phone(info.get_text())))
        }

        # Extract contact links and Facebook URL
        contact_links = find_contact_links(info)
        facebook_url = extract_facebook_url(info)

        # Gather contact info from links
        for contact_link in contact_links:
            contact_url = contact_link if 'http' in contact_link else urlparse(res.url)._replace(path='/'.join(res.url.split('/')[:-1]) + '/' + contact_link).geturl()
            contact_res = fetch_data_with_error_handling(contact_url, headers)
            if contact_res:
                logging.info('Searched contact URL: %s', contact_res.url)
                print(f'Searched contact URL: {contact_res.url}')  # Print for CMD
                contact_info = BeautifulSoup(contact_res.text, 'lxml').get_text()
                contacts_f['Email'].extend(get_email(contact_info))
                contacts_f['Phone'].extend(get_phone(contact_info))

        # Check social media for phone numbers
        if not contacts_f['Phone']:
            if facebook_url:
                fb_phones = get_phone_from_social_media(facebook_url)
                contacts_f['Phone'].extend(fb_phones)
                if not fb_phones:
                    log_no_results('phone numbers', 'Facebook')

        # Check Google Maps
        if not contacts_f['Phone']:
            maps_phones = get_phone_from_social_media(f"{company_name} site:maps.google.com")
            contacts_f['Phone'].extend(maps_phones)
            if not maps_phones:
                log_no_results('phone numbers', 'Google Maps')

        # Check Yelp
        if not contacts_f['Phone']:
            yelp_phones = get_phone_from_social_media(f"{company_name} site:yelp.com")
            contacts_f['Phone'].extend(yelp_phones)
            if not yelp_phones:
                log_no_results('phone numbers', 'Yelp')

        # Check Google
        if not contacts_f['Phone']:
            google_results = search_google(company_name)
            for result in google_results:
                google_res = fetch_data_with_error_handling(result, headers)
                if google_res:
                    google_emails = get_email(google_res.text)
                    google_phones = get_phone(google_res.text)
                    contacts_f['Email'].extend(google_emails)
                    contacts_f['Phone'].extend(google_phones)

                    if contacts_f['Phone']:  # If phone number is found, break the loop
                        break
                else:
                    log_no_results('phone numbers', 'Google')

        contacts_f['Email'] = remove_duplicates(contacts_f['Email'])
        contacts_f['Phone'] = remove_duplicates(contacts_f['Phone'])

        return contacts_f
    return None

# Initialize search list
with open("web_urls.txt", "w") as file:  # Clear existing data
    pass

# Input URLs directly with validation
urls = []
while True:
    url = input('Enter the webpage URL (or type "n" to finish): ')
    if url.lower() == 'n':
        logging.info('Thank you...')
        break

    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'https://' + url

    # Basic URL validation
    if not re.match(r'https?://[^\s/$.?#].[^\s]*', url):
        print("Invalid URL. Please enter a valid URL.")
        logging.warning("Invalid URL entered: %s", url)
        continue

    urls.append(url)
    with open("web_urls.txt", "a") as file:
        file.write(url + '\n')

# Looping over the URLs with rate limiting
contacts = []
for url in urls:
    contact_info = gather_contact_info(url)
    if contact_info:
        contacts.append(contact_info)
        logging.info('Contact Info: %s', json.dumps(contact_info, indent=2))

        # Enhanced print output
        print(f'Contact Info:\n'
              f'Website: {contact_info["Website"]}\n'
              f'Emails: {", ".join(contact_info["Email"]) if contact_info["Email"] else "None"}\n'
              f'Phones: {", ".join(contact_info["Phone"]) if contact_info["Phone"] else "None"}\n')
    
    time.sleep(1)  # Rate limit

# Saving the results
def save_to_excel(contacts):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contacts"

    headers = ['Website', 'Email', 'Phone']
    ws.append(headers)

    for contact in contacts:
        ws.append([contact['Website'], ", ".join(contact['Email']), ", ".join(contact['Phone'])])

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
        for cell in col:
            cell.font = Font(name='Arial', size=12)
            cell.fill = PatternFill(start_color="FFFFFF00", end_color="FFFFFF00", fill_type="solid")

    wb.save("contacts.xlsx")

# Call the function to save the contacts to Excel
save_to_excel(contacts)
print("Results saved to contacts.xlsx")
