from Activation import *
from NN import NN
import numpy as np

def SingleHeadSelfAttention(Input):
  Key = Input
  Query = Input
  Value = Input

def MultiHeadSelfAttention(Input, NumOfHeads):
  InToKey = NN(InputSize=Input.shape[1], OutSize=(Input.shape[1] * NumOfHeads), Activation='Identity', LearningRate=0)
  InToQuery = NN(InputSize=Input.shape[1], OutSize=(Input.shape[1] * NumOfHeads), Activation='Identity', LearningRate=0)
  InToValue = NN(InputSize=Input.shape[1], OutSize=(Input.shape[1] * NumOfHeads), Activation='Identity', LearningRate=0)
  Key = np.zeros((Input.shape[0], Input.shape[1] * NumOfHeads))
  Query = np.zeros((Input.shape[0], Input.shape[1] * NumOfHeads))
  Value = np.zeros((Input.shape[0], Input.shape[1] * NumOfHeads))
  for i in range(Input.shape[0]):
    Key[i, :] = InToKey.ForwardProp(Input[i, :])
    Query[i, :] = InToQuery.ForwardProp(Input[i, :])
    Value[i, :] = InToValue.ForwardProp(Input[i, :])

  Key /= Input.shape[1] ** 0.25
  Query /= Input.shape[1] ** 0.25
  Value /= Input.shape[1] ** 0.25

  # Key = Key.reshape((NumOfHeads, 2, 3))
  # Query = Query.reshape((NumOfHeads, 2, 3))
  # Value = Value.reshape((NumOfHeads, 2, 3))
  # Weights = np.zeros((NumOfHeads, 2, 2))
  
  Weights = np.dot(Key, np.transpose(Query))

  Weights = ApplyActivation(Weights, "StableSoftmax")
  print(Weights)
  # return np.dot(Weights, Value)

'''
class Transformer:
  def __init__(self, Heads, InputShape):
    self.ToKey = np.random.uniform(-np.sqrt(1 / InputShape), np.sqrt(1 / InputShape), (InputShape, InputShape))
    self.ToQuery = np.random.uniform(-np.sqrt(1 / InputShape), np.sqrt(1 / InputShape), (InputShape, InputShape))
    self.ToValue = np.random.uniform(-np.sqrt(1 / InputShape), np.sqrt(1 / InputShape), (InputShape, InputShape))
    self.UnifyHeads = np.random.uniform(-np.sqrt(1 / InputShape), np.sqrt(1 / InputShape), (InputShape * Heads, InputShape))
'''

Input = np.array([[1, 0, 0], [0, 0, 1]])
# x = np.array([1, 0, 0, 0, 0, 1])
# Heads = 2
# print(x.reshape((Heads,int(len(x)/Heads))))
print(SelfAttention(Input, 1))