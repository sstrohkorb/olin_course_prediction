from parse_course_data import *

import csv

semesters_dict = {"1011FA": 0, "1011SP": 1, "1112FA": 2, "1112SP": 3, "1213FA": 4, "1213SP": 5, "1314FA": 6, "1314SP": 7}
course_list = ["SCI1210"]

[students, courses, professors] = get_course_data('../course_enrollments_2002-2014spring_anonymized.csv')
prereg_data = get_prereg_data("../pre_reg_survey_data/*")
enter_prereg_data(courses, prereg_data)

column_headings = ["Semester", "Predicted Enrollment", "Actual Enrollment", "Pre-Reg Enrollment"]

for course_no in course_list: 
  num_semesters = len(semesters_dict)
  actual_enrollment = [0] * num_semesters
  prereg_enrollment = [0] * num_semesters
  predicted_enrollment = [0] * num_semesters
  semester_names = [''] * num_semesters
  for i in range(num_semesters):
    for semester in semesters_dict:
      if semesters_dict[semester] == i:
        desired_semester = semester
    semester_names[i] = desired_semester

  # Get all the data in lists right here
  # Berit:
  # if you could store your stuff in predicted_enrollment, that'd be great!! 

  # Sarah:
    if desired_semester in courses[course_no].course_offerings:
        actual_enrollment[i] = courses[course_no].course_offerings[desired_semester].enrollment
        prereg_enrollment[i] = courses[course_no].course_offerings[desired_semester].prereg_predicted_enrollment


  with open('simulation_data/' + course_no + '.csv', 'wb') as csv_file:
      writer = csv.writer(csv_file, delimiter=',')
      data = [['Me', 'You'],
              ['293', '219'],
              ['54', '13']]
      writer.writerows(data)
