memorySize = 5000

class compu:
  def __init__(self, prog, inp):
    global memorySize
    self.program = list(prog)
    self.inputBuffer = list(inp)
    self.outputBuffer = list()
    self.state = 1 #1=new, 2=ended, 3=paused
    self.itr = 0
    self.relativeBase = 0
    while len(self.program) < memorySize:
      self.program.append(0)

  def addInput(self, inp):
    self.inputBuffer.extend(inp)

  def parseCode(self, code):
    p3 = int(code / 10000)
    code = code % 10000
    p2 = int(code / 1000)
    code = code % 1000
    p1 = int(code / 100)
    code = code % 100
    return p1, p2, p3, code

  #parse and process opcode
  def processCode(self, itr):
    code = self.program[itr]
    p1, p2, p3, code = self.parseCode(code)
    if code == 99:
      return "quit"

    # process code
    # 1 parameter
    if p1 == 1:
      ind1 = itr+1
    elif p1 == 2:
      ind1 = self.program[itr+1] + self.relativeBase
    else:
      ind1 = self.program[itr+1]
  
    if code == 3:
      if not self.inputBuffer:
        return "pause"
      self.program[ind1] = self.inputBuffer.pop(0)
      return 2

    if code == 4:
      self.outputBuffer.append(self.program[ind1])
      return 2

    if code == 9:
      self.relativeBase += self.program[ind1]
      return 2
    # 2 parameters  
    if p2 == 1:
      ind2 = itr+2
    elif p2 == 2:
      ind2 = self.program[itr+2] + self.relativeBase
    else:
      ind2 = self.program[itr+2]
    if code == 5:
      if self.program[ind1] != 0:
        return self.program[ind2] - itr
      else:
        return 3
    if code == 6:
      if self.program[ind1] == 0:
        return self.program[ind2] - itr
      else:
        return 3 
    # 3 parameters  
    if p3 == 1:
      ind3 = itr+3
    elif p3 == 2:
      ind3 = self.program[itr+3] + self.relativeBase
    else:
      ind3 = self.program[itr+3]
    if code == 1:
      self.program[ind3] = self.program[ind1] + self.program[ind2]
      return 4
    if code == 2:
      self.program[ind3] = self.program[ind1] * self.program[ind2]
      return 4
    if code == 7:
      if self.program[ind1] < self.program[ind2]:
        self.program[ind3] = 1
        return 4
      self.program[ind3] = 0
      return 4
    if code == 8:
      if self.program[ind1] == self.program[ind2]:
        self.program[ind3] = 1
        return 4
      self.program[ind3] = 0
      return 4

    print("BAD CODE:")
    print(str(code))
    return "quit"

  # prepere and process program
  def ProcessProgram(self):
    #prep program
    move = 0
    process = True
    self.outputBuffer = list()
    #process program
    while process:
      move = self.processCode(self.itr)
      if move == "quit":
        self.state = 2
        self.itr = 0
        process = False
      elif move == "pause":
        self.state = 3
        process = False
      else :
        self.itr += move
    return self.state, self.outputBuffer
