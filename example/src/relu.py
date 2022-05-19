import numpy as np

class relu:
  def __repr__(self):
    return 'relu()'

  def forward(self, input):
    output = np.maximum(0, input)
    return output

  def backward(self, input):
    equation = np.vectorize(self.equationforderivative, otypes=[float])
    return equation(input)
    
  def equationforderivative(self, input):
    return 0 if input <= 0 else 1