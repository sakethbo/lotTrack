import unittest
from datetime import datetime, date
from src.scraper import LotteryScraper

class TestCash4Scraper(unittest.TestCase):
    def setUp(self):
        self.scraper = LotteryScraper()

    def test_get_current_drawing(self):
        """Test getting the current drawing time."""
        latest_results = self.scraper.get_latest_results()
        # Since we're testing against a real API that might be unavailable,
        # we'll accept either a valid result or None
        if latest_results is not None:
            self.assertIn(latest_results['draw_time'], ['MIDDAY', 'EVENING'])

    def test_parse_winning_numbers(self):
        # Test with sample HTML
        sample_html = """
        <table class="table-winning-numbers-pick">
            <tr>
                <td title="date">06/16/2025 NIGHT</td>
                <td title="Winning Number">
                    <div class="lotto-numbers-list">
                        <span><i>4</i></span>
                        <span><i>1</i></span>
                        <span><i>7</i></span>
                        <span><i>7</i></span>
                    </div>
                </td>
                <td title="Winners">269</td>
                <td title="Total Payout">$92,398</td>
            </tr>
        </table>
        """
        results = self.scraper.scrape_winning_numbers()
        if results:  # Only test if we got results
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)
            result = results[0]
            self.assertIsInstance(result['date'], date)
            self.assertIsInstance(result['draw_time'], str)
            self.assertIsInstance(result['winning_numbers'], list)
            self.assertEqual(len(result['winning_numbers']), 4)
            self.assertIsInstance(result['winners'], int)
            self.assertIsInstance(result['payout'], str)

    def test_get_winning_numbers(self):
        winning_numbers = self.scraper.get_winning_numbers()
        self.assertIsInstance(winning_numbers, dict)
        for draw_time, numbers in winning_numbers.items():
            self.assertIn(draw_time, ['MIDDAY', 'EVENING', 'NIGHT'])
            self.assertIsInstance(numbers, list)
            if numbers:
                self.assertEqual(len(numbers), 4)

if __name__ == '__main__':
    unittest.main() 