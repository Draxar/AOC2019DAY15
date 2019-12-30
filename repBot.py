from random import randrange

class repairBot:

  def __init__(self, x, y, width, lenght):
    self.vout = list()
    self.current = list()
    self.nexti = list()
    self.lastWasOO = False
    self.curIsOO = False
    self.minRoad = 9999999999999
    self.roadList = [1]
    self.x = x
    self.y = y
    self.ox = -1
    self.oy = -1
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
      # blank last ball
      ret.append(self.x)
      ret.append(self.y)
      if self.lastWasOO == False:
        if self.curIsOO == True:
          self.curIsOO = False
          self.lastWasOO == True
        ret.append(5)
      else:
        self.lastWasOO == True
        ret.append(2)
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
    if buf[0]==0:
      if len(self.roadList) == 0:
        return []
      self.roadList.pop()
    if buf[0]==2:
      self.ox = self.x
      self.oy = self.y
      #wait = input("PRESS ENTER TO CONTINUE.")
      self.curIsOO = True
      if self.minRoad > len(self.roadList):
        self.minRoad = len(self.roadList)
    best = self.checkMoves()
    if len(best)>0:
      self.lc = best.pop(randrange(len(best)))
      self.roadList.append(self.lc)
    else:
      self.lc = self.retu()
      if self.lc == []:
        return []
    return [self.lc]
    
  def retu(self):
    if len(self.roadList) == 0:
      return []
    ret = self.roadList.pop()
    if ret == 1 or ret == 3:
      ret += 1
    else:
      ret -= 1
    #wait = input("PRESS ENTER TO CONTINUE.")
    return ret
    

    
  def checkMoves(self, mode = 0):
    best = list()
    if self.board[self.y-1][self.x] == mode:
      best.append(1)
    if self.board[self.y+1][self.x] == mode:
      best.append(2)
    if self.board[self.y][self.x-1] == mode:
      best.append(3)
    if self.board[self.y][self.x+1] == mode:
      best.append(4)

    return best

  def process(self, buf):
    if len(buf) == 0:
      retv = list()
      retl = [self.lc]
    else:
      retv = self.processVideo(buf)
      retl = self.processAi(buf)
    return retv, retl

  def oxygenize(self, coord):
    #check if not already processed

    self.board[coord[1]][coord[0]] = 6
    self.vout.append(coord[0])
    self.vout.append(coord[1])
    self.vout.append(6)
    if self.board[coord[1]-1][coord[0]] == 2:
      self.nexti.append([coord[0],coord[1]-1])
    if self.board[coord[1]+1][coord[0]] == 2:
      self.nexti.append([coord[0],coord[1]+1])
    if self.board[coord[1]][coord[0]-1] == 2:
      self.nexti.append([coord[0]-1,coord[1]])
    if self.board[coord[1]][coord[0]+1] == 2:
      self.nexti.append([coord[0]+1,coord[1]])

    
  def reoxygenizationTime(self):
    self.vout=list()
    for c in self.current:
      self.oxygenize(c)
    self.current = self.nexti
    self.nexti = list()
    return self.vout

    