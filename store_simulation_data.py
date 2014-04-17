from xlwt import Workbook

def store_simulation_data(course_list, courses, sim_data, destination_file_name="test_data.xls"):
  """
  course_list -> the list of courses we're predicting (course numbers)
  """
  
  w = Workbook()

  column_headings = ["Semester", "Predicted Enrollment", "Actual Enrollment", "Pre-Reg Enrollment"]
  semester_names = ["1011FA", "1011SP", "1112FA", "1112SP", "1213FA", "1213SP", "1314FA", "1314SP"]
  semesters_dict = {semester_name: i for i, semester_name in enumerate(semester_names)}
  
  for course_no in course_list: 
    course_name = courses[course_no].title
    if courses[course_no].section_title != '':
      course_name += ": " + courses[course_no].section_title
    num_semesters = len(semesters_dict)
    actual_enrollment = [0] * num_semesters
    prereg_enrollment = [0] * num_semesters
    predicted_enrollment = sim_data[course_no]

    for i, desired_semester in enumerate(semester_names):
    # Sarah:
      if desired_semester in courses[course_no].course_offerings:
          actual_enrollment[i] = int(courses[course_no].course_offerings[desired_semester].enrollment)
          prereg_enrollment[i] = int(courses[course_no].course_offerings[desired_semester].total_prereg_enrollment())

    # Format data for input into the csv file
    data = []
    data.append([course_no + " - " + course_name])
    data.append(column_headings)
    for i in range(num_semesters):
      data.append([semester_names[i], predicted_enrollment[i], actual_enrollment[i], prereg_enrollment[i]])

    ws = w.add_sheet(course_no)
    for i,row in enumerate(data):
      for j,cell in enumerate(row):
          ws.write(i,j,cell)

  w.save(destination_file_name)











