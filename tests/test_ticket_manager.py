import unittest
from datetime import datetime, date
from src.ticket_manager import TicketManager

class TestTicketManager(unittest.TestCase):
    def setUp(self):
        self.ticket_manager = TicketManager()

    def test_add_ticket(self):
        self.ticket_manager.add_ticket(['1', '2', '3', '4'], 'straight', 'MIDDAY', date.today(), date.today(), 'test@example.com')
        tickets = self.ticket_manager.get_tickets()
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]['numbers'], ['1', '2', '3', '4'])

    def test_remove_ticket(self):
        # Add a ticket first
        self.ticket_manager.add_ticket(['1', '2', '3', '4'], 'straight', 'MIDDAY', date.today(), date.today(), 'test@example.com')
        
        # Remove the ticket
        self.ticket_manager.remove_ticket(0)
        tickets = self.ticket_manager.get_tickets()
        self.assertEqual(len(tickets), 0)

    def test_get_tickets_for_drawing(self):
        # Add tickets for different drawings
        self.ticket_manager.add_ticket(['1', '2', '3', '4'], 'straight', 'MIDDAY', date.today(), date.today(), 'test@example.com')
        self.ticket_manager.add_ticket(['5', '6', '7', '8'], 'straight', 'EVENING', date.today(), date.today(), 'test@example.com')
        
        # Get tickets for MIDDAY drawing
        midday_tickets = self.ticket_manager.get_tickets_for_drawing('MIDDAY')
        self.assertEqual(len(midday_tickets), 1)
        self.assertEqual(midday_tickets[0]['numbers'], ['1', '2', '3', '4'])

    def test_check_winning_numbers(self):
        # Add a ticket
        self.ticket_manager.add_ticket(['1', '2', '3', '4'], 'straight', 'MIDDAY', date.today(), date.today(), 'test@example.com')
        
        # Check with winning numbers
        winning_numbers = ['1', '2', '3', '4']
        results = self.ticket_manager.check_winning_numbers(winning_numbers, 'MIDDAY')
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]['is_winner'])

if __name__ == '__main__':
    unittest.main() 