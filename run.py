from make_train_test_data import *
from parse_course_data import *
from prediction import *
from store_simulation_data import * 
from analyze_predictions import *
from sklearn import linear_model

def initialize_input_data(enrollment_history_filepath='../course_enrollments_2002-2014spring_anonymized.csv', prereg_data_filepath="../pre_reg_survey_data/*"):
    [students, courses, professors] = get_course_data(enrollment_history_filepath)
    prereg_data = get_prereg_data(prereg_data_filepath)
    enter_prereg_data(courses, prereg_data)

    all_courses_list = []
    for course in courses: 
        all_courses_list.append([courses[course].course_number, courses[course].title])

    return students, courses, all_courses_list

def add_dummy_student(x_list, y_list):
    if x_list: 
      dummy_x = [0]*len(x_list[0])
      dummy_x[-1] = 1   # set the dummy feature to 1
      for i in range(2): x_list.append(dummy_x)
      y_list.append(1)
      y_list.append(0)
    # else: 
    #   for i in range(2): x_list.append([1])
    #   y_list.append(1)
    #   y_list.append(0)
    return x_list, y_list

def make_random_train_test(students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data):
    [x_matrix, y_values] = make_student_feature_data(students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data)
    [x_train, y_train, x_test, y_test] = make_random_training_data(x_matrix, y_values, len(y_values)/2)
    if add_dummy_data: 
      x_train, y_train = add_dummy_student(x_train, y_train)
      x_test, y_test = add_dummy_student(x_test, y_test)
    return [x_train, y_train, x_test, y_test]

def make_semester_specific_train_test(situation, students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data):
    current_students, past_students = get_current_and_past_students(students, ending_semester, current_semester)
    [x_train, y_train] = make_student_feature_data(situation, False, past_students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data)
    [x_test, y_test] = make_student_feature_data(situation, True, current_students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data)
    if add_dummy_data: 
      x_train, y_train = add_dummy_student(x_train, y_train)
      x_test, y_test = add_dummy_student(x_test, y_test)
    return [x_train, y_train, x_test, y_test]


def make_logistic(x_train, y_train, c_value=1e5):
  """ Takes as input x vectors and their corresponding y values as well as the test size, makes 
      all of the training and testing data and makes a linear regression logistic
  """
  logistic = linear_model.LogisticRegression(C=c_value)
  logistic.fit(x_train, y_train)
  return logistic

def predict_enrollment_for_one_course(students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data, number_of_models):
  all_train_test_data = []
  for i in range(number_of_models):
    train_test_data = make_semester_specific_train_test(i, students, courses, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester, predicting_for_semester, add_dummy_data)
    all_train_test_data.append(train_test_data)
    # If everyone has taken the class already 
  if len(train_test_data[2]) == 0:
    return [0]*number_of_models
  else: 
    all_predicted_enrollments = []
    for train_test_data in all_train_test_data:
      # train_test_data = [x_train, y_train, x_test, y_test]
      x_train = train_test_data[0]
      y_train = train_test_data[1]
      x_test = train_test_data[2]
      logistic = make_logistic(x_train, y_train, 1e3)
      predicted_enrollment = sum(predict_enrollment(logistic, x_test))
      all_predicted_enrollments.append(predicted_enrollment)
    return all_predicted_enrollments

if __name__ == '__main__':
    students, courses, all_courses_list = initialize_input_data()

    number_of_models = 5

    add_dummy_data = True # the Sarah's computer flag

    ending_semesters = ['0506SP', '0607FA','0607SP', '0708FA','0708SP', '0809FA', '0809SP', '0910FA', '0910SP', '1011FA', '1011SP', '1112FA', '1112SP', '1213FA', '1213SP', '1314FA', '1314SP']
    predicting_semesters = ending_semesters[9:]
    predicting_semesters.append('1415FA')

    # ending_semesters = ['0910SP', '1011FA', '1011SP', '1112FA', '1112SP', '1213FA', '1213SP', '1314FA', '1314SP']
    
    course_list = ["SCI1210", "ENGR2210", "SCI1410", "MTH2130", "ENGR2510", "SCI1130", "ENGR2410", "MTH2110", "ENGR3410", 
                   "ENGR2320", "ENGR2340", "ENGR2350", "ENGR3330", "ENGR2420", "ENGR3220", "ENGR3310", "ENGR3260", 
                   "ENGR3390", "ENGR3420", "AHSE2110"]
    # course_list = ["SCI1210", "ENGR2210", "SCI1410"]
    # course_list = ["SCI1210"]

    predicted_data = [{} for x in range(number_of_models)]
    for i in range(len(course_list)):
      print course_list[i]
      all_semesters_predicted_enrollments = [[] for x in range(number_of_models)]

      for j in range(len(ending_semesters) - 8):
        total_course_enrollments = [0]*number_of_models
        for k in range(7):
          all_predicted_enrollments_for_one_course = predict_enrollment_for_one_course(students, courses, all_courses_list, course_list[i], k, k+1, ending_semesters[j], ending_semesters[j + 8], predicting_semesters[j], add_dummy_data, number_of_models)
          for x in range(number_of_models):
            total_course_enrollments[x] += all_predicted_enrollments_for_one_course[x]
        
        for x in range(number_of_models):
          all_semesters_predicted_enrollments[x].append(total_course_enrollments[x])

      for x in range(number_of_models):
        predicted_data[x][course_list[i]] = all_semesters_predicted_enrollments[x]\

    model_names, course_names, total_model_errors = calculate_error_for_each_model(course_list, courses, predicting_semesters, predicted_data, True)
    make_histograms_for_models(model_names, course_names, total_model_errors)
    store_simulation_data(course_list, courses, predicting_semesters, predicted_data)



    

