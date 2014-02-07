from parse_course_data import *

import numpy as np
from sklearn import datasets
from sklearn import linear_model

[students, courses, professors] = get_course_data('../anonymizeddata_UpToFall2013.csv')

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
    if course_no == 'ENGR3420':
      y_value = 1

  all_x_vectors.append(x_vector)
  all_y_values.append(y_value)

# Select traning and testing data
all_x_vectors_train = all_x_vectors[:-10]
all_y_values_train = all_y_values[:-10]
all_x_vectors_test  = all_x_vectors[-10:]
all_y_values_test  = all_y_values[-10:]

logistic = linear_model.LogisticRegression(C=1e5)
logistic.fit(all_x_vectors_train, all_y_values_train)

for i in range(len(all_x_vectors_test)):
  print logistic.predict(all_x_vectors_test[i])
  print all_y_values_test[i]