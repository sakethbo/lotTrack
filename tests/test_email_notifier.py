import unittest
from datetime import datetime, date
from src.email_notifier import EmailNotifier
from src.play_types import PlayType

class TestEmailNotifier(unittest.TestCase):
    def setUp(self):
        self.email_notifier = EmailNotifier()

    def test_format_winning_message(self):
        ticket = {
            'numbers': ['1', '2', '3', '4'],
            'play_type': 'straight',
            'draw_time': 'MIDDAY',
            'date': date.today()
        }
        winning_numbers = ['1', '2', '3', '4']
        prize_amount = 5000
        
        message = self.email_notifier.format_winning_message(ticket, winning_numbers, prize_amount)
        self.assertIn('Congratulations', message)
        self.assertIn('1-2-3-4', message)
        self.assertIn('$5,000', message)

    def test_format_losing_message(self):
        ticket = {
            'numbers': ['1', '2', '3', '4'],
            'play_type': 'straight',
            'draw_time': 'MIDDAY',
            'date': date.today()
        }
        winning_numbers = ['5', '6', '7', '8']
        
        message = self.email_notifier.format_losing_message(ticket, winning_numbers)
        self.assertIn('Unfortunately', message)
        self.assertIn('1-2-3-4', message)
        self.assertIn('5-6-7-8', message)

    def test_send_notification(self):
        # This test is skipped by default since it requires email credentials
        self.skipTest("Skipping email notification test")
        
        ticket = {
            'numbers': ['1', '2', '3', '4'],
            'play_type': 'straight',
            'draw_time': 'MIDDAY',
            'date': date.today()
        }
        winning_numbers = ['1', '2', '3', '4']
        prize_amount = 5000
        
        # Test sending winning notification
        result = self.email_notifier.send_notification(ticket, winning_numbers, prize_amount)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main() 