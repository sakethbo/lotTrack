import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
import pytz
from .play_types import PlayType

class TicketManager:
    """Manages lottery tickets and their results."""
    
    def __init__(self, data_file: str = None):
        if data_file is None:
            # Try to load from config
            try:
                with open('config/config.json', 'r') as f:
                    config = json.load(f)
                    data_file = config['data_files']['tickets']
            except Exception:
                data_file = "data/tickets.json"
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        
        self.data_file = data_file
        self.tickets = self._load_tickets()
        
    def _load_tickets(self) -> List[Dict[str, Any]]:
        """Load tickets from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
        
    def _save_tickets(self):
        """Save tickets to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tickets, f, indent=2)
        except Exception:
            pass

    def _validate_numbers(self, numbers: List[str]) -> bool:
        """Validate ticket numbers."""
        if len(numbers) != 4:
            return False
        return all(n.isdigit() and 0 <= int(n) <= 9 for n in numbers)
            
    def add_ticket(self, numbers: List[str], play_type: str, draw_time: str, 
                  start_date: date, end_date: date, email: str) -> bool:
        """Add a new ticket."""
        if not numbers or not play_type or not draw_time or not start_date or not end_date or not email:
            return False
            
        # Ensure numbers are stored as a list
        if isinstance(numbers, str):
            numbers = list(numbers)
            
        ticket = {
            'numbers': numbers,
            'play_type': play_type,
            'draw_time': draw_time,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'email': email,
            'created_at': date.today().isoformat()
        }
        
        self.tickets.append(ticket)
        self._save_tickets()
        return True
        
    def remove_ticket(self, ticket_index: int) -> bool:
        """Remove a ticket by index."""
        if 0 <= ticket_index < len(self.tickets):
            self.tickets.pop(ticket_index)
            self._save_tickets()
            return True
        return False
        
    def get_tickets(self) -> List[Dict[str, Any]]:
        """Get all tickets."""
        return self.tickets
        
    def list_tickets(self) -> List[Dict[str, Any]]:
        """Alias for get_tickets to maintain CLI compatibility."""
        return self.get_tickets()
        
    def get_tickets_for_drawing(self, drawing_date: date) -> List[Dict[str, Any]]:
        """Get tickets that are valid for a specific drawing date."""
        return [
            t for t in self.tickets
            if datetime.fromisoformat(t['start_date']).date() <= drawing_date <= datetime.fromisoformat(t['end_date']).date()
        ]
        
    def get_active_tickets(self) -> List[Dict[str, Any]]:
        """Get all active tickets."""
        today = date.today()
        return [
            t for t in self.tickets
            if datetime.fromisoformat(t['start_date']).date() <= today <= datetime.fromisoformat(t['end_date']).date()
        ]
        
    def update_ticket_dates(self, ticket_index: int, start_date: date, end_date: date) -> bool:
        """Update the dates of a ticket."""
        if 0 <= ticket_index < len(self.tickets):
            self.tickets[ticket_index]['start_date'] = start_date.isoformat()
            self.tickets[ticket_index]['end_date'] = end_date.isoformat()
            self._save_tickets()
            return True
        return False
        
    def check_ticket(self, ticket: Dict[str, Any], winning_numbers: str) -> Tuple[bool, float]:
        """Check if a ticket is a winner and calculate prize."""
        if not ticket or not winning_numbers:
            return False, 0.0
            
        numbers = ticket['numbers']
        play_type = ticket['play_type']
        
        # Create play type instance
        play = PlayType.create(play_type, ''.join(numbers))
        if not play:
            return False, 0.0
            
        # Check if ticket is a winner
        is_winner, prize = play.calculate_prize(numbers, list(winning_numbers))
        return is_winner, prize

    def check_winning_numbers(self, winning_numbers: str, draw_time: str):
        """
        Check all tickets for the given draw_time against the winning numbers.
        Returns a list of dicts with ticket, is_winner, prize_amount, and winning_numbers.
        """
        results = []
        for ticket in self.tickets:
            # Only check tickets for the specified draw time and if ticket is active
            if ticket.get('draw_time', '').upper() == draw_time.upper():
                # Check if ticket is active (valid for today)
                today = date.today()
                start = datetime.fromisoformat(ticket['start_date']).date()
                end = datetime.fromisoformat(ticket['end_date']).date()
                if start <= today <= end:
                    is_winner, prize = self.check_ticket(ticket, winning_numbers)
                    results.append({
                        'ticket': ticket,
                        'is_winner': is_winner,
                        'prize_amount': prize,
                        'winning_numbers': list(winning_numbers)
                    })
        return results 