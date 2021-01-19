import time

global ai_player, human_player

def ask_user_start():
    val = input("Choose X or O where O gets to go first: ")
    global ai_player, human_player
    if val == "O":
        ai_player = "X"
        human_player = "O"
    else:
        ai_player = "O"
        human_player = "X"

def ask_user_play(board):
    val = input("Choose an empty square to place your next move (1-9): ")
    if isinstance(board[int(val)-1], int):
        board[int(val)-1] = human_player
        print_board(board)
        return board
    else:
        print("This square is already taken, please try again.")
        board = ask_user_play(board)
        return board


def print_board(board):
    board = [" " if isinstance(pos, int) else pos for pos in board]
    for i in range(3):
        print(str(board[i*3]) + " | " + str(board[i*3+1]) + " | " + str(board[i*3+2]) + "        " + str(i*3+1) + " | " + str(i*3+2) + " | " + str(i*3+3))
        if i < 2:
            print("---------        ---------")


def create_board():
    print_board()


def empty_indexes(board):
    return filter(lambda s: isinstance(s, int), board)


def is_winning(board, player):
    # list of winning combinations
    winning_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for indexes in winning_combinations:
        if board[indexes[0]-1] == player and board[indexes[1]-1] == player and board[indexes[2]-1] == player:
            return True
    return False


def minimax(board, player, position=0):
    available_indexes = list(empty_indexes(board))
    # return a value if the board has been completely filled
    if is_winning(board, ai_player):
        return [1, position]
    elif is_winning(board, human_player):
        return [-1, position]
    elif len(available_indexes) == 0:
        return [0, position]
    total_moves = []
    # generate new boards for every available index
    for index in available_indexes:
        new_board = board.copy()
        new_board[index-1] = player
        if player == ai_player:
            result = minimax(new_board, human_player)
        else:
            result = minimax(new_board, ai_player)
        total_moves.append([result[0], index])
    # find minimum if it is for the human player, find maximum if it is for the ai player
    if player == ai_player:
        total_moves = sorted(total_moves, key=lambda x: x[0], reverse=True)
        return total_moves[0]
    else:
        total_moves = sorted(total_moves, key=lambda x: x[0])
        return total_moves[0]


def minimax_alpha_beta(board, player, alpha, beta, position=0):
    available_indexes = list(empty_indexes(board))
    # return a value if the board has been completely filled
    if is_winning(board, ai_player):
        # return value of beta or alpha depending on if it is a min or max level
        if player == ai_player:
            return [1, position, -2, 1]
        else:
            return [1, position, 1, 2]
    elif is_winning(board, human_player):
        # return value of beta or alpha depending on if it is a min or max level
        if player == ai_player:
            return [-1, position, -2, -1]
        else:
            return [-1, position, -1, 2]
    elif len(available_indexes) == 0:
        # return value of beta or alpha depending on if it is a min or max level
        if player == ai_player:
            return [0, position, -2, 0]
        else:
            return [0, position, 0, 2]
    total_moves = []
    # generate new boards for every available index
    for index in available_indexes:
        new_board = board.copy()
        new_board[index-1] = player
        if player == ai_player:
            result = minimax_alpha_beta(new_board, human_player, alpha, beta)
            # check to see if alpha needs to be updated
            alpha = max(alpha, result[2])
            # check if branches can be pruned
            if alpha >= beta:
                total_moves.append([result[0], index, alpha, beta])
                break
        else:
            result = minimax_alpha_beta(new_board, ai_player, alpha, beta)
            # check to see if beta needs to be updated
            beta = min(beta, result[3])
            # check if branches can be pruned
            if beta <= alpha:
                total_moves.append([result[0], index, alpha, beta])
                break
        total_moves.append([result[0], index, alpha, beta])
    # find minimum if it is for the human player, find maximum if it is for the ai player
    if player == ai_player:
        total_moves = sorted(total_moves, key=lambda x: x[0], reverse=True)
        # swap alpha and beta values
        total_moves[0][2], total_moves[0][3] = total_moves[0][3], total_moves[0][2]
        return total_moves[0]
    else:
        total_moves = sorted(total_moves, key=lambda x: x[0])
        # swap alpha and beta values
        total_moves[0][2], total_moves[0][3] = total_moves[0][3], total_moves[0][2]
        return total_moves[0]


def ai_play(board, alpha_beta):
    start_time = time.time()
    if alpha_beta:
        [evaluation, index, alpha, beta] = minimax_alpha_beta(board, ai_player, -2, 2)
    else:
        [evaluation, index] = minimax(board, ai_player)
    board[index-1] = ai_player
    end_time = time.time()
    print("AI has taken " + str(end_time-start_time) + " seconds to play")
    print_board(board)
    return board


def play_game(board, alpha_beta):
    while len(list(empty_indexes(board))) > 0:
        board = ai_play(board, alpha_beta)
        if check_for_win(board):
            break
        board = ask_user_play(board)
        if check_for_win(board):
            break


def check_for_win(board):
    available_indexes = list(empty_indexes(board))
    if is_winning(board, ai_player):
        print("The computer has won!")
        return 1
    elif is_winning(board, human_player):
        print("You have won!")
        return 1
    elif len(available_indexes) == 0:
        print("It is a tie!")
        return 1
    else:
        return 0


def main():
    alpha_beta = True
    empty_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ask_user_start()
    if human_player == "O":
        print_board(empty_board)
        board = ask_user_play(empty_board)
        play_game(board, alpha_beta)
    else:
        play_game(empty_board, alpha_beta)


if __name__ == "__main__":
    main()
