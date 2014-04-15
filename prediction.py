def test_logistic_binary(logistic, x_test, y_test):
  """ Tests a given logisitc based on the testing data provided and checks its correctness by 
      seeing what percentage correctness the logistic guesses right, whether a student will take
      a given course or not
  """
  num_correct = 0
  for i in range(len(x_test)):
    predicted = logistic.predict(x_test[i])
    if predicted == y_test[i]:
      num_correct += 1
  percent_correct = float(num_correct)/float(len(x_test))
  # print "%f correct" %percent_correct
  return percent_correct