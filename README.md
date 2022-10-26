# Chess-Game-Server
Endpoint to mange a game of chess (with any front end that conforms to API)

1. To start the end point

flask run # optionally [--debugger --reload]

2. To create a new game instance

	GET request to '/' (usually base url is 'http://127.0.0.1:5000', so 'http://127.0.0.1:5000/')
	RETURNS a game id, as well as positions of pieces on the board

3. To get positions of pieces on the board

	GET request to 'game_id/positions'
	1. returns positions of pieces on the board
	2. returns current moves in the game
4. To make a move
	POST request to 'game_id/move'
	body {
		move:'valid chess move string' e.g e4 / Nf3 / ...etc
	}
	RETURNS 200 if move is valid and updates the particular game instance
