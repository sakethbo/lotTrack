import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

class EmailNotifier:
    """Handles sending email notifications for lottery results."""
    
    def __init__(self, config_file: str = "config/config.json"):
        self.config = self._load_config(config_file)
        self.email_config = self.config.get('email', {})
        
        # Get sender email credentials from environment variables (for security)
        self.sender_email = os.getenv('EMAIL_USER', self.email_config.get('sender_email', ''))
        self.sender_password = os.getenv('EMAIL_PASSWORD', self.email_config.get('sender_password', ''))
        
        if not all([self.sender_email, self.sender_password]):
            logger.warning("Email configuration is incomplete. Notifications will not be sent.")
        
    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {str(e)}")
            return {}

    def _create_html_content(self, drawing_type: str, winning_numbers: str,
                           results: Dict[str, List[Dict]]) -> str:
        """Create HTML content for the email."""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .ticket {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; }}
                .win {{ color: green; }}
                .no-win {{ color: red; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Georgia Cash 4 Results</h2>
                    <p>Drawing Type: {drawing_type}</p>
                    <p>Winning Numbers: {winning_numbers}</p>
                    <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="content">
        """
        
        if not results:
            html += "<p class='no-win'>No winning tickets for this drawing.</p>"
        else:
            for user_id, user_results in results.items():
                html += f"<h3>User: {user_id}</h3>"
                for result in user_results:
                    html += f"""
                    <div class="ticket">
                        <p>Ticket ID: {result['ticket_id']}</p>
                        <p class="win">Prize Amount: ${result['prize']:.2f}</p>
                    </div>
                    """
                    
        html += """
                </div>
            </div>
        </body>
        </html>
        """
        return html
        
    def _create_plain_content(self, drawing_type: str, winning_numbers: str,
                            results: Dict[str, List[Dict]]) -> str:
        """Create plain text content for the email."""
        content = f"""
Georgia Cash 4 Results
=====================
Drawing Type: {drawing_type}
Winning Numbers: {winning_numbers}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if not results:
            content += "No winning tickets for this drawing."
        else:
            for user_id, user_results in results.items():
                content += f"\nUser: {user_id}\n"
                for result in user_results:
                    content += f"""
Ticket ID: {result['ticket_id']}
Prize Amount: ${result['prize']:.2f}
"""
                    
        return content
        
    def _create_message(self, subject: str, body: str, recipient_email: str) -> MIMEMultipart:
        """Create an email message."""
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        return message

    def send_notification(self, ticket: Dict, winning_numbers: list, prize_amount: float) -> bool:
        """Send notification about lottery results."""
        try:
            if not all([self.sender_email, self.sender_password]):
                logger.error("Email configuration is incomplete")
                return False

            recipient_email = ticket.get('email')
            if not recipient_email:
                logger.error("No recipient email found in ticket")
                return False

            if prize_amount > 0:
                subject = "🎉 Congratulations! You Won the Georgia Cash 4!"
                body = self.format_winning_message(ticket, winning_numbers, prize_amount)
            else:
                subject = "Georgia Cash 4 Results"
                body = self.format_losing_message(ticket, winning_numbers)

            message = self._create_message(subject, body, recipient_email)
            
            # Connect to Gmail SMTP server
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()  # Enable TLS
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            logger.info(f"Email notification sent successfully to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            return False

    def send_expiration_notification(self, ticket: Dict, days_remaining: int) -> bool:
        """Send notification about ticket expiration."""
        try:
            if not all([self.sender_email, self.sender_password]):
                logger.error("Email configuration is incomplete")
                return False

            recipient_email = ticket.get('email')
            if not recipient_email:
                logger.error("No recipient email found in ticket")
                return False

            subject = "⚠️ Your Georgia Cash 4 Ticket is Expiring Soon"
            body = self.format_expiration_message(ticket, days_remaining)
            
            message = self._create_message(subject, body, recipient_email)
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            logger.info(f"Expiration notification sent successfully to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending expiration notification: {str(e)}")
            return False

    def format_winning_message(self, ticket: Dict, winning_numbers: list, prize_amount: float) -> str:
        """Format winning notification message."""
        return f"""
Congratulations! Your Georgia Cash 4 ticket has won!

Your Numbers: {'-'.join(ticket['numbers'])}
Winning Numbers: {'-'.join(winning_numbers)}
Play Type: {ticket['play_type']}
Draw Time: {ticket['draw_time']}
Prize Amount: ${prize_amount:,.2f}

Please claim your prize within 180 days of the drawing date.

Good luck with your next ticket!
"""

    def format_losing_message(self, ticket: Dict, winning_numbers: list) -> str:
        """Format losing notification message."""
        return f"""
Your Georgia Cash 4 results are in:

Your Numbers: {'-'.join(ticket['numbers'])}
Winning Numbers: {'-'.join(winning_numbers)}
Play Type: {ticket['play_type']}
Draw Time: {ticket['draw_time']}

Unfortunately, this ticket did not win. Better luck next time!
"""

    def format_expiration_message(self, ticket: Dict, days_remaining: int) -> str:
        """Format expiration notification message."""
        return f"""
Your Georgia Cash 4 ticket is expiring soon!

Ticket Details:
Numbers: {'-'.join(ticket['numbers'])}
Play Type: {ticket['play_type']}
Draw Time: {ticket['draw_time']}
Days Remaining: {days_remaining}

If you want to continue tracking these numbers, please update the ticket's end date using the CLI:
python -m src.cli update-dates <ticket_number> --start-date YYYY-MM-DD --end-date YYYY-MM-DD
""" 