from xlwt import Workbook


def make_excel_for_models(model_names, course_names, error_list, filename='model_comparison.xls'):
  """
  Write model error data to excel spreadsheet
  """
  w = Workbook()
  column_headings = ['Course Name'] + model_names

  data = [column_headings]
  data.extend(zip(*[course_names] + error_list))

  ws = w.add_sheet('model comparison')

  for i,row in enumerate(data):
      for j,cell in enumerate(row):
          ws.write(i,j,cell)

  w.save(filename)

def test_make_excel_for_models(filename='excel_test.xls'):
  model_names = ['model a', 'model b', 'model c']
  course_names = ['course 1', 'course 2', 'course 3', 'course 4']
  error_list = [ [1,2,3,4], [5,4,3,2], [8,7,0,9]]

  make_excel_for_models(model_names, course_names, error_list, filename)


def store_simulation_data(course_list, courses, semester_names, sim_data, destination_file_name="test_data.xls"):
  """
  course_list -> the list of courses we're predicting (course numbers)
  """
  
  w = Workbook()

  column_headings = ["Semester", "Baseline Predicted Enrollment","Gender Feature Enrollment", "Prereg Predicted Enrollment", "Course History Predicted Enrollment", "Prereg + Course History Predicted Enrollment", "Actual Enrollment", "Pre-Reg Enrollment"]
  semesters_dict = {semester_name: i for i, semester_name in enumerate(semester_names)}
  number_of_models = len(sim_data)

  for course_no in course_list: 
    course_name = courses[course_no].title
    if courses[course_no].section_title != '':
      course_name += ": " + courses[course_no].section_title
    num_semesters = len(semesters_dict)
    actual_enrollment = [0] * num_semesters
    prereg_enrollment = [0] * num_semesters

    model_predicted_enrollment = [[] for i in range(number_of_models)]
    for i in range(number_of_models):
      model_predicted_enrollment[i] = sim_data[i][course_no]

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
      temp_data_list = [semester_names[i]]
      for model in model_predicted_enrollment:
        temp_data_list.append(model[i])
      temp_data_list += [actual_enrollment[i], prereg_enrollment[i]]
      data.append(temp_data_list)

    ws = w.add_sheet(course_no)
    for i,row in enumerate(data):
      for j,cell in enumerate(row):
          ws.write(i,j,cell)

  w.save(destination_file_name)


if __name__ == '__main__':
  test_make_excel_for_models()











