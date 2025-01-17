from .tensor import tensor
from .static_ops import identity

class conv:
  def __init__(self, filtershape, learningrate, numoffilters=1, activation=identity(), padding=False, stride=(1, 1), clip=False, inshape=None):
    self.learningrate, self.activation, self.padding, self.stride, self.numoffilters, self.clip = learningrate, activation, padding, stride, numoffilters, clip
    self.inshape = inshape

    self.filtershape = tuple([numoffilters]) + filtershape
    self.filter = tensor.uniform(-0.25, 0.25, self.filtershape)
    self.bias = tensor.zeros(self.filtershape[0])

    if inshape is not None:
      if len(inshape) == 2:
        inshape = tuple([self.filtershape[0]]) + inshape
      padding = (self.filtershape[1] - 1, self.filtershape[2] - 1) if padding == True else (0, 0)
      
      self.outshape = tuple([filtershape[0], int((inshape[1] - filtershape[1] + padding[0] + 1) / self.stride[0]), int((inshape[2] - filtershape[2] + padding[1] + 1) / self.stride[1])])
      self.out = tensor.zeros(self.outshape)

  def __copy__(self):
    return type(self)(self.filtershape, self.learningrate, self.activation, self.padding, self.stride, self.inshape)

  def __repr__(self):
    return 'conv(inshape=' + str(self.inshape) + ', outshape=' + str(self.outshape) + ', filtershape=' + str(self.filtershape) + ', learningrate=' + str(self.learningrate) + ', activation=' + str(self.activation) + ', padding=' + str(self.padding) + ', stride=' + str(self.stride) + ')'

  def modelinit(self, inshape):
    self.inshape = inshape
    if len(inshape) == 2:
      inshape = tuple([self.numoffilters]) + inshape
    if self.padding == True:
      inshape = (inshape[0], inshape[1] + self.filtershape[1] - 1, inshape[2] + self.filtershape[2] - 1)

    self.outshape = tuple([self.numoffilters, int((inshape[1] - self.filtershape[1] + 1) / self.stride[0]), int((inshape[2] - self.filtershape[2] + 1) / self.stride[1])])
    self.out = tensor.zeros(self.outshape)

    return self.outshape

  def forward(self, input):
    self.input = input
    if(len(input.shape) == 2):
      self.input = self.input * tensor.ones((self.filtershape[0], self.input.shape[0], self.input.shape[1]))
    if (self.padding == True):
      self.input = tensor.pad(self.input, int((len(self.filter[0]) - 1) / 2), mode='constant')[1 : self.filtershape[0] + 1]

    for i in range(0, self.outshape[1], self.stride[0]):
      for j in range(0, self.outshape[2], self.stride[1]):
        self.out[:, i, j] = tensor.sum(self.input[:, i : i + self.filtershape[1], j : j + self.filtershape[2]] * self.filter, axis=(1, 2))

    self.out += self.bias[:, tensor.newaxis, tensor.newaxis]
    self.derivative = self.activation.backward(self.out)
    self.out = self.activation.forward(self.out)
    return self.out
  
  def backward(self, outError):
    filterΔ = tensor.zeros(self.filtershape)
    
    outGradient = outError * self.derivative

    for i in range(0, self.outshape[1], self.stride[0]):
      for j in range(0, self.outshape[2], self.stride[1]):
        filterΔ += self.input[:, i : i + self.filtershape[1], j : j + self.filtershape[2]] * outGradient[:, i, j][:, tensor.newaxis, tensor.newaxis]
    
    self.bias += tensor.sum(outGradient, axis=(1, 2)) * self.learningrate
    self.filter += filterΔ * self.learningrate

    if self.clip: self.bias, self.filter = tensor.clip(self.bias, -1, 1), tensor.clip(self.filter, -1, 1)

    # in Error
    rotfilter = tensor.rot90(self.filter, 2)
    PaddedError = tensor.pad(outError, self.filtershape[1] - 1, mode='constant')[self.filtershape[1] - 1 : self.filtershape[0] + self.filtershape[1] - 1, :, :]
    
    self.inError = tensor.zeros(self.inshape)
    if len(self.inError.shape) == 3:
      for i in range(int(self.inshape[1] / self.stride[0])):
        for j in range(int(self.inshape[2] / self.stride[1])):
         self.inError[:, i * self.stride[0], j * self.stride[1]] = tensor.sum(rotfilter * PaddedError[:, i:i + self.filtershape[1], j:j + self.filtershape[2]], axis=(1, 2))
       
    elif len(self.inError.shape) == 2:
      for i in range(int(self.inshape[0] / self.stride[0])):
        for j in range(int(self.inshape[1] / self.stride[1])):
         self.inError[i * self.stride[0], j * self.stride[1]] = tensor.sum(rotfilter * PaddedError[:, i:i + self.filtershape[1], j:j + self.filtershape[2]])

    return self.inError