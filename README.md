checkers
========

Simple checkers server for practice writing ai clients

File structure
--------------
This contains two executable scripts "server.py" and "termclient.py".

server.py executes a rule enforcing checkers server. It accepts two connections then
begins a game. Once the game is finished it shuts itself down. By default sever.py only
accepts connections from localhost. It scans for an open port from 8080 to 8090 and prints
the port it is listening on to the terminal.

termclient.py executes a terminal based checker playing client. It attempts to connect to
localhost port 8080 by default. Use the -p option to make it listen on a different port.
termclient.py is meant only to be slightly more convient to test with than telnet, in that it
prints the board. Commands should be given to termclient.py exactly as they will be sent over
to the server.

The other python files are shared logic.

ipc.py is the interprocess communication. It defines classes to make it easy to use a line based
protocol over sockets.

checkers.py contains all logic having to do with checkers.

All code is python 3.

Instructions for people with only python 2 installed
----------------------------------------------------

Install python 3

Initial layout and terminology
------------------------------

The board initial layout looks as follows:

<pre>
   abcdefgh
  +--------+
 8| b b b b|
 7|b b b b |
 6| b b b b|
 5|        |
 4|        |
 3|r r r r |
 2| r r r r|
 1|r r r r |
  +--------+
</pre>

r stands for a red piece. b stands for a black piece.
R will be used to represent a red king. B will be used to represent a black king.

To keep things simple for both the ai and the server:
 * it is always red's turn first
 * red always starts at the low numbered rows

A board position is given specified by the column and row. For example there is a
black piece at a7.

The protocol
------------

First, start the server. Once both players are connected it sends out messages
to let the clients know the game has started and some of the game options.

Every message follows the following format:

    COMMAND:details\n

Both \n and \r\n newlines are supported newlines. Everything is case sensitive.
COMMAND should always be all caps.


The following commands can be sent from the client
--------------------------------------------------

<dl>
 <dt>QUIT:ignored</dt>
 <dd>This causes the current player to lose</dd>

 <dt>MOVE:a3,b4</dt>
 <dd>This moves the piece from a3 to b4. This is a valid first move.
     For double (or more) jumps simply use more commas. For example:
     MOVE:a3,c5,a7</dd>
</dl>

The following commands can be sent from the server
--------------------------------------------------

<dl>
 <dt>GAMESTART:board_size=8,board_rows=3,turn=second,color=b</dt>
 <dd>Sinals the start of the game. This is received by black (shown by
     the b) who will go second.</dd>

 <dt>ACCEPTED:unimportant</dt>
 <dd>Signals that the move just given by the client was accepted as a valid
     move by the server.</dd>

 <dt>REJECTED:reason</dt>
 <dd>Signals that the move just given by the client was rejected by the server.
     A good client should be able to avoid this messages. The reason is for debug
     purposes.</dd>

 <dt>MOVE:a3,b4</dt>
 <dd>Gives the move of the other player.</dd>

 <dt>GAMEOVER:Win</dt>
 <dd>Alernatively will be GAMEOVER:Lose, depending on which happened. If the other
     player disconnected or quit this will be sent as the only message. If one player
     makes a move to win the server will first send the messages about the move just
     happened then immediatly following that will send this gameover message.</dd>
</dl>

