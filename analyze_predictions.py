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