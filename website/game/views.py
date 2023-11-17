from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Player
from .models import Board
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import CreateView , UpdateView
import random
from django.db import transaction
# Create your views here.


class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    template_name = 'game/player_form.html'
    success_url = reverse_lazy('players')
class PlayerUpdate(UpdateView):
    model = Player
    fields = ['row', 'col']
    template_name = 'game/player_form.html'
    success_url = reverse_lazy('players')


def create_board(request):
    try:
        rows = 10
        columns = 10

        # Generating the board
        Board.objects.all().delete()  # Clear existing board data
        for row in range(rows):
            for col in range(columns):
                Board.objects.create(row=row, column=col, value=0)

        # Placing treasures randomly on the board
        num_treasures = 5
        for _ in range(num_treasures):
            random_row = random.randint(0, rows - 1)
            random_col = random.randint(0, columns - 1)
            random_value = random.randint(1, 9)
            try:
                cell = Board.objects.get(row=random_row, column=random_col, value=0)
                cell.value = random_value  # Assign the random value to the cell
                cell.label = '$'
                cell.save()
            except Board.DoesNotExist:
                print(f"Cell at row {random_row}, column {random_col}, value {random_value} does not exist.")

        # Creating player instances and placing them randomly on the board
        Player.objects.all().delete()  # Clear existing players
        for player_number in range(1, 3):
            random_row = random.randint(0, rows - 1)
            random_col = random.randint(0, columns - 1)
            p = Player.objects.create(name=str(player_number), row=random_row, col=random_col)
            p.save()
            try:
                cell = Board.objects.get(row=random_row, column=random_col, value=0)
                cell.label = f'{player_number}'
                cell.save()
            except Board.DoesNotExist:
                print(f"Cell at row {random_row}, column {random_col} does not exist.")

        # Return an HTTP response indicating successful board and player creation
        return HttpResponse("Board and players created successfully!")

    except Exception as e:
        # If any exception occurs, return an error message
        return HttpResponse(f"An error occurred: {str(e)}")

def display_game(request):
    player1 = Player.objects.get(name='1')
    player2 = Player.objects.get(name='2')

    # Fetching board data and organizing it into a 10x10 grid format
    board_data = [['' for _ in range(10)] for _ in range(10)]

    # Fetching board data and organizing it into a 10x10 grid format
    for row in range(10):
        cells = Board.objects.filter(row=row).order_by('column')
        for cell in cells:
            board_data[row][cell.column] = cell.label

    context = {
        'player1_row': player1.row,
        'player1_col': player1.col,
        'player2_row': player2.row,
        'player2_col': player2.col,
        'board': board_data,
    }
    return render(request, 'game/display_game.html', context)


@transaction.atomic
def move_player(request, player_id):
    player = get_object_or_404(Player, name=player_id)
    direction = request.POST.get('direction')

    old_row = player.row
    old_col = player.col

    if direction == 'up':
        player.row -= 1
    elif direction == 'down':
        player.row += 1
    elif direction == 'left':
        player.col -= 1
    elif direction == 'right':
        player.col += 1

    # Save the updated player position back to the database
    player.save()

    # Update the corresponding cell label on the board
    try:
        old_cell = Board.objects.get(row=old_row, column=old_col)
        old_cell.label = '*'  # Reset the old cell label to the default value '*'
        old_cell.save()
    except Board.DoesNotExist:
        print(f"Old cell at row {old_row}, column {old_col} does not exist.")
    # Retrieve player scores
    player1 = Player.objects.get(name='1')
    player2 = Player.objects.get(name='2')
    try:
        new_cell = Board.objects.get(row=player.row, column=player.col)
        if new_cell.label == '$':  # Check if the player landed on a treasure cell
            player.score += new_cell.value  # Increment player's score by treasure value
            new_cell.label = f'{player_id}'  # Set the label to the player's identifier
            player.save()
            new_cell.save()

            # Check if all treasures are found
            remaining_treasures = Board.objects.filter(label='$').count()
            if remaining_treasures == 0:
                if player1.score > player2.score:
                    # All treasures found, end the game or perform necessary actions
                    return HttpResponse("Game Over, All treasures found! Player 1 won!")
                else:
                    # All treasures found, end the game or perform necessary actions
                    return HttpResponse("Game Over, All treasures found! Player 2 won!")
        else:
            new_cell.label = f'{player_id}'  # Set the label to the player's identifier
            new_cell.save()
    except Board.DoesNotExist:
        print(f"New cell at row {player.row}, column {player.col} does not exist.")

    # Retrieve the updated board data from the database
    board_data = []
    rows = 10  # Assuming 10 rows
    columns = 10  # Assuming 10 columns

    for row in range(rows):
        row_data = []
        for col in range(columns):
            cell = Board.objects.filter(row=row, column=col).first()
            row_data.append(cell)
        board_data.append(row_data)



    if new_cell.label == '$':
        if player_id == '1':
            player1.score += new_cell.value
            player1.save()
        else:
            player2.score += new_cell.value
            player2.save()

    # Render the template with the properly formatted board data
    return render(request, 'game/game_display.html', {
        'board': board_data,
        'player1_score': player1.score,
        'player2_score': player2.score
    })





def get_player(request, player_id):
    players = Player.objects.filter(name=player_id)
    if len(players) == 1:
        player = players[0]
        return HttpResponse(f'Player {player.name} is at row {player.row} and col {player.col}; with a score of {player.score}')
    else:
        return HttpResponse('No such player')


def get_all_players(request):
    players = Player.objects.all()
    result = ''
    for player in players:
        result += str(player) + '<br>'
    return HttpResponse(result)

