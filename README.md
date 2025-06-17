# Georgia Lottery Cash 4 Tracker

An automated lottery number tracking system for Georgia Cash 4 lottery numbers. This application tracks winning numbers, manages user tickets, calculates prizes, and sends email notifications for wins/losses.

## Features

- Automated tracking of Georgia Cash 4 lottery numbers
- Support for all Cash 4 play types (Straight, Box, Straight/Box, Combo, 1-Off)
- Daily automated checks via GitHub Actions
- Email notifications for wins/losses
- Ticket management and prize calculations
- Historical results tracking

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/georgia-lottery-tracker.git
cd georgia-lottery-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your email credentials and preferences

4. Set up GitHub Actions:
   - Fork this repository
   - Add your email credentials as GitHub Secrets:
     - `SENDER_EMAIL`
     - `SENDER_PASSWORD`
     - `RECIPIENT_EMAIL`
     - `SMTP_SERVER`
     - `SMTP_PORT`

## Play Types

### Straight (Exact Order)
- Match all 4 numbers in exact order
- Prize: $5,000 for $1 bet

### Box (Any Order)
- Match all 4 numbers in any order
- Variations: 4-way, 6-way, 12-way, 24-way
- Prize varies based on combination

### Straight/Box
- Split $1 bet: 50¢ straight + 50¢ box
- Can win both straight and box prizes

### Combo
- Covers all straight combinations of selected numbers
- Prize varies based on number of combinations

### 1-Off
- Match numbers within 1 digit
- Variations: 1-off, 2-off, 3-off, 4-off

## Project Structure

```
georgia-lottery-tracker/
├── .github/workflows/    # GitHub Actions configuration
├── src/                  # Source code
├── data/                 # Data storage
├── config/              # Configuration files
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 