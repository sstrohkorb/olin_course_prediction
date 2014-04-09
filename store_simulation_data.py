from parse_course_data import *
from big_3_majors_linear_regression import initialize_data, get_sim_data

import csv
from xlwt import Workbook

w = Workbook()

predicting_semesters = ['0506FA','0506SP', '0607FA','0607SP', '0708FA','0708SP', '0809FA', '0809SP', '0910FA', '0910SP', '1011FA', '1011SP', '1112FA', '1112SP', '1213FA', '1213SP', '1314FA', '1314SP']
semester_names = ["1011FA", "1011SP", "1112FA", "1112SP", "1213FA", "1213SP", "1314FA", "1314SP"]
semesters_dict = {semester_name: i for i, semester_name in enumerate(semester_names)}
course_list = ["SCI1210", "ENGR2210", "SCI1410", "MTH2130", "ENGR2510", "SCI1130", "ENGR2410", "MTH2110", "ENGR3410", 
               "ENGR2320", "ENGR2340", "ENGR2350", "ENGR3330", "ENGR2420", "ENGR3220", "ENGR3310", "ENGR3260", 
               "ENGR3390", "ENGR3420", "AHSE2110"]

# [students, courses, professors] = get_course_data('../course_enrollments_2002-2014spring_anonymized.csv')
students, courses, professors, semesters, all_courses_list = initialize_data()
prereg_data = get_prereg_data("../pre_reg_survey_data/*")
enter_prereg_data(courses, prereg_data)

column_headings = ["Semester", "Predicted Enrollment", "Actual Enrollment", "Pre-Reg Enrollment", "ROC value"]

# this makes predicitions using data from the beginning of Olin
# list of dictionaries mapping course number to tuples (tot_enrolled, avg_roc_arith, sem_enr, max_rocs)
sim_data = [get_sim_data(num_iter=50, sim_courses=course_list, start_sem=start_sem, end_sem=predicting_semesters[i+8], students=students, courses=courses, all_courses_list=all_courses_list) for i, start_sem in enumerate(predicting_semesters[:-8])]

for course_no in course_list: 
  course_name = courses[course_no].title
  if courses[course_no].section_title != '':
    course_name += ": " + courses[course_no].section_title
  num_semesters = len(semesters_dict)
  actual_enrollment = [0] * num_semesters
  prereg_enrollment = [0] * num_semesters
  predicted_enrollment = [sem_dict[course_no][0] for sem_dict in sim_data]
  avg_rocs = [sem_dict[course_no][1] for sem_dict in sim_data]

  for i, desired_semester in enumerate(semester_names):

  # Get all the data in lists right here

  # Sarah:
    if desired_semester in courses[course_no].course_offerings:
        actual_enrollment[i] = int(courses[course_no].course_offerings[desired_semester].enrollment)
        prereg_enrollment[i] = int(courses[course_no].course_offerings[desired_semester].prereg_predicted_enrollment)

  # Format data for input into the csv file
  data = []
  data.append([course_no + " - " + course_name])
  data.append(column_headings)
  for i in range(num_semesters):
    data.append([semester_names[i], predicted_enrollment[i], actual_enrollment[i], prereg_enrollment[i], avg_rocs[i]])

  # with open('simulation_data/' + course_no + '.csv', 'wb') as csv_file:
  #     writer = csv.writer(csv_file, delimiter=',')
  #     writer.writerows(data)

  ws = w.add_sheet(course_no)
  for i,row in enumerate(data):
    for j,cell in enumerate(row):
        ws.write(i,j,cell)

w.save("simulation_data.xls")











