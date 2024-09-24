````markdown
# ContactInfoScraper

## Description

**ContactInfoScraper** is a Python script designed to extract contact information, including emails and phone numbers, from specified web pages and their associated social media profiles. The script utilizes web scraping techniques to gather data from various sources, helping users easily compile contact details for businesses or organizations.

## Features

- Fetches emails and phone numbers from the main webpage and linked contact pages.
- Extracts information from social media platforms such as Facebook, Google Maps, and Yelp.
- Conducts Google searches to find additional contact information.
- Removes duplicate entries for a cleaner output.
- Outputs the collected data into a well-formatted Excel spreadsheet.

## How It Works

1. **Setup and Configuration**: The script initializes logging for monitoring its activity, and sets up necessary imports for web scraping and data handling.

2. **Data Collection**:

   - **URL Input**: Users can input multiple URLs directly, which will be validated before processing.
   - **Contact Information Gathering**: For each URL, the script fetches the main webpage, extracts emails and phone numbers, and searches for additional contact links.
   - **Social Media and Google Search**: If phone numbers are not found, it checks the associated Facebook page and uses Google Maps and Yelp for further data extraction.

3. **Output**:
   - The collected contact information is saved into a CSV file and formatted into an Excel file with appropriate styling for easy readability.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `BeautifulSoup4`
  - `lxml`
  - `re`
  - `csv`
  - `json`
  - `openpyxl`
  - `googlesearch-python`
  - `tld`

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4 lxml openpyxl googlesearch-python tld
```
````

## Usage

1. Clone or download the repository.
2. Place your target URLs in a text file named `web_urls.txt`, or enter them directly when prompted by the script.
3. Run the script:

   ```bash
   python contact_info_scraper.py
   ```

4. Follow the prompts to enter URLs.
5. After completion, the results will be saved to `contacts.xlsx`.

## Example of URL Input

```
Enter the webpage URL (or type "n" to finish): https://example.com
```

## Sample Output

The script will display the contact information in the terminal:

```
Contact Info:
Website: https://example.com
Emails: contact@example.com
Phones: +1-234-567-8901
```

The output will also be saved in `contacts.xlsx` with columns for Website, Email, and Phone.

## Logging

The script logs its activities, which can help in debugging or tracking its progress. The logs are printed in the console and can be found in a log file if configured.

## Notes

- Ensure that the target websites allow web scraping as per their `robots.txt` file to avoid legal issues.
- Adjust the rate limiting (`time.sleep(1)`) as necessary based on your testing needs and the target website's policies.

## Contributions

Feel free to fork the repository and submit pull requests for any enhancements or bug fixes. Feedback and contributions are welcome!

## License

This project is licensed under the MIT License.

```

```
