import click
import re
from datetime import datetime, date
from typing import List, Set
from .ticket_manager import TicketManager
from .play_types import PlayType

# Common email domains
COMMON_DOMAINS = {
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
    'icloud.com', 'protonmail.com', 'mail.com', 'live.com', 'msn.com'
}

# Stricter email validation regex pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> bool:
    """Validate email format and check for common typos."""
    # First check basic format
    if not re.match(EMAIL_PATTERN, email):
        return False
    
    # Extract domain
    domain = email.split('@')[1].lower()
    
    # Check for common typos in popular domains
    if domain in ['gmial.com', 'gmai.com', 'gmal.com', 'gnail.com']:
        click.echo("Did you mean 'gmail.com'?")
        return False
    if domain in ['yaho.com', 'yahooo.com']:
        click.echo("Did you mean 'yahoo.com'?")
        return False
    if domain in ['hotmai.com', 'hotmal.com']:
        click.echo("Did you mean 'hotmail.com'?")
        return False
    
    # Check if domain is in common domains list
    if domain not in COMMON_DOMAINS:
        click.echo(f"Warning: '{domain}' is not a common email domain. Please verify your email address.")
        if not click.confirm("Do you want to proceed with this email?"):
            return False
    
    return True

PLAY_TYPES = {
    '1': 'straight',
    '2': 'box',
    '3': 'straightbox',
    '4': 'combo',
    '5': 'oneoff'
}

DRAW_TIMES = {
    '1': 'MIDDAY',
    '2': 'EVENING',
    '3': 'NIGHT'
}

@click.group()
def cli():
    """Georgia Lottery Cash 4 Number Tracker"""
    pass

def get_play_types() -> Set[str]:
    """Get play types from user input."""
    click.echo("\nAvailable Play Types:")
    for key, value in PLAY_TYPES.items():
        click.echo(f"{key}. {value}")
    click.echo("\nEnter numbers separated by commas (e.g., 1,2,3):")
    
    while True:
        choices = input().strip().split(',')
        selected = set()
        for choice in choices:
            if choice.strip() in PLAY_TYPES:
                selected.add(PLAY_TYPES[choice.strip()])
        
        if selected:
            return selected
        click.echo("Invalid selection. Please try again:")

def get_draw_times() -> Set[str]:
    """Get draw times from user input."""
    click.echo("\nAvailable Draw Times:")
    for key, value in DRAW_TIMES.items():
        click.echo(f"{key}. {value}")
    click.echo("\nEnter numbers separated by commas (e.g., 1,2):")
    
    while True:
        choices = input().strip().split(',')
        selected = set()
        for choice in choices:
            if choice.strip() in DRAW_TIMES:
                selected.add(DRAW_TIMES[choice.strip()])
        
        if selected:
            return selected
        click.echo("Invalid selection. Please try again:")

def get_date(prompt: str) -> date:
    """Get date from user input in MM-DD format."""
    while True:
        try:
            date_str = input(f"{prompt} (MM-DD): ").strip()
            month, day = map(int, date_str.split('-'))
            # Use current year
            year = datetime.now().year
            return date(year, month, day)
        except ValueError:
            click.echo("Invalid date format. Please use MM-DD (e.g., 06-16):")

def get_email() -> str:
    """Get and validate email from user input."""
    while True:
        email = input("Enter your email address: ").strip()
        if validate_email(email):
            return email
        click.echo("Invalid email format. Please enter a valid email address (e.g., user@example.com):")

@cli.command()
@click.option('--numbers', prompt='Enter your 4-digit number (e.g., 1234)',
              help='Your 4-digit lottery number')
def add_ticket(numbers):
    """Add a new lottery ticket to track."""
    ticket_manager = TicketManager()
    
    # Validate numbers
    number_list = list(numbers)
    if not ticket_manager._validate_numbers(number_list):
        click.echo('Error: Invalid number format. Please enter 4 digits (0-9)')
        return
    
    # Get email
    email = get_email()
    
    # Get play types
    selected_play_types = get_play_types()
    
    # Get draw times
    selected_draw_times = get_draw_times()
    
    # Get dates
    start_date = get_date("Start date")
    end_date = get_date("End date")
    
    # Show summary before creating tickets
    total_tickets = len(selected_play_types) * len(selected_draw_times)
    click.echo(f"\nYou are about to create {total_tickets} ticket(s):")
    click.echo(f"Number: {numbers}")
    click.echo(f"Email: {email}")
    click.echo(f"Play Types: {', '.join(selected_play_types)}")
    click.echo(f"Draw Times: {', '.join(selected_draw_times)}")
    click.echo(f"Valid from: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Confirm with user
    if not click.confirm("\nDo you want to proceed?"):
        click.echo("Ticket creation cancelled.")
        return
    
    # Add tickets for each combination
    success_count = 0
    for play_type in selected_play_types:
        for draw_time in selected_draw_times:
            if ticket_manager.add_ticket(number_list, play_type, draw_time, start_date, end_date, email):
                success_count += 1
    
    if success_count > 0:
        click.echo(f'\nSuccessfully added {success_count} ticket(s)!')
        click.echo("\nCreated tickets:")
        for play_type in selected_play_types:
            for draw_time in selected_draw_times:
                click.echo(f"- {play_type} play for {draw_time} drawing")
    else:
        click.echo('Error: Failed to add tickets')

@cli.command()
def list_tickets():
    """List all your lottery tickets."""
    ticket_manager = TicketManager()
    tickets = ticket_manager.list_tickets()
    
    if not tickets:
        click.echo('No tickets found.')
        return
    
    for i, ticket in enumerate(tickets):
        click.echo(f"\nTicket #{i + 1}:")
        # Handle both string and list number formats
        numbers = ticket['numbers']
        if isinstance(numbers, list):
            numbers = ''.join(numbers)
        click.echo(f"Numbers: {numbers}")
        click.echo(f"Play Type: {ticket['play_type']}")
        # Handle optional draw_time field
        if 'draw_time' in ticket:
            click.echo(f"Draw Time: {ticket['draw_time']}")
        click.echo(f"Start Date: {ticket['start_date']}")
        click.echo(f"End Date: {ticket['end_date']}")
        if 'email' in ticket:
            click.echo(f"Email: {ticket['email']}")

@cli.command()
@click.option('--ticket-number', prompt='Enter the ticket number to delete (1-N)',
              help='The number of the ticket to delete')
def delete_ticket(ticket_number):
    """Delete a lottery ticket."""
    try:
        ticket_index = int(ticket_number) - 1  # Convert to 0-based index
        ticket_manager = TicketManager()
        
        # List tickets first so user can see what they're deleting
        tickets = ticket_manager.list_tickets()
        if not tickets:
            click.echo('No tickets found.')
            return
            
        if not 0 <= ticket_index < len(tickets):
            click.echo(f'Error: Invalid ticket number. Please enter a number between 1 and {len(tickets)}')
            return
            
        # Show ticket details before deletion
        ticket = tickets[ticket_index]
        click.echo("\nTicket to be deleted:")
        numbers = ticket['numbers']
        if isinstance(numbers, list):
            numbers = ''.join(numbers)
        click.echo(f"Numbers: {numbers}")
        click.echo(f"Play Type: {ticket['play_type']}")
        if 'draw_time' in ticket:
            click.echo(f"Draw Time: {ticket['draw_time']}")
        click.echo(f"Start Date: {ticket['start_date']}")
        click.echo(f"End Date: {ticket['end_date']}")
        if 'email' in ticket:
            click.echo(f"Email: {ticket['email']}")
            
        # Confirm deletion
        if click.confirm("\nAre you sure you want to delete this ticket?"):
            if ticket_manager.remove_ticket(ticket_index):
                click.echo('Ticket deleted successfully.')
            else:
                click.echo('Error: Failed to delete ticket.')
        else:
            click.echo('Ticket deletion cancelled.')
            
    except ValueError:
        click.echo('Error: Please enter a valid ticket number.')

@cli.command()
@click.argument('ticket_index', type=int)
def update_dates(ticket_index):
    """Update the validity dates of a ticket."""
    ticket_manager = TicketManager()
    
    start_date = get_date("New start date")
    end_date = get_date("New end date")
    
    if ticket_manager.update_ticket_dates(ticket_index - 1, start_date, end_date):
        click.echo('Dates updated successfully!')
    else:
        click.echo('Error: Failed to update dates. Check if the ticket exists.')

@cli.command()
@click.argument('ticket_index', type=int)
def remove_ticket(ticket_index):
    """Remove a lottery ticket."""
    ticket_manager = TicketManager()
    
    if ticket_manager.remove_ticket(ticket_index - 1):
        click.echo('Ticket removed successfully!')
    else:
        click.echo('Error: Failed to remove ticket. Check if the ticket exists.')

@cli.command()
def check_active():
    """Check all active tickets."""
    ticket_manager = TicketManager()
    active_tickets = ticket_manager.get_active_tickets()
    
    if not active_tickets:
        click.echo('No active tickets found.')
        return
    
    click.echo(f"Found {len(active_tickets)} active tickets:")
    for i, ticket in enumerate(active_tickets):
        click.echo(f"\nTicket #{i + 1}:")
        click.echo(f"Numbers: {''.join(ticket['numbers'])}")
        click.echo(f"Play Type: {ticket['play_type']}")
        click.echo(f"Draw Time: {ticket['draw_time']}")
        click.echo(f"Valid until: {ticket['end_date']}")

if __name__ == '__main__':
    cli() 