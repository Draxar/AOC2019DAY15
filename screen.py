import os
clearSCR = lambda: os.system('clear')

class screen:
  tiles = {
    0 : " ",
    1 : "█",
    2 : "#",
    3 : "_",
    4 : "o",
    5 : "."
  }
  def __init__(self, width, lenght):
    self.score = 0
    self.width = width
    self.lenght = lenght
    self.board = list ()
    for i in range(lenght):
      self.board.append(list())
      for j in range(width):
        self.board[-1].append(0)

  def printScrean(self):
    clearSCR()
    for i in range(self.lenght):
      for j in range(self.width):
        print(self.tiles[self.board[i][j]], end = '')
      print("")

  def inp(self, inp):
    global palPlace
    global balPlace
    itr = 0
    while itr + 3 <= len(inp):
      if inp[itr] == -1 and inp[itr+1] == 0:
        self.score = inp[itr+2]
      else:
        self.board[inp[itr+1]][inp[itr]] = inp[itr+2]
        if inp[itr+2] == 3:
          palPlace = inp[itr]
        if inp[itr+2] == 4:
          balPlace = inp[itr]
      itr += 3
  
  def count(self, field):
    ret = 0
    for i in range(self.lenght):
      for j in range(self.width):
        if self.board[i][j] == field:
          ret += 1
    return ret
