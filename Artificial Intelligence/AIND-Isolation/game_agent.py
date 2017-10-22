"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from scipy.spatial import distance
import numpy as np

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):#do we have moves to play?
        return float("-inf")

    if game.is_winner(player): # have we won the game?
        return float("inf")

    #How many moves do we have to play?
    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    return float(len(my_moves)**2-len(opp_moves)**2)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves-3*opp_moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    #manhattan distance to the center of the game
    w, h = game.width / 2., game.height / 2. #center of the board
    y, x = game.get_player_location(player) #possition
    return distance.cityblock((h - y),(w - x))

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.
    ********************  DO NOT MODIFY THIS CLASS  ********************
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)
            return best_move

        except SearchTimeout:
            #print("   Timed Out - at depth: ",self.search_depth)
            #print("   Best Move: ",best_move)
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        #print('Printing legal moves: /n',game.get_legal_moves())


        # The game is over when the active player has no valid move.
        # So we could check if there is a valid move
        def terminal_test(self,gameState, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            """ Return True if the game is over for the active player
            and False otherwise.
            """
            # if there are no valid moves - game over.
            if len(game.get_legal_moves())<1 or (depth==0):
                return True
            else:
                #print('Legal moves remaining: ',gameState.get_legal_moves())
                return False

        def min_value(gameState, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            """
            Return the value for a win (+1) if the game is over,
            otherwise return the minimum value over all legal child
            nodes.
            """
            # So we can check if the game is over using above terminal_test()
            # If the game is over - return the score according to chosen Heuristic
            if terminal_test(self, gameState, depth):
                return self.score(gameState, self)

            v = float("inf")
            for m in gameState.get_legal_moves():
                v = min(v, max_value(gameState.forecast_move(m), depth-1))
            return v


        def max_value(gameState, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # If we've reached termina state - return the score (Heuristic)
            # for selected move
            if terminal_test(self, gameState, depth):
                return self.score(gameState, self)

            v = float("-inf")
            for m in gameState.get_legal_moves():
                v = max(v, min_value(gameState.forecast_move(m), depth-1))
            return v

        def minimax_decision(self, gameState, depth):

            """ Return the move along a branch of the game tree that
            has the best possible value.  A move is a pair of coordinates
            in (column, row) order corresponding to a legal move for
            the searching player.
            You can ignore the special case of calling this function
            from a terminal state.
            """
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if terminal_test(self, gameState, depth):
                return self.score(gameState, self)

            best_score = float("-inf")
            best_move = gameState.get_legal_moves()[0]
            for m in gameState.get_legal_moves():
                v = min_value(gameState.forecast_move(m), depth-1)
                if v > best_score:
                    best_score = v
                    best_move = m

            # end _minimax_decision
            return best_move

        # end minimax

        return minimax_decision(self, game, depth)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
            return best_move

        except SearchTimeout:

            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        def terminal_test(self,gameState, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            """ Return True if the game is over for the active player
            and False otherwise.
            """
            # if there are no valid moves - game over.
            if len(game.get_legal_moves())<1 or (depth==0):
                return True
            else:

                return False

        def min_value(gameState, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # If we've reached termina state - return the score (Heuristic)
            # for selected move
            if terminal_test(self, gameState, depth):
                return self.score(gameState, self)

            v = float("inf")
            for m in gameState.get_legal_moves():
                v = min(v, max_value(gameState.forecast_move(m), depth-1, alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)

            return v

        def max_value(gameState, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # If we've reached termina state - return the score (Heuristic)
            # for selected move
            if terminal_test(self, gameState, depth):
                return self.score(gameState, self)

            v = float("-inf")
            for m in gameState.get_legal_moves():
                v = max(v, min_value(gameState.forecast_move(m), depth-1, alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)

            return v



        def alpha_beta_search(self, gameState, depth, alpha, beta):

            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # Make sure there is a gameState.get_legal_moves()[0]
            if terminal_test(self, gameState, depth):
                return self.score(gameState, self)

            best_score = float("-inf")
            best_move = gameState.get_legal_moves()[0]
            for m in gameState.get_legal_moves():
                v = min_value(gameState.forecast_move(m), depth-1, alpha, beta)
                if v > best_score:
                    best_score = v
                    best_move = m
                alpha = max(alpha,best_score)
            #print('...  Alpha-Beta Decision :',best_move)
            # end _minimax_decision
            return best_move

        # TODO: finish this function!
        return alpha_beta_search(self, game, depth, alpha, beta)
