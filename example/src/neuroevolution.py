from .tensor import tensor
from copy import copy

class neuroevolution:
  def __init__(self, inshape, outshape, PopulationSize, model):
    self.inshape, self.outshape, self.PopulationSize = inshape, outshape, PopulationSize
    
    self.model = tensor.zeros((PopulationSize, len(model)), dtype=object)
    for i in range(PopulationSize):
      inshape = self.inshape
      for j in range(len(model)):
        self.model[i, j] = copy(model[j])
        inshape = self.model[i, j].modelinit(inshape)

  def forwardmulti(self, input):
    out = tensor.zeros((self.PopulationSize, self.outshape))
    for i in range(self.PopulationSize):
      hid = input
      for j in range(self.model.shape[1]):
        hid = self.model[i, j].forward(hid)
      out[i] = hid
    return out

  def forwardsingle(self, input, Player):
    out = tensor.zeros(self.outshape)
    for j in range(self.model.shape[1]):
      input = self.model[Player, j].forward(input)
    return input

  def mutate(self, FavorablePlayer):
    Favorablemodel = self.model[FavorablePlayer]

    for i in range(self.model.shape[1]):
      self.model[0, i].weights = Favorablemodel[i].weights
      self.model[0, i].biases = Favorablemodel[i].biases

    for i in range(1, self.PopulationSize):
      for j in range(self.model.shape[1]):
        self.model[i, j].weights = Favorablemodel[j].weights
        self.model[i, j].biases = Favorablemodel[j].biases

        self.model[i, j].weights *= tensor.random.choice([0, 1], self.model[i, j].weights.shape, p=[self.model[i, j].learningrate, 1 - self.model[i, j].learningrate])
        self.model[i, j].weights = tensor.where(self.model[i, j].weights == 0, tensor.uniform(-1, 1, self.model[i, j].weights.shape), self.model[i, j].weights)

        self.model[i, j].biases *= tensor.random.choice([0, 1], self.model[i, j].biases.shape, p=[self.model[i, j].learningrate, 1 - self.model[i, j].learningrate])
        self.model[i, j].biases = tensor.where(self.model[i, j].biases == 0, tensor.uniform(-1, 1, self.model[i, j].biases.shape), self.model[i, j].biases)