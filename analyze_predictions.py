import matplotlib.pyplot as plt

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

def make_histograms_for_models(model_names, course_names, error_list):
  width = .8
  bar_starts = range(len(course_names))
  label_center = map(lambda x: x+width/2, bar_starts)
  num_models = len(model_names)
  plt.figure(1)
  for i, model_name in enumerate(model_names):
    plt.subplot(num_models, 1, i)
    plt.bar(bar_starts, error_list[i])
    plt.xticks(label_center, course_names)
    plt.ylabel('error')
    plt.title(model_name)
  plt.show()

def test_make_histo():
  model_names = ['model a', 'model b']
  course_names = ['course 1', 'course 2', 'course 3']
  error_list = [ [2, 3, 4], [5, 2, 7]]
  make_histograms_for_models(model_names, course_names, error_list)

if __name__ == '__main__':
  test_make_histo()
