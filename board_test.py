# Board testing
import chess

try:
  board = chess.Board() # creating board
  print(board.unicode()) # print board
  # pushing some moves
  board.push_san("e4")
  board.push_san("e5")
  board.push_san("Qh5")
  board.push_san("Nc6")
  board.push_san("Bc4")
  board.push_san("Nf6")
  board.push_san("Qxf7")
  
  print(board.unicode()) # print board
  assert board.is_checkmate() # asserting about checkmate
 
except:
   raise 0
