```markdown
# ContactInfoScraper

## Overview

ContactInfoScraper is a Python script designed to extract email and phone numbers from given web pages and output the data into an Excel file (contacts.xlsx). It also logs all events and outputs them into a log.txt file.

## Features

- Extracts email and phone numbers from websites.
- Retrieves contact information from social media pages like Facebook.
- Enhanced logging with timestamps for tracking each step of the process.
- Readable output in Command Prompt windows of all sizes.
- User-friendly batch file (OpenCmdHere.bat) for opening the CMD in the correct folder (for Windows).

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
```

## Usage

1. Clone or download the repository.
2. You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

3. Place your target URLs in a text file named `web_urls.txt`, or enter them directly when prompted by the script.
4. Run the Python script to start scraping contact information:

   ```bash
   python contact_info_scraper.py
   ```

   The script will:

- Output information to the Command Prompt with clear formatting.
- Log all activities and errors into a log.txt file.
- Save the contact information into contacts.xlsx.

5. Follow the prompts to enter URLs.
6. After completion, the results will be saved to `contacts.xlsx`.

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

A detailed log of the entire process, including errors and timestamps, is written to log.txt. Timestamps are displayed both in the Command Prompt and in the log file.

## Notes

- If you are using Windows, you can excute the ''OpenCmdHere.bat'' so you can run all the commands fron there.
- Adjust the rate limiting (`time.sleep(1)`) as necessary based on your testing needs and the target website's policies.

## Contributions

Feel free to fork the repository and submit pull requests for any enhancements or bug fixes. Feedback and contributions are welcome!

## License

This project is licensed under the MIT License.
