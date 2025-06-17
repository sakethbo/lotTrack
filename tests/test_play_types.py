import unittest
from src.play_types import (
    Straight, Box, StraightBox, Combo, OneOff,
    create_play_type
)

class TestPlayTypes(unittest.TestCase):
    def test_straight_win(self):
        # Test $1 bet
        ticket = Straight("1234", 1.0)
        self.assertEqual(ticket.calculate_prize("1234"), 5000.0)
        self.assertEqual(ticket.calculate_prize("4321"), 0.0)
        
        # Test $0.50 bet
        ticket = Straight("1234", 0.5)
        self.assertEqual(ticket.calculate_prize("1234"), 2500.0)
        
    def test_box_win(self):
        """Test box play type with winning numbers."""
        ticket = Box("1211", 1.0)
        self.assertEqual(ticket.calculate_prize("1211"), 400.0)  # 4-way box pays $400
        
        # 6-way box (2 pairs)
        ticket = Box("1122", 1.0)
        self.assertEqual(ticket.calculate_prize("1212"), 800.0)
        
        # 12-way box (3 same, 1 different)
        ticket = Box("1112", 1.0)
        self.assertEqual(ticket.calculate_prize("1211"), 400.0)
        
        # 24-way box (all different)
        ticket = Box("1234", 1.0)
        self.assertEqual(ticket.calculate_prize("4321"), 200.0)
        
    def test_straightbox_win(self):
        """Test straight/box play type with winning numbers."""
        ticket = StraightBox("1122", 1.0)
        self.assertEqual(ticket.calculate_prize("1122"), 3300.0)  # Straight ($2900) + Box ($400)
        
        # 6-way box straight/box
        ticket = StraightBox("1122", 1.0)
        self.assertEqual(ticket.calculate_prize("1122"), 3300.0)  # 2900 + 400
        self.assertEqual(ticket.calculate_prize("1212"), 400.0)   # Box only
        
        # 12-way box straight/box
        ticket = StraightBox("1123", 1.0)
        self.assertEqual(ticket.calculate_prize("1123"), 2900.0)  # 2700 + 200
        self.assertEqual(ticket.calculate_prize("1213"), 200.0)   # Box only
        
        # 24-way box straight/box
        ticket = StraightBox("1234", 1.0)
        self.assertEqual(ticket.calculate_prize("1234"), 2700.0)  # 2600 + 100
        self.assertEqual(ticket.calculate_prize("4321"), 100.0)   # Box only
        
    def test_combo_win(self):
        """Test combo play type with winning numbers."""
        numbers = "1234"
        ticket = Combo(numbers, 1.0)
        self.assertEqual(ticket.calculate_prize(numbers), 208.33)  # $5000 / 24 combinations
        
    def test_oneoff_win(self):
        # Test straight match
        ticket = OneOff("1234", 1.0)
        self.assertEqual(ticket.calculate_prize("1234"), 2500.0)
        
        # Test one digit 1-off
        ticket = OneOff("1234", 1.0, off_count=1)
        self.assertEqual(ticket.calculate_prize("0234"), 124.0)
        
        # Test two digit 1-off
        ticket = OneOff("1234", 1.0, off_count=2)
        self.assertEqual(ticket.calculate_prize("0235"), 24.0)
        
        # Test three digit 1-off
        ticket = OneOff("1234", 1.0, off_count=3)
        ticket = OneOff("1234", 1.0, off_count=4)
        self.assertEqual(ticket.calculate_prize("0123"), 32.0)
        
    def test_create_play_type(self):
        # Test creating each play type
        play_types = ['straight', 'box', 'straightbox', 'combo', 'oneoff']
        for play_type in play_types:
            ticket = create_play_type(play_type, "1234", 1.0)
            self.assertIsNotNone(ticket)
            
        # Test invalid play type
        with self.assertRaises(ValueError):
            create_play_type("invalid", "1234", 1.0)
            
    def test_invalid_numbers(self):
        # Test invalid number formats
        invalid_numbers = ["123", "12345", "abcd", "12.34"]
        for numbers in invalid_numbers:
            with self.assertRaises(ValueError):
                Straight(numbers, 1.0)
                
    def test_invalid_box_type(self):
        # Test invalid box combinations
        with self.assertRaises(ValueError):
            Box("12345", 1.0)
            
    def test_invalid_combo_type(self):
        # Test invalid combo combinations
        with self.assertRaises(ValueError):
            Combo("12345", 1.0)
            
    def test_invalid_oneoff_count(self):
        # Test invalid 1-off counts
        with self.assertRaises(ValueError):
            OneOff("1234", 1.0, off_count=5)
        with self.assertRaises(ValueError):
            OneOff("1234", 1.0, off_count=0)
            
if __name__ == '__main__':
    unittest.main() 