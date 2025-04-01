'''Exceptions.'''

class M3Exception(Exception):
  '''Generic exception encapsulator.'''
  def __init__(self, message):
    super().__init__(message)
