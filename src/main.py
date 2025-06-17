import os
import logging
from datetime import datetime, date
from typing import Dict, List
from dotenv import load_dotenv
load_dotenv()
from .scraper import LotteryScraper
from .ticket_manager import TicketManager
from .email_notifier import EmailNotifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lottery_check.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_drawing(draw_time: str, scraper: LotteryScraper, ticket_manager: TicketManager, email_notifier: EmailNotifier):
    """Check a specific drawing time."""
    try:
        # Get winning numbers for the drawing
        winning_numbers = scraper.get_winning_numbers().get(draw_time.lower())
        if not winning_numbers:
            logger.warning(f"No winning numbers found for {draw_time} drawing")
            return

        # Check tickets against winning numbers
        results = ticket_manager.check_winning_numbers(winning_numbers[0], draw_time)
        
        # Process results
        for result in results:
            ticket = result['ticket']
            if result['is_winner']:
                # Send winning notification
                email_notifier.send_notification(
                    ticket,
                    result['winning_numbers'],
                    result['prize_amount']
                )
                logger.info(f"Winner found! Ticket {ticket['numbers']} won ${result['prize_amount']}")
            else:
                # Send losing notification
                email_notifier.send_notification(
                    ticket,
                    result['winning_numbers'],
                    0
                )
                logger.info(f"No win for ticket {ticket['numbers']}")

    except Exception as e:
        logger.error(f"Error checking {draw_time} drawing: {str(e)}")

def main():
    """Main function to check all drawings."""
    try:
        # Initialize components
        scraper = LotteryScraper()
        ticket_manager = TicketManager()
        email_notifier = EmailNotifier()

        # Check all three drawings
        drawing_times = ['MIDDAY', 'EVENING', 'NIGHT']
        for draw_time in drawing_times:
            logger.info(f"Checking {draw_time} drawing...")
            check_drawing(draw_time, scraper, ticket_manager, email_notifier)

        # Check for tickets that are about to expire
        today = date.today()
        active_tickets = ticket_manager.get_active_tickets()
        for ticket in active_tickets:
            end_date = datetime.fromisoformat(ticket['end_date']).date()
            days_remaining = (end_date - today).days
            
            if days_remaining <= 3:  # Notify if ticket expires in 3 days or less
                email_notifier.send_expiration_notification(ticket, days_remaining)
                logger.info(f"Sent expiration notification for ticket {ticket['numbers']}")

    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main() 