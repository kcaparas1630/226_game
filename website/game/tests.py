from django.test import TestCase
from .models import Player, Board
# Create your tests here.

class PlayerTestCase(TestCase):

    def test_create_player(self):
        self.client.post('/game/create')  # Ensure game creation for each test
        p1 = Player.objects.all()
        self.assertEqual(len(p1), 2)
        for players in p1:
            self.assertTrue(players.name == '1' or players.name == '2')
            self.assertTrue(0 <= players.row <= 9)
            self.assertTrue(0 <= players.col <= 9)

    def test_valid_random_player_positions(self):
        self.client.post('/game/create')  # Ensure game creation for each test
        # Test if players are randomly placed within the board
        p1 = Player.objects.get(name='1')
        p2 = Player.objects.get(name='2')
        self.assertNotEqual((p1.row, p1.col), (p2.row, p2.col))  # Ensure players are not in the same position

    def test_player_score_update(self):

        p1 = Player.objects.create(name='1', row=0, col=0, score=0)
        p2 = Player.objects.create(name='2', row=1, col=1, score=0)

        self.assertEqual(p1.row, 0)
        self.assertEqual(p1.col, 0)
        initial_score_p1 = p1.score

        # Create a treasure at a specific position
        treasure = Board.objects.create(label='$', row=1, column=0, value=10)

        # Move Player 1
        response = self.client.post('/game/display/1/', {'direction': 'down'})
        self.assertEqual(response.status_code, 200)  # Check if the request was successful

        # Refresh Player 1 from the database to get the updated score
        p1.refresh_from_db()
        self.assertEqual(p1.score, 10)
        self.assertNotEqual(p1.score, initial_score_p1)


class BoardTestCase(TestCase):



    def test_create_board(self):
        self.client.post('/game/create')  # Ensure game creation for each test
        b = Board.objects.all()
        self.assertEqual(len(b),100)
        for tiles in b:
            self.assertTrue(0 <= tiles.row <= 9)
            self.assertTrue(0 <= tiles.column <= 9)

    def test_treasure_placement(self):
        self.client.post('/game/create')  # Ensure game creation for each test
        # Test placement of treasures
        treasures = Board.objects.filter(label='$')
        self.assertEqual(len(treasures), 5)  # Ensure 5 treasures exist


class MovementTestCase(TestCase):
    def test_invalid_player1_movement_up(self):
        p1 = Player.objects.create(name='1', row=0, col=0, score=0)
        p2 = Player.objects.create(name='2', row=1, col=1, score=0)
        self.client.post(f'/game/display/1/', {'direction': 'up'})
        p1.save()
        self.assertEqual(p1.row, 0)  # Ensure player stays at the top row

    def test_invalid_player1_movement_down(self):
        p1 = Player.objects.create(name='1', row=9, col=9, score=0)
        p2 = Player.objects.create(name='2', row=1, col=1, score=0)
        self.client.post(f'/game/display/1/', {'direction': 'down'})
        p1.save()
        self.assertEqual(p1.row, 9)  # Ensure player stays at the bottom row

    def test_invalid_player1_movement_left(self):
        p1 = Player.objects.create(name='1', row=0, col=0, score=0)
        p2 = Player.objects.create(name='2', row=1, col=1, score=0)
        self.client.post(f'/game/display/1/', {'direction': 'left'})
        p1.save()
        self.assertEqual(p1.col, 0)  # Ensure player stays at the leftmost column

    def test_invalid_player1_movement_right(self):
        p1 = Player.objects.create(name='1', row=9, col=9, score=0)
        p2 = Player.objects.create(name='2', row=1, col=1, score=0)
        self.client.post(f'/game/display/1/', {'direction': 'right'})
        p1.save()
        self.assertEqual(p1.col, 9)  # Ensure player stays at the rightmost column

    def test_invalid_player2_movement_up(self):
        p2 = Player.objects.create(name='2', row=0, col=0, score=0)
        p1 = Player.objects.create(name='1', row=8, col=8, score=0)
        self.client.post(f'/game/display/2/', {'direction': 'up'})
        p2.save()
        self.assertEqual(p2.row, 0)  # Ensure player stays at the top row

    def test_invalid_player2_movement_down(self):
        p2 = Player.objects.create(name='2', row=9, col=9, score=0)
        p1 = Player.objects.create(name='1', row=8, col=8, score=0)
        self.client.post(f'/game/display/2/', {'direction': 'down'})
        p2.save()
        self.assertEqual(p2.row, 9)  # Ensure player stays at the bottom row

    def test_invalid_player2_movement_left(self):
        p2 = Player.objects.create(name='2', row=0, col=0, score=0)
        p1 = Player.objects.create(name='1', row=8, col=8, score=0)
        self.client.post(f'/game/display/2/', {'direction': 'left'})
        p2.save()
        self.assertEqual(p2.col, 0)  # Ensure player stays at the leftmost column

    def test_invalid_player2_movement_right(self):
        p2 = Player.objects.create(name='2', row=9, col=9, score=0)
        p1 = Player.objects.create(name='1', row=8, col=8, score=0)
        self.client.post(f'/game/display/2/', {'direction': 'right'})
        p2.save()
        self.assertEqual(p2.col, 9)  # Ensure player stays at the rightmost column

