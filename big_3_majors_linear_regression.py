from parse_course_data import *

import numpy as np
from sklearn import datasets
from sklearn import linear_model
import matplotlib.pyplot as plt


def make_training_data(x_vector, y_vector, test_size):
  """ Takes as input all of the x values in a list and the y values in a list and then designates
      a certain number of them (test_size) as test cases and the rest as training data
  """
  # np.random.seed(0)
  indices = np.random.permutation(len(x_vector))
  x_train = [x_vector[i] for i in indices[:-test_size]]
  y_train = [y_vector[i] for i in indices[:-test_size]]
  x_test = [x_vector[i] for i in indices[-test_size:]]
  y_test = [y_vector[i] for i in indices[-test_size:]]

  return [x_train, y_train, x_test, y_test]

def create_course_enrollment_data(students, courses, professors, desired_course, desired_semester):
  """ Setup the x and y vectors that contain all of the data that the model will take in based
      on the enrollment data that is input. 
      all_x_vectors represents the inputs to the linear regression model
      all_y_values represents the outputs to the linear regression model
  """
  semesters = ['FF', 'FR', 'SO1', 'SO2', 'JR1', 'JR2', 'SR1', 'SR2']
  for i in range(len(semesters)):
    if semesters[i] == desired_semester:
      acceptable_semesters = semesters[:i]
      break

  course_list = []
  for course in courses:
    course_list.append(course[0])

  course_dict = {course_list[i]: i for i in range(len(course_list))}

  all_x_vectors = []
  all_y_values = []

  for student_id in students:
    x_vector = [0]*len(course_list)
    y_value = 0

    for course_offering in students[student_id].list_of_course_offerings:
      course_no = course_offering.course.course_number
      x_vector[course_dict[course_no]] = 1

      # don't include courses that have had less than 20 students enrolled in them (ever)
      if course_offering.course.total_number_of_students < 20:
        x_vector[course_dict[course_no]] = 0

      # designate the students that actually did take the desired course during the desired semester
      elif course_no == desired_course and course_offering.student_year == desired_semester:
        x_vector[course_dict[course_no]] = 0
        y_value = 1

      # if the course is in a semester beyond what we're considering, set the y value to 0
      # (not including the 'future' information in our calculations)
      elif course_offering.student_year not in acceptable_semesters:
        x_vector[course_dict[course_no]] = 0

    all_x_vectors.append(x_vector)
    all_y_values.append(y_value)

  return [all_x_vectors, all_y_values]

def make_logistic(all_x_vectors, all_y_values, test_size):
  """ Takes as input x vectors and their corresponding y values as well as the test size, makes 
      all of the training and testing data and makes a linear regression logistic
  """

  # Select traning and testing data
  [x_train, y_train, x_test, y_test] = make_training_data(all_x_vectors, all_y_values, test_size)

  logistic = linear_model.LogisticRegression(C=1e5)
  logistic.fit(x_train, y_train)
  return [logistic, x_test, y_test]

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

def area_under_curve(x_vals, y_vals):
  """ Given a set of x and y coordinates, calculates the area under the curve made by those
      points on the x-y axis
  """
  total_area = 0
  for i in range(len(x_vals) - 1):
    total_area += (x_vals[i+1] - x_vals[i]) * y_vals[i+1]
  return total_area

def compute_ROC_for_logistic(logistic, x_test, y_test):
  """ Computes the area under the ROC curve for a given logistic and training data. The ROC curve
      is represented by the false positives on the x axis and true positives on the y axis. 
  """
  prob = logistic.predict_proba(x_test)
  sorted_probabilities = sorted(zip(prob, y_test), key=lambda x:x[0][1], reverse=True)
  true_pos = []
  false_pos = []
  true_pos_total = 0
  false_pos_total = 0
  total_pos = sum(y_test)
  total_neg = len(y_test) - total_pos
  for (probabilities, y_value) in sorted_probabilities:
    if y_value == 1:
      true_pos_total += 1.0
    else: 
      false_pos_total += 1.0
    if total_pos == 0:
      true_pos.append(0)
    else: 
      true_pos.append(true_pos_total/total_pos)
    if total_neg == 0:
      true_neg.append(0)
    else: 
      false_pos.append(false_pos_total/total_neg)

  # area under the ROC curve
  area = area_under_curve(false_pos, true_pos)
  
  return area
  

def determine_highest_weighted_courses(logistic, all_courses_list, number_of_courses):
  """ Finds the classes with highest absolute value coefficients and determines whether 
      they're positive or negative
  """
  sorted_highly_weighted_courses = sorted(zip(logistic.coef_[0], all_courses_list), key=lambda x:abs(x[0]), reverse=True)
  return sorted_highly_weighted_courses[:number_of_courses]

def prediction_strength_for_a_course(course_number, course_name, course_semester, number_of_iterations, all_courses_list):
  """ Determine prediction strength for a course based on the area under the ROC curve and also
      determine what the highested weighted courses are for a given course 
  """
  [x_vector, y_vector] = create_course_enrollment_data(students, all_courses_list, professors, course, semester)
  #test_results = []
  ROC_results = []
  for i in range(number_of_iterations):
    [logistic, x_test, y_test] = make_logistic(x_vector, y_vector, 40)
    #test_results.append(test_logistic_binary(logistic, x_test, y_test))
    ROC_results.append(compute_ROC_for_logistic(logistic, x_test, y_test))

  print sum(ROC_results)/len(ROC_results)
  
  # Determine highly weighted courses
  highly_weighted_courses = determine_highest_weighted_courses(logistic, all_courses_list, 6)
  temp_str = ""
  for correlation, course_info in highly_weighted_courses:
    if correlation < 0:
      temp_str += "-"
    else: 
      temp_str += "+"
    temp_str += " " + course_info[1] + '\n'
  
  return temp_str


if __name__ == "__main__":
  [students, courses, professors] = get_course_data('../anonymizeddata_UpToFall2013.csv')
  all_courses_list = []
  for course in courses: 
    all_courses_list.append([courses[course].course_number, courses[course].title])

  #course_list = ['ENGR3420', 'ENGR2250', 'ENGR2510', 'ENGR3320', 'MTH3120', 'SCI2320', 'ENGR3370', 'SCI2199', 'ENGR3380']
  #course_names = ['AnalDig', 'UOCD', 'SoftDes', 'MechSolids', 'PDEs', 'OChem', 'Controls', 'Relativity', 'DFM']
  #course_semester = ['JR', 'SO', 'SO', 'SO', 'JR', 'SO', 'SR', 'SO', 'SR']

  course_list = ['AHSE1100', 'ENGR3420', 'ENGR3380', 'ENGR2330', 'ENGR3370', 'ENGR3210', 'ENGR3220', 'SCI1210', 'ENGR3392', 'ENGR2510']
  course_names = ['HistofTech', 'AnalDig', 'DFM', 'MechProto', 'Controls', 'Sustainable Design', 'HFID', 'ModBio', 'Robo2', 'SoftDes']
  course_semester = ['FF', 'JR2', 'SR2', 'JR2', 'SR2', 'JR1', 'JR1', 'SR2', 'JR2', 'FR']

  for course, course_name, semester in zip(course_list, course_names, course_semester):
    description = prediction_strength_for_a_course(course, course_name, semester, 50, all_courses_list)
    print '%s: %s' %(course_name, semester)
    print description
