# IndeedScraper

IndeedScraper is a Python script that utilizes the Selenium and BeautifulSoup libraries to scrape job postings data from the Indeed website. It allows you to gather job information based on a specified job title and location, storing the data in a Pandas dataframe and saving it to a CSV file for further analysis.

## Features

- Scrapes job postings from Indeed based on job title and location.
- Extracts job title, company name and link, location, and job description.
- Stores data in a Pandas dataframe.
- Saves data to a CSV file for easy analysis and processing.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/stratiiv/IndeedScraper.git
```
2. Install the required dependencies using Pipenv:
```bash
pipenv install
```
3. Activate the virtual environment:
```bash
pipenv shell
```
4. Run the script:
```bash
python main.py
```
5. Follow the prompts to enter the job title and location for scraping.
6. The scraped data will be stored in a Pandas dataframe and saved to a CSV file named data/jobs.csv
## Notes
* The script performs scrolling to load all job postings on Indeed.
* It handles pop-ups for Google login and cookies alerts.
* The chromedriver executable is required to run the Selenium automation. Make sure it's in your system's PATH or update the main.py script with the correct path.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

IndeedScraper is open source and released under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for more details.

