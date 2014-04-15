from sklearn import linear_model

def make_logistic(x_train, y_train, c_value=1e5):
  """ Takes as input x vectors and their corresponding y values as well as the test size, makes 
      all of the training and testing data and makes a linear regression logistic
  """

  logistic = linear_model.LogisticRegression(C=c_value)
  logistic.fit(x_train, y_train)
  return logistic