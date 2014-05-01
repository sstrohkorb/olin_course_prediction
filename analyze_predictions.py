import matplotlib.pyplot as plt
from numpy import *

def determine_highest_weighted_courses(logistic, all_features_list, number_of_courses):
  """ Finds the classes with highest absolute value coefficients and determines whether 
      they're positive or negative
  """
  sorted_highly_weighted_courses = sorted(zip(logistic.coef_[0], all_features_list), key=lambda x:abs(x[0]), reverse=True)
  return sorted_highly_weighted_courses[:number_of_courses]

def print_highest_weighted_courses(logistic, all_features_list, number_of_courses):
  highly_weighted_courses = determine_highest_weighted_courses(logistic, all_features_list, number_of_courses)
  temp_str = ""
  i = 0
  for correlation, course_info in highly_weighted_courses:
    # if correlation < 0:
    #   temp_str += "-"
    # else: 
    #   temp_str += "+"
    # temp_str += " " + course_info[1] + '\n'
    if course_info[0] == "PR1":
      print course_info[1], i, correlation
    i += 1
  return temp_str

def calculate_error_for_each_model(course_list, courses, semester_names, sim_data, semesters_with_prereg_data_only):
  model_names = ["Baseline Predicted Enrollment","Spring/Fall Feature Enrollment", "Prereg Predicted Enrollment", "Course History Predicted Enrollment", "Prereg + Course History Predicted Enrollment", "Pre-Reg Enrollment"]

  semesters_dict = {semester_name: i for i, semester_name in enumerate(semester_names)}
  number_of_models = len(sim_data)

  total_model_errors = [[] for x in range(number_of_models + 1)]

  course_names = []

  for course_no in course_list: 
    course_name = courses[course_no].title
    if courses[course_no].section_title != '':
      course_name += ": " + courses[course_no].section_title
    course_names.append(course_name)

    num_semesters = len(semesters_dict)

    actual_enrollment = [0] * num_semesters
    prereg_enrollment = [0] * num_semesters

    model_predicted_enrollment = [[] for i in range(number_of_models)]
    for i in range(number_of_models):
      model_predicted_enrollment[i] = sim_data[i][course_no]
      
    for i, desired_semester in enumerate(semester_names):
      if desired_semester in courses[course_no].course_offerings:
          actual_enrollment[i] = int(courses[course_no].course_offerings[desired_semester].enrollment)
          prereg_enrollment[i] = int(courses[course_no].course_offerings[desired_semester].total_prereg_enrollment())

    error_for_each_model = [0]*number_of_models
    for j in range(number_of_models + 1): 
      error_for_each_model = 0.0
      for i in range(num_semesters):
        smoother = 0.0
        if actual_enrollment[i] == 0:
          smoother = 1.0
        # pre-reg data
        if j == number_of_models:
          if prereg_enrollment[i] == 0:
            error_for_each_model += 0
          else:
            error_for_each_model += abs(float(actual_enrollment[i]) - float(prereg_enrollment[i]))
        else:
          if prereg_enrollment[i] != 0 or not semesters_with_prereg_data_only:
            error_for_each_model += abs(float(actual_enrollment[i]) - float(model_predicted_enrollment[j][i]))
          else:
            error_for_each_model += 0

      total_model_errors[j].append(error_for_each_model)

  return model_names, course_names, total_model_errors

def make_histograms_for_models(model_names, course_names, error_list):
  width = .8
  bar_starts = range(len(course_names))
  label_center = map(lambda x: x+width/2, bar_starts)
  num_models = len(model_names)
  # plt.figure(1)
  for i, model_name in enumerate(model_names):
    plt.figure(i+1)
    # plt.subplot(num_models, 1, i+1)
    plt.bar(bar_starts, error_list[i])

    print model_name
    print median(error_list[i])
    
    plt.xticks(label_center, course_names, rotation='vertical')
    plt.ylabel('error')
    plt.ylim((0, 60))
    plt.title(model_name)

  plt.show()

def test_make_histo():
  model_names = ['model a', 'model b', 'model c']
  course_names = ['course 1', 'course 2', 'course 3', 'course 4']
  error_list = [ [1,2,3,4], [5,4,3,2], [8,7,0,9]]
  make_histograms_for_models(model_names, course_names, error_list)

if __name__ == '__main__':
  test_make_histo()
