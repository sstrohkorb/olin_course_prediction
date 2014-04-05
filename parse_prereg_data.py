import csv
import glob


def get_prereg_data(desired_files_path):
  """
  Takes in a directory with all of the desired preregistration survey data in csv format
  and returns a dictionary that looks like this: 
      {'1314SP': {'Course name': 41, 'Course name 2': 30}, '1415FA': {'Course name': 20, 
        'Course name 2': 45}}

  Call this function like this: get_prereg_data("../pre_reg_survey_data/*")
  """
  all_prereg_filepaths = glob.glob(desired_files_path)
  all_course_data_dict = {}

  for filepath in all_prereg_filepaths:
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
      total_row = -1
      i = 0
      for row in contents:
        all_course_data_dict[semester].append(row)
        for j in range(10):
          if row[j].find("AHS")!= -1 and course_start_column == -1:
            course_start_column = j
            course_name_row = i
          elif row[j].find("otal")!= -1 and total_row == -1:
            total_row = i
        i += 1
      all_course_data_dict[semester].append([course_start_column, course_name_row, total_row])

  # Now that we have all of the information organized by semester, extract the two rows we want
  # which are the one with the course names and the total number who wanted to register for that
  # course
  course_enrollment_dict = {}
  for sem in all_course_data_dict:
    course_enrollment_dict[sem] = {}
    course_name_list = []
    total_expected_enrollment_list = []
    
    sem_data = all_course_data_dict[sem]
    sem_data_len = len(sem_data)
    
    [course_start_column, course_name_row, total_row] = sem_data[sem_data_len - 1]
    
    for i in range(sem_data_len):
      trimmed_list = sem_data[i][course_start_column : sem_data_len]
      if i == course_name_row:
        course_name_list = trimmed_list
      elif i == total_row:
        total_expected_enrollment_list = trimmed_list

    for j in range(len(course_name_list)):
      course_enrollment_dict[course_name_list[j]] = total_expected_enrollment_list[j]

  return course_enrollment_dict


