from parse_course_data import *

import csv

semesters_dict = {"1011FA": 0, "1011SP": 1, "1112FA": 2, "1112SP": 3, "1213FA": 4, "1213SP": 5, "1314FA": 6, "1314SP": 7}
course_list = []

[students, courses, professors] = get_course_data('../course_enrollments_2002-2014spring_anonymized.csv')
prereg_data = get_prereg_data("../pre_reg_survey_data/*")
enter_prereg_data(courses, prereg_data)

for course_num in course_list: 

  # Get all the data in lists right here
  # Berit:

  # Sarah:

  with open('/simulation_data/' + course_num + '.csv', 'w', newline='') as fp:
      a = csv.writer(fp, delimiter=',')
      data = [['Me', 'You'],
              ['293', '219'],
              ['54', '13']]
      a.writerows(data)


print "\nActual enrollment data:\n"
for course_no in courses:
    if course_no == "ENGR3290":
        continue
    if desired_semester in courses[course_no].course_offerings:
        print courses[course_no].course_offerings[desired_semester].enrollment
    else:
        print 0

print "\nPrereg data:\n"
for course_no in courses:
    if course_no == "ENGR3290":
        continue
    if desired_semester in courses[course_no].course_offerings:
        print courses[course_no].course_offerings[desired_semester].prereg_predicted_enrollment
    else:
        print 0

print "\nTotal Enrollment (ever)\n"
for course_no in courses:
    if course_no == "ENGR3290":
        continue
    tots_enrollment = 0
    for sem_offered in courses[course_no].course_offerings:
        tots_enrollment += courses[course_no].course_offerings[sem_offered].enrollment
    print tots_enrollment