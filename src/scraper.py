import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, date
import pytz
from typing import Dict, Optional, Tuple, List, Any
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class LotteryScraper:
    """Scraper for Georgia Lottery Cash 4 numbers."""
    
    BASE_URL = "https://www.galottery.com/en-us/games/draw-games/cash-four.html#tab-winningNumbers"
    DRAWING_TIMES = {
        "midday": "12:29 PM",
        "evening": "6:59 PM",
        "night": "11:34 PM"
    }
    DATA_FILE = "data/winning_numbers.json"
    
    def __init__(self):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        
    def _get_rendered_html(self) -> str:
        """Use Selenium with a headless Chrome browser to fetch the rendered HTML."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(self.BASE_URL)
            time.sleep(5)  # Wait for JavaScript to load
            return driver.page_source
        finally:
            driver.quit()
            
    def _load_stored_numbers(self) -> Optional[Dict[str, Tuple[str, str]]]:
        """Load winning numbers from the data file."""
        try:
            if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, 'r') as f:
                    data = json.load(f)
                    # Check if the data is from today
                    # Note: Program runs after midnight, so we're checking previous day's results
                    if data.get('date') == date.today().isoformat():
                        return data.get('numbers', {})
        except Exception:
            pass
        return None
            
    def _save_numbers(self, numbers: Dict[str, Tuple[str, str]]):
        """Save winning numbers to the data file."""
        try:
            data = {
                'date': date.today().isoformat(),  # Today's date (when program runs)
                'numbers': numbers  # Previous day's results
            }
            with open(self.DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
            
    def get_winning_numbers(self) -> Dict[str, Tuple[str, str]]:
        """
        Fetch winning numbers for all drawings by scraping the website table using Selenium.
        Returns a dictionary with drawing type as key and tuple of (numbers, date) as value.
        Only returns the latest result for each drawing type.
        
        Note: This program is designed to run after midnight (12 AM) to check the previous day's results.
        For example, if run on 2025-06-17, it will fetch results from 2025-06-16.
        """
        # Try to load stored numbers first
        stored_numbers = self._load_stored_numbers()
        if stored_numbers:
            return stored_numbers
            
        # If no stored numbers or they're old, scrape new ones
        results = {}  # Will store the latest result for each drawing type
        try:
            html = self._get_rendered_html()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find the table using the correct ID
            table_div = soup.find('div', id='winningNumbersSearchResults')
            if not table_div:
                return {}
                
            table = table_div.find('table', class_='table-winning-numbers-pick')
            if not table:
                return {}
            
            # Get all rows and process them in order (latest first)
            rows = table.find_all('tr', attrs={'data-toggle': 'tableWinningNumbers'})
            for row in rows:
                try:
                    # Get date and draw time
                    date_cell = row.find('td', attrs={'title': 'date'})
                    if not date_cell:
                        continue
                        
                    # Get just the date text without the drawing time div
                    date_text = date_cell.contents[0].strip()  # Get the text node before the div
                    date_str = date_text  # This will be just the date (MM/DD/YYYY)
                    
                    # Get draw time from the div
                    draw_time_div = date_cell.find('div', class_='draw-time')
                    if not draw_time_div:
                        continue
                    draw_time = draw_time_div.get_text(strip=True).lower()
                    
                    # Normalize draw_time to keys: 'midday', 'evening', 'night'
                    if 'mid' in draw_time:
                        drawing_type = 'midday'
                    elif 'eve' in draw_time:
                        drawing_type = 'evening'
                    elif 'night' in draw_time:
                        drawing_type = 'night'
                    else:
                        continue
                    
                    # Skip if we already have a result for this drawing type
                    if drawing_type in results:
                        continue
                    
                    # Get winning numbers
                    numbers_cell = row.find('td', attrs={'title': 'Winning Number'})
                    if not numbers_cell:
                        continue
                        
                    number_spans = numbers_cell.find_all('span')
                    winning_numbers = ''.join(span.find('i').get_text(strip=True) for span in number_spans if span.find('i'))
                    
                    results[drawing_type] = (winning_numbers, date_str)
                    
                    # If we have all three drawing types, we can stop
                    if len(results) == 3:
                        break
                        
                except Exception:
                    continue
                    
            # Save the results
            if results:
                self._save_numbers(results)
                
        except Exception:
            return {}
        return results 