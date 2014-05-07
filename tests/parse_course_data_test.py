from controllers import *

def get_course_data_students_test(students):
  """ Test 01 - contents of students """
  test01_pass = True
  test01_error = ""

  if len(students) != 1:
    test01_pass = False
    test01_error += "More or less than one student reported (there should be one). "

  if students:
    for student_no in students:
      # Final semester
      if students[student_no].final_semester != 6:
        test01_pass = False
        test01_error = "Incorrect student final semester."
      # First semester
      if students[student_no].first_semester != "1011FA":
        test01_pass = False
        test01_error = "Incorrect student first semester."
      # Gender
      if students[student_no].gender != "F":
        test01_pass = False
        test01_error = "Incorrect student gender."
      # Graduating class
      if students[student_no].graduating_class != "0":
        test01_pass = False
        test01_error = "Incorrect student graduating class."
      # random ID
      if students[student_no].ID != "493":
        test01_pass = False
        test01_error = "Incorrect student ID."
      # List of course offerings (we'll check that they're here)
      course_offerings = students[student_no].list_of_course_offerings
      mod_sim_math_no = course_offerings[0][0].course.course_number
      if mod_sim_math_no != "MTH1111":
        test01_pass = False
        test01_error = "Incorrect student course offering list."
      # Major
      if "Electr'l & Computer Engr" not in students[student_no].major:
        test01_pass = False
        test01_error = "Incorrect student major."
      # Major history
      if "Undeclared" not in students[student_no].major_history[2] or "Electr'l & Computer Engr" not in students[student_no].major_history[3]:
        test01_pass = False
        test01_error = "Incorrect student major history."
      # Semesters present
      if "1314FA" not in students[student_no].semesters_present or "1011FA" not in students[student_no].semesters_present:
        test01_pass = False
        test01_error = "Incorrect student semesters present."

  return test01_pass, test01_error

def get_course_data_courses_test(courses):
  """ Test 02 - contents of courses """
  test02_pass = True
  test02_error = ""

  if len(courses) != 14:
    test02_pass = False
    test02_error += "More or less than one student reported (there should be 14). "

  if courses:
    if not courses["ENGR2420"]:
      test02_pass = False
      test02_error += "Circuits course (ENGR2420) not present in courses list. "
    else:
      circuits = courses["ENGR2420"]
      

  return test02_pass, test02_error

def get_course_data_test():
  
  all_tests_pass = True

  """ Run the function under test (FUT) """
  [students, courses, professors] = get_course_data("input_data/test_course_data01.csv")

  # students test
  test01_pass, test01_error = get_course_data_students_test(students)
  if test01_pass == False:
    all_tests_pass = False
    print "Test 01 FAIL: " + test01_error

  # courses test
  test02_pass, test02_error = get_course_data_courses_test(courses)
  if test02_pass == False:
    all_tests_pass = False
    print "Test 02 FAIL: " + test02_error

  # no professors test for now since we don't really use it
  
  if all_tests_pass == True:
    print "PASS: all tests for get_course_data()"










