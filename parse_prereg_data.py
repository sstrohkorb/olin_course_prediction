import csv
import glob
from math import *

def get_prereg_data(desired_files_path):
  """
  Takes in a directory with all of the desired preregistration survey data in csv format
  and returns a dictionary that looks like this: 
      {'1314SP': {'Course name': 41, 'Course name 2': 30}, '1415FA': {'Course name': 20, 
        'Course name 2': 45}}

  Call this function like this: get_prereg_data("../pre_reg_survey_data/*")
  """
  all_prereg_filepaths = glob.glob(desired_files_path)
  filepaths_not_to_include = ["FA10", "FA11", "SP12"]
  all_course_data_dict = {}


  for filepath in all_prereg_filepaths:
    pursue_filepath = True
    for rejected_filepath in filepaths_not_to_include:
      if rejected_filepath in filepath:
        pursue_filepath = False

    if pursue_filepath:
      with open(filepath,'rU') as f:
        
        # Obtain the semester and years in the format '1314SP' from the csv file name
        if filepath.find("FA") != -1:
          semester_index = filepath.index("FA")
          semester_letters = filepath[semester_index : (semester_index + 2)]
          year = int(filepath[(semester_index + 2) : (semester_index + 4)])
          semester = str(year) + str(year + 1) + semester_letters
        else:
          semester_index = filepath.index("SP")
          semester_letters = filepath[semester_index : (semester_index + 2)]
          year = int(filepath[(semester_index + 2) : (semester_index + 4)])
          semester = str(year - 1) + str(year) + semester_letters
        
        all_course_data_dict[semester] = []

        # Import the csv data and find the rows and columns of the desired info
        contents = csv.reader(f)
        course_start_column = -1
        course_name_row = -1
        firsts_row = -1
        sophs_row = -1
        juniors_row = -1
        seniors_row = -1
        i = 0
        for row in contents:
          all_course_data_dict[semester].append(row)
          for j in range(10):
            if row[j].find("AHS")!= -1 and course_start_column == -1:
              course_start_column = j
              course_name_row = i
            elif (row[j].find("First") != -1 or row[j].find("first") != -1) and firsts_row == -1:
              firsts_row = i
            elif (row[j].find("Soph") != -1 or row[j].find("soph") != -1) and sophs_row == -1:
              sophs_row = i
            elif (row[j].find("Junior") != -1 or row[j].find("junior") != -1) and juniors_row == -1:
              juniors_row = i
            elif (row[j].find("Senior") != -1 or row[j].find("senior") != -1) and seniors_row == -1:
              seniors_row = i
          i += 1
        all_course_data_dict[semester].append([course_start_column, course_name_row, firsts_row, sophs_row, juniors_row, seniors_row])


  # Now that we have all of the information organized by semester, extract the two rows we want
  # which are the one with the course names and the total number who wanted to register for that
  # course
  course_enrollment_dict = {}
  for sem in all_course_data_dict:
    course_enrollment_dict[sem] = {}
    course_name_list = []
    firsts_expected_enrollment_list = []
    sophs_expected_enrollment_list = []
    juniors_expected_enrollment_list = []
    seniors_expected_enrollment_list = []
    
    sem_data = all_course_data_dict[sem]
    sem_data_len = len(sem_data)
    
    [course_start_column, course_name_row, firsts_row, sophs_row, juniors_row, seniors_row] = sem_data[sem_data_len - 1]

    for i in range(sem_data_len):
      trimmed_list = sem_data[i][course_start_column : len(sem_data[0])]
      if i == course_name_row:
        course_name_list = trimmed_list
      elif i == firsts_row:
        firsts_expected_enrollment_list = trimmed_list
      elif i == sophs_row:
        sophs_expected_enrollment_list = trimmed_list
      elif i == juniors_row:
        juniors_expected_enrollment_list = trimmed_list
      elif i == seniors_row:
        seniors_expected_enrollment_list = trimmed_list
    all_years_enrollment_lists = [firsts_expected_enrollment_list, sophs_expected_enrollment_list, juniors_expected_enrollment_list, seniors_expected_enrollment_list]

    for j in range(len(course_name_list)):
      course_name = course_name_list[j]
      space_index = course_name.find(" ")
      course_name = course_name[0 : space_index] + course_name[(space_index + 1) : len(course_name)]
      prereg_enrollment_list = []
      for enrollment_list in all_years_enrollment_lists:
        if enrollment_list:
          raw_enrollment = float(enrollment_list[j])
          prereg_enrollment_list.append(raw_enrollment)
        else:
          prereg_enrollment_list.append(-1)
      course_enrollment_dict[sem][course_name] = prereg_enrollment_list
  return course_enrollment_dict


