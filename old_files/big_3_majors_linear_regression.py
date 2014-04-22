from parse_course_data import *
import enrollment_simulation as sim

import numpy as np
from sklearn import datasets
from sklearn import linear_model
import matplotlib.pyplot as plt
from random import *


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

  for student_id, student in students.items():
    # make sure that the student made it to the desired semester
    for student_semester, semester_course_offerings in enumerate(student.list_of_course_offerings):
      for course_offering in semester_course_offerings:
        if student_semester == desired_semester:
          student_made_it_to_desired_semester += 1
          break
    # then determine the rest
    if student_made_it_to_desired_semester: 
      total_eligible_to_take_course += 1
      for student_semester, semester_course_offerings in enumerate(student.list_of_course_offerings):
        for course_offering in semester_course_offerings:
          course_no = course_offering.course.course_number
          if course_no == desired_course:
            if student_semester <= current_semester:
              num_who_took_course_previously += 1
            if student_semester == desired_semester:
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

  # sorted_probabilities = sorted(zip(prob, y_test), key=lambda x:x[0][1], reverse=True)

  # prob started giving me a length 1 vector for some reason =/
  sorted_probabilities = sorted(zip(prob, y_test), key=lambda x:x[0][0])

  probs, y_values = zip(*sorted_probabilities)
  
  area = compute_ROC(y_values)
  
  return area

def compute_ROC(y_values):
  """given true y values sorted by assigned probability, create ROC and compute area underneath
  """
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
      false_pos.append(0)
    else: 
      false_pos.append(false_pos_total/total_neg)

  # area under the ROC curve
  area = area_under_curve(false_pos, true_pos)

  return area
  

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

def get_sim_data(num_iter=100, sim_courses=None, start_sem='0607FA', end_sem='1314FA', students=None, courses=None, professors=None, semesters=None, all_courses_list=None):
  """
  predict course enrollment and return predictions and ROC values
  parameters:
    num_iter: (int) number of times logistic is made for a given case when determining
      the best c value
    sim_courses: (list of course numbers) courses to simulate. run spring 2014 courses if none provided
  return value:
    dictionary mapping course number to (tot_enrolled, avg_roc_arith, sem_enr, max_rocs)
  """
  print 'predicting %s - %s'%(start_sem, end_sem)
  course_list = sim_courses or ['ENGR2320', 'MTH2199B', 'ENGR3499A', 'ENGR3599', 'AHSE4190', 'MTH2199A', 'MTH2199C', 
    'ENGR3499', 'ENGR3299', 'ENGR3810', 'MTH2140', 'SCI2214', 'ENGR1330', 'ENGR2350', 'MTH3170', 'MTH2188A', 
    'ENGR4190', 'AHSE3190', 'ENGR2599', 'AHSE3199', 'ENGR2410', 'MTH2199', 'ENGR2141', 'ENGR3370', 'SCI2320', 
    'AHSE0112', 'ENGR2510', 'SCI1410', 'ENGR3525', 'SUST3301', 'ENGR4290', 'SCI3320', 'ENGR3620', 'ENGR3820', 
    'ENGR2330', 'SCI2130B', 'ENGR3199', 'ENGR3399', 'SCI1310', 'MTH3120', 'AHSE4590', 'SCI1210', 'ENGR2199C', 
    'ENGR3392', 'AHSE1500', 'ENGR1121', 'SCI1130', 'ENGR3415', 'AHSE2199', 'AHSE2199B', 'AHSE2199A', 'SCI1199B', 
    'ENGR2210', 'ENGR2250', 'ENGR2420', 'ENGR3260', 'SCI2140']


  if not students or not courses or not all_courses_list:
    students, courses, professors, semesters, all_courses_list = initialize_data()

  current_students, past_students = sim.get_testing_sets(students, end_sem)
  c_vals = np.logspace(-1, 4, num=15)

  data = {course: sim.simulate_course(students, all_courses_list, professors, course, current_students, c_vals, num_iter=num_iter) for course in course_list}
  return data

def test_sweep_c(course_list, course_names, course_semester, current_semesters, c_values, starting_semester):
  """
  This is a testing function that sweeps through a range of c values and plots the results
  """
  students, courses, professors, semesters, all_courses_list = initialize_data()

  all_courses_averaged_results = []
  for course, course_name, desired_semester, current_semester in zip(course_list, course_names, course_semester, current_semesters):
    [x_vector, y_vector] = create_course_enrollment_data(students, all_courses_list, professors, starting_semester, course, current_semester, desired_semester, ending_semester='1314FA')
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
      print "Our algorithm: %.4f" % (averaged_result)
    all_courses_averaged_results.append(averaged_results)

  for i in range(len(course_list)):
    label = '%s: %s-%s' %(course_names[i], current_semesters[i], course_semester[i])
    plt.plot(c_values, all_courses_averaged_results[i], label=label)
  plt.xscale('log')
  plt.legend()
  plt.show()

def test_sweep_c_for_course(start_sem='0607FA', end_sem='1314FA', students=None, courses=None, professors=None, semesters=None, all_courses_list=None):
  print 'predicting %s - %s'%(start_sem, end_sem)
  course_list = ["SCI1210", "ENGR2210", "SCI1410", "MTH2130", "ENGR2510", "SCI1130", "ENGR2410", "MTH2110", "ENGR3410", 
               "ENGR2320", "ENGR2340", "ENGR2350", "ENGR3330", "ENGR2420", "ENGR3220", "ENGR3310", "ENGR3260", 
               "ENGR3390", "ENGR3420", "AHSE2110"]

  if not students or not courses or not all_courses_list:
    students, courses, professors, semesters, all_courses_list = initialize_data()

  current_students, past_students = sim.get_testing_sets(students, end_sem)
  c_vals = np.logspace(-1, 4, num=15)
  best_c_vals = []

  for course in course_list:
    best_c_vals.extend(sim.sweep_c_for_course(students, all_courses_list, professors, course, current_students, c_vals=c_vals, start_sem=start_sem, end_sem=end_sem))



if __name__ == "__main__":

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

  # n = 1
  # course_list = ['ENGR3525']*n
  # course_names = ['SoftSys']*n
  # course_semester = [3] # SO2
  # current_semesters = [2] # SO1
  # c_values = np.logspace(-1, 4, num=10)
  # starting_semester = '0203FA'

  # test_sweep_c(course_list, course_names, course_semester, current_semesters, c_values, starting_semester)

  # run_sim('test.csv', num_iter=3, sim_courses=['ENGR3420'])
  students, courses, professors, semesters, all_courses_list = initialize_data()
  all_course_numbers = [x[0] for x in all_courses_list]

  test_sweep_c_for_course()

  # start_sems = ['0203FA','0203SP', '0304FA','0304SP', '0405FA','0405SP', '0506FA','0506SP', '0607FA','0607SP', '0708FA','0708SP', '0809FA', '0809SP']
  # end_sems = ['0708FA', '0708SP', '0809FA', '0809SP', '0910FA', '0910SP', '1011FA', '1011SP', '1112FA', '1112SP', '1213FA', '1213SP', '1314FA', '1314SP']
  # start_sems = ['0506FA','0506SP', '0607FA','0607SP', '0708FA','0708SP', '0809FA', '0809SP']
  # end_sems = ['1011SP', '1112FA', '1112SP', '1213FA', '1213SP', '1314FA', '1314SP']

  # for start, end in zip(reversed(start_sems), reversed(end_sems)):
  #   filename = 'results/simulate_%s_%s.csv'%(start, end)
  #   print 'simulating %s - %s'%(start, end)
  #   try:
  #     run_sim(filename, num_iter=50, sim_courses=all_course_numbers, start_sem=start, end_sem=end, students=students, courses=courses, professors=professors, semesters=semesters, all_courses_list=all_courses_list )
  #   except:
  #     print 'simulation failed: %s - %s'%(start, end)

  # start_sems = ['0405FA']
  # end_sems = ['0910FA']
  # for start, end in zip(start_sems, end_sems):
  #   filename = 'test.csv'
  #   print 'simulating %s - %s'%(start, end)
  #   run_sim(filename, num_iter=3, sim_courses=['ENGR3525'], start_sem=start, end_sem=end, students=students, courses=courses, professors=professors, semesters=semesters, all_courses_list=all_courses_list )





