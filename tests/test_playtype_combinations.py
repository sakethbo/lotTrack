from src.play_types import PlayType

def test_combination(ticket_number: list, winning_number: list):
    """Test a ticket number against a winning number for all play types."""
    print(f"\nTesting ticket: {''.join(ticket_number)} against winning number: {''.join(winning_number)}")
    print("-" * 60)
    
    for play_type in ['straight', 'box', 'straightbox', 'combo', 'oneoff']:
        pt = PlayType.create(play_type, ''.join(ticket_number))
        is_winner, prize = pt.calculate_prize(ticket_number, winning_number)
        print(f"Play type: {play_type:12} | Winner: {is_winner} | Prize: ${prize:,.2f}")

# Test case 1: Exact match
print("\nTest Case 1: Exact Match")
test_combination(['1', '2', '3', '4'], ['1', '2', '3', '4'])

# Test case 2: Box match (same numbers, different order)
print("\nTest Case 2: Box Match")
test_combination(['1', '2', '3', '4'], ['4', '3', '2', '1'])

# Test case 3: One-Off match (one digit off by one)
print("\nTest Case 3: One-Off Match")
test_combination(['1', '2', '3', '4'], ['1', '2', '3', '5'])

# Test case 4: No match
print("\nTest Case 4: No Match")
test_combination(['1', '2', '3', '4'], ['5', '6', '7', '8']) 