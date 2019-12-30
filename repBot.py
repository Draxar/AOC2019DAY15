from random import randrange

class repairBot:

  def __init__(self, x, y, width, lenght):
    self.x = x
    self.y = y
    self.lc = 1
    self.widgth = width
    self.lenght = lenght
    self.board = list ()
    for i in range(lenght):
      self.board.append(list())
      for j in range(width):
        self.board[-1].append(0)

  def processVideo(self, buf):
    ret = list()
    print(buf[0])
    if buf[0] == 0:
      #print wall in proper direction
      if self.lc == 1: #N
        ret.append(self.x)
        ret.append(self.y-1)
        ret.append(1)
        self.board[self.y-1][self.x]=1
      elif self.lc == 2: #S
        ret.append(self.x)
        ret.append(self.y+1)
        self.board[self.y+1][self.x]=1
        ret.append(1)
      elif self.lc == 3: #W
        ret.append(self.x-1)
        ret.append(self.y)
        ret.append(1)
        self.board[self.y][self.x-1]=1
      elif self.lc == 4: #E
        ret.append(self.x+1)
        ret.append(self.y)
        ret.append(1)
        self.board[self.y][self.x+1]=1
    if buf[0] == 1 or buf[0] == 2:
      print(self.x)
      print(self.y)
      # blank last ball
      ret.append(self.x)
      ret.append(self.y)
      ret.append(0)
      self.board[self.y][self.x]=2 #seen
      #print ball in proper direction
      if self.lc == 1: #N
        self.y-=1
      elif self.lc == 2: #S
        self.y+=1
      elif self.lc == 3: #W
        self.x-=1
      elif self.lc == 4: #E
        self.x+=1
      ret.append(self.x)
      ret.append(self.y)
      ret.append(4)
    return ret

  def processAi(self, buf):
    # first AI "circle:
    if buf[0]==1:
      return [self.lc]
    if buf[0]==0:
      best, good = self.checkMoves()
      print(best)
      print(good)
      if len(best)>0:
        return [best[randrange(len(best))]]
      else:
        return [good[randrange(len(good))]]
    if buf[0]==2:
      return []#finish
    
  def checkMoves(self):
    best = list()
    good = list()
    if self.board[self.y-1][self.x] == 2:
      good.append(1)
    if self.board[self.y-1][self.x] == 0:
      best.append(1)

    if self.board[self.y+1][self.x] == 2:
      good.append(2)
    if self.board[self.y+1][self.x] == 0:
      best.append(2)

    if self.board[self.y][self.x-1] == 2:
      good.append(3)
    if self.board[self.y][self.x-1] == 0:
      best.append(3)

    if self.board[self.y][self.x+1] == 2:
      good.append(4)
    if self.board[self.y][self.x+1] == 0:
      best.append(4)

    return best, good

  def process(self, buf):
    if len(buf) == 0:
      retv = list()
      retl = [self.lc]
    else:
      retv = self.processVideo(buf)
      retl = self.processAi(buf)
    return retv, retl