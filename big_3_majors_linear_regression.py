from parse_course_data import *

import numpy as np
from sklearn import datasets
from sklearn import linear_model
import matplotlib.pyplot as plt
from random import *


def make_semesters_dict():
  start = 2
  end = 14
  semesters = {}
  for i in range((end - start)):
    temp_start = str(start + i)
    temp_end = str(start + i + 1)
    if len(temp_start) == 1:
      temp_start = '0' + temp_start
    if len(temp_end) == 1:
      temp_end = '0' + temp_end
    sem_fa = temp_start + temp_end + 'FA'
    sem_sp = temp_start + temp_end + 'SP' 
    semesters[sem_fa] = i * 2
    semesters[sem_sp] = i * 2 + 1
  return semesters


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

def freuqency_based_prediction_strength(students, courses, professors, desired_course, current_semester, desired_semester):
  """ Determines a baseline prediction strength based on how many students have taken the course 
      in that semester as to provide a comparison for how good our model actually is
  """

  # TODO: Add input for the starting semester

  total_eligible_to_take_course = 0
  total_not_taken_course_before = 0
  num_who_took_course_previously = 0
  num_who_took_course_during_desired_semester = 0
  student_made_it_to_desired_semester = 0

  for student_id in students:
    # make sure that the student made it to the desired semester 
    for course_offering in students[student_id].list_of_course_offerings:
      if course_offering.student_semester_no == desired_semester:
        student_made_it_to_desired_semester += 1
        break
    # then determine the rest
    if student_made_it_to_desired_semester: 
      total_eligible_to_take_course += 1
      for course_offering in students[student_id].list_of_course_offerings:
        course_no = course_offering.course.course_number
        if course_no == desired_course:
          if course_offering.student_semester_no <= current_semester:
            num_who_took_course_previously += 1
          if course_offering.student_semester_no == desired_semester:
            num_who_took_course_during_desired_semester += 1

  total_not_taken_course_before = total_eligible_to_take_course - num_who_took_course_previously

  if total_not_taken_course_before == 0:
    frequency_taken_course = 0
  else: 
    frequency_taken_course = float(num_who_took_course_during_desired_semester)/float(total_not_taken_course_before)
  
  # developing the 'mock' test data based on the frequency
  y_values = []
  for i in range(1000):
    random_selection = float(randint(1,100))/100.0
    # the case that the 'mock' student did not take the course
    if random_selection > frequency_taken_course:
      y_values.append(0)
    else: 
      y_values.append(1)

  area = compute_ROC(y_values)
  
  return area

# TODO: add major into the x_values, state assumptions being made (switching majors with the
#       engineering concentration), and choose the majors we want to include based on #
def create_course_enrollment_data(students, courses, professors, starting_semester, desired_course, current_semester, desired_semester):
  """ Setup the x and y vectors that contain all of the data that the model will take in based
      on the enrollment data that is input. 
      all_x_vectors represents the inputs to the linear regression model
      all_y_values represents the outputs to the linear regression model
  """

  course_list = []
  for course in courses:
    course_list.append(course[0])

  course_dict = {course_list[i]: i for i in range(len(course_list))}
  major_dict = {'Undeclared': 0, 'Mechanical Engineering': 1, "Electr'l & Computer Engr": 2, 'Engineering': 3}

  all_x_vectors = []
  all_y_values = []

  for student_id in students:
    student = students[student_id]
    if student.final_semester < desired_semester:
      # student did not make it to desired_semester- discard student
      continue
    if semesters[student.first_semester] < semesters[starting_semester]:
      # if the student started at Olin before the input starting_semester, discard student
      continue

    num_courses = len(course_list)
    x_vector = [0]*(num_courses + len(major_dict))
    y_value = 0

    drop_student = False

    # Set major for current semester
    x_vector[num_courses + major_dict[student.major_history[current_semester]]] = 1
    
    for course_offering in student.list_of_course_offerings:
      course_no = course_offering.course.course_number
      x_vector[course_dict[course_no]] = 1

      # don't include courses that have had less than 100 students enrolled in them (ever)
      if course_offering.course.total_number_of_students < 100:
        x_vector[course_dict[course_no]] = 0

      # designate the students that actually did take the desired course during the desired semester
      elif course_no == desired_course and course_offering.student_semester_no == desired_semester:
        x_vector[course_dict[course_no]] = 0
        y_value = 1

      # if the course is in a semester beyond what we're considering, set the y value to 0
      # (not including the 'future' information in our calculations)
      elif course_offering.student_semester_no > current_semester:
        x_vector[course_dict[course_no]] = 0

      # if student has already taken class
      elif course_no == desired_course and course_offering.student_semester_no <= current_semester:
        drop_student = True 

    if drop_student:
      continue

    all_x_vectors.append(x_vector)
    all_y_values.append(y_value)

  return [all_x_vectors, all_y_values]

def make_logistic(all_x_vectors, all_y_values, test_size, c_value=1e5):
  """ Takes as input x vectors and their corresponding y values as well as the test size, makes 
      all of the training and testing data and makes a linear regression logistic
  """

  # Select traning and testing data
  [x_train, y_train, x_test, y_test] = make_training_data(all_x_vectors, all_y_values, test_size)

  logistic = linear_model.LogisticRegression(C=c_value)
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

  y_values = []
  for (prob, y_value) in sorted_probabilities:
    y_values.append(y_value)
  
  area = compute_ROC(y_values)
  
  return area

def compute_ROC(y_values):

  true_pos = []
  false_pos = []
  true_pos_total = 0
  false_pos_total = 0
  total_pos = sum(y_values)
  total_neg = len(y_values) - total_pos
  for y_value in y_values:
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

def prediction_strength_for_a_course(x_vector, y_vector, all_courses_list, number_of_iterations, c_value):
  """ Determine prediction strength for a course based on the area under the ROC curve and also
      determine what the highested weighted courses are for a given course 
  """
  #test_results = []
  ROC_results = []
  test_size = int(len(x_vector)/2)
  for i in range(number_of_iterations):
    [logistic, x_test, y_test] = make_logistic(x_vector, y_vector, int(len(x_vector)/2), c_value)
    #test_results.append(test_logistic_binary(logistic, x_test, y_test))
    ROC_results.append(compute_ROC_for_logistic(logistic, x_test, y_test))

  actual_result = sum(ROC_results)/len(ROC_results)
  
  # Determine highly weighted courses
  highly_weighted_courses = determine_highest_weighted_courses(logistic, all_courses_list, 6)
  temp_str = ""
  for correlation, course_info in highly_weighted_courses:
    if correlation < 0:
      temp_str += "-"
    else: 
      temp_str += "+"
    temp_str += " " + course_info[1] + '\n'
  
  return [actual_result, temp_str]


def write_to_csv_file(filename, row_headings, data):
  f = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
  f.writerow(row_headings)
  for data_entry in data:
    f.writerow(data_entry)


if __name__ == "__main__":
  [students, courses, professors] = get_course_data('../course_enrollments_2002-2014spring_anonymized.csv')
  semesters = make_semesters_dict()
  spring_14_courses = ['ENGR2320', 'MTH2199B', 'ENGR3499A', 'ENGR3599', 'AHSE4190', 'MTH2199A', 'MTH2199C', 
    'ENGR3499', 'ENGR3299', 'ENGR3810', 'MTH2140', 'SCI2214', 'ENGR1330', 'ENGR2350', 'MTH3170', 'MTH2188A', 
    'ENGR4190', 'AHSE3190', 'ENGR2599', 'AHSE3199', 'ENGR2410', 'MTH2199', 'ENGR2141', 'ENGR3370', 'SCI2320', 
    'AHSE0112', 'ENGR2510', 'SCI1410', 'ENGR3525', 'SUST3301', 'ENGR4290', 'SCI3320', 'ENGR3620', 'ENGR3820', 
    'ENGR2330', 'SCI2130B', 'ENGR3199', 'ENGR3399', 'SCI1310', 'MTH3120', 'AHSE4590', 'SCI1210', 'ENGR2199C', 
    'ENGR3392', 'AHSE1500', 'ENGR1121', 'SCI1130', 'ENGR3415', 'AHSE2199', 'AHSE2199B', 'AHSE2199A', 'SCI1199B', 
    'ENGR2210', 'ENGR2250', 'ENGR2420', 'ENGR3260', 'SCI2140']
  all_courses_list = []
  for course in courses: 
    all_courses_list.append([courses[course].course_number, courses[course].title])

  #course_list = ['ENGR3420', 'ENGR2250', 'ENGR2510', 'ENGR3320', 'MTH3120', 'SCI2320', 'ENGR3370', 'SCI2199', 'ENGR3380']
  #course_names = ['AnalDig', 'UOCD', 'SoftDes', 'MechSolids', 'PDEs', 'OChem', 'Controls', 'Relativity', 'DFM']
  #course_semester = ['JR', 'SO', 'SO', 'SO', 'JR', 'SO', 'SR', 'SO', 'SR']

  #course_list = ['AHSE1100', 'ENGR3420', 'ENGR3380', 'ENGR2330', 'ENGR3370', 'ENGR3210', 'ENGR3220', 'SCI1210', 'ENGR3392', 'ENGR2510']
  #course_names = ['HistofTech', 'AnalDig', 'DFM', 'MechProto', 'Controls', 'Sustainable Design', 'HFID', 'ModBio', 'Robo2', 'SoftDes']
  #course_semester = ['FF', 'JR2', 'SR2', 'JR2', 'SR2', 'JR1', 'JR1', 'SR2', 'JR2', 'FR']
  #current_semesters = ['', 'JR1', 'SR1', 'JR1', 'SR1', 'SO2', 'SO2', 'SR1', 'JR1', 'FF']

  # num = 6
  # course_list = ['ENGR3220']*num
  # course_names = ['HFID']*num
  # course_semester = ['SR1']*num
  # current_semesters = ['FF', 'FR', 'SO1', 'SO2', 'JR1', 'JR2']

  n = 1
  course_list = ['ENGR3525']*n
  course_names = ['SoftSys']*n
  course_semester = [3] # SO2
  current_semesters = [2] # SO1
  c_values = np.logspace(-1, 4, num=10)
  starting_semester = '0203FA'

  all_courses_averaged_results = []
  for course, course_name, desired_semester, current_semester in zip(course_list, course_names, course_semester, current_semesters):
    [x_vector, y_vector] = create_course_enrollment_data(students, all_courses_list, professors, starting_semester, course, current_semester, desired_semester)
    frequency_baseline = freuqency_based_prediction_strength(students, all_courses_list, professors, course, current_semester, desired_semester)
    num_students_taken_course_ever = courses[course].total_number_of_students
    averaged_results = []
    for c_value in c_values:
      temp_list = []
      for i in range(3):
        [actual_result, description] = prediction_strength_for_a_course(x_vector, y_vector, all_courses_list, 20, c_value)
        temp_list.append(actual_result)
      averaged_result = sum(temp_list)/len(temp_list)
      averaged_results.append(averaged_result)
      print '%s: %s %s - %s' %(course_name, current_semester, desired_semester, c_value)
      #print "Total: " + str(num_students_taken_course_ever)
      #print "Baseline:      %.4f" % frequency_baseline
      #print description
      print "Our algorithm: %.4f" % (averaged_result)
    all_courses_averaged_results.append(averaged_results)

  for i in range(len(course_list)):
    label = '%s: %s-%s' %(course_names[i], current_semesters[i], course_semester[i])
    plt.plot(c_values, all_courses_averaged_results[i], label=label)
  plt.xscale('log')
  plt.legend()
  plt.show()


  row_headings = ["Course Number", "Course Title", "Actual Enrollment", "Predicted Enrollment", "ROC Value"]
  data = [
    ['ENGR2320', 'Mechanics of Solids & Structures', 30, 26, .94]
  ]
  filename = "results/SP14_enrollment_prediction.csv"
  write_to_csv_file(filename, row_headings, data)







