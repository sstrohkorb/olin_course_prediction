from parse_course_data import *

import numpy as np
from sklearn import datasets
from sklearn import linear_model



def make_training_data(x_vector, y_vector, test_size):
  # np.random.seed(0)
  indices = np.random.permutation(len(x_vector))
  x_train = [x_vector[i] for i in indices[:-test_size]]
  y_train = [y_vector[i] for i in indices[:-test_size]]
  x_test = [x_vector[i] for i in indices[-test_size:]]
  y_test = [y_vector[i] for i in indices[-test_size:]]

  return [x_train, y_train, x_test, y_test]

def create_course_enrollment_data(students, courses, professors, desired_course):
  course_list = []
  for course in courses:
    course_list.append(courses[course].course_number)
    course_list.sort()

  course_dict = {course_list[i]: i for i in range(len(course_list))}

  all_x_vectors = []
  all_y_values = []
  for student_id in students:
    x_vector = [0]*len(course_list)
    y_value = 0
    for course_offering in students[student_id].list_of_course_offerings:
      course_no = course_offering.course.course_number
      x_vector[course_dict[course_no]] = 1
      if course_no == desired_course:
        x_vector[course_dict[course_no]] = 0
        y_value = 1

    all_x_vectors.append(x_vector)
    all_y_values.append(y_value)

  return [all_x_vectors, all_y_values]

def make_logistic(all_x_vectors, all_y_values, test_size):

  # Select traning and testing data
  [x_train, y_train, x_test, y_test] = make_training_data(all_x_vectors, all_y_values, test_size)

  logistic = linear_model.LogisticRegression(C=1e5)
  logistic.fit(x_train, y_train)
  return [logistic, x_test, y_test]

def test_logistic(logistic, x_test, y_test):
  num_correct = 0
  for i in range(len(x_test)):
    predicted = logistic.predict(x_test[i])
    if predicted == y_test[i]:
      num_correct += 1
  percent_correct = float(num_correct)/float(len(x_test))
  # print "%f correct" %percent_correct
  return percent_correct



[students, courses, professors] = get_course_data('../anonymizeddata_UpToFall2013.csv')

course_list = ['ENGR3420', 'ENGR2250', 'ENGR2510', 'ENGR3320', 'MTH3120', 'SCI2320', 'ENGR3370', 'AHSE1122', 'SCI2199', 'ENGR3380']
course_names = ['AnalDig', 'UOCD', 'SoftDes', 'MechSolids', 'PDEs', 'OChem', 'Controls', 'Wired', 'Relativity', 'DFM']
for course, course_name in zip(course_list, course_names):
  [x_vector, y_vector] = create_course_enrollment_data(students, courses, professors, course)

  test_results = []
  for i in range(100):
    [logistic, x_test, y_test] = make_logistic(x_vector, y_vector, 10)
    test_results.append(test_logistic(logistic, x_test, y_test))

  print '%s: %s - %f' %(course, course_name, sum(test_results)/len(test_results))
