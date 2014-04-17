from parse_course_data import *
import numpy as np

def get_current_and_past_students(students, semester):
    """
    return list of students who are enrolled that semester
    and students who were enrolled previous to that semester
    """
    # note that students who are away during semester will be considered past students
    # even if they are enrolled in later semesters
    current_students = [{} for i in range(8)]
    non_current_students = {} #students who are not enrolled in given semester
    past_students = {} #students who are not current but were enrolled previously
    for s_id, student in students.items():
        # find all current students
        for student_semester, semester_course_offerings in enumerate(student.list_of_course_offerings):
            for c in semester_course_offerings:
                if c.semester == semester:
                    current_students[student_semester][s_id] = student
                    break

        if student in current_students:
            continue
            
        # find all past students if not current
        for student_semester, semester_course_offerings in enumerate(student.list_of_course_offerings):
            for c in semester_course_offerings:
                if c.semester < semester:
                    # Kludge warning! This relies on a lexicographic string comparison
                    past_students[s_id] = student
                    break
    all_current_students = {}
    for semester_dict in current_students:
      all_current_students.update(semester_dict)

    return all_current_students, past_students

def make_student_feature_data(students, courses, desired_course, current_semester, desired_semester, starting_semester, ending_semester):
  """ Setup the x and y vectors that contain all of the data that the model will take in based
      on the enrollment data that is input.
      parameters:
        students: (dict) dictionary mapping student id to student object representing all students.
        courses: (list of tuples) list of courses being considered of form (course number, course title)
        professors: (not currently in use) (dict) dictionary mapping professor name to Professor object
        starting_semester: (string) semester at which the data is to begin (eg '0708FA')
          this means using only data from students who began attending on or after starting_semester
        desired_course: (string) the course number of the considered course
        current_semester: (int) integer representing the current semester of the student
        desired_semester: (int) integer representing the predicted semester of the student
        ending_semester: (string) semester at which the data is to end (eg '0708FA')
      return values:
        all_x_vectors represents the inputs to the linear regression model
        all_y_values represents the outputs to the linear regression model
  """
  # if ending semester is not set, end semester is infinity
  # this could probably be made better
  if ending_semester is None:
    ending_semester = '9999'

  # list of course numbers
  course_list = []
  for course in courses:
    course_list.append(course[0])

  # dict mapping course numbers to index in course_list
  course_dict = {course_list[i]: i for i in range(len(course_list))}
  major_dict = {'Undeclared': 0, 'Mechanical Engineering': 1, "Electr'l & Computer Engr": 2, 'Engineering': 3}
  
  # dict mapping year semsester to number of semesters since olin's inception
  semesters = make_semesters_dict(2002, 2014)

  all_x_vectors = []
  all_y_values = []

  for student_id, student in students.items():

    if student.final_semester < desired_semester:
      # student did not make it to desired_semester- discard student
      continue

    if semesters[student.first_semester] < semesters[starting_semester]:
      # if the student started at Olin before the input starting_semester, discard student
      continue

    num_courses = len(course_list)
    x_vector = [0]*(num_courses + len(major_dict) + 1 + 2 + 1) # 1 for the gender, 2 for the pre-reg data, 1 for the dummy
    y_value = 0

    # flag indicating that student should be discarded if set to True
    drop_student = False

    # Set major for current semester
    x_vector[num_courses + major_dict[student.major_history[current_semester]]] = 1

    # Add geneder of the student
    if 'F' in student.gender: 
      x_vector[num_courses + len(major_dict)] = 1
  
    for student_sem, semester_course_offerings in enumerate(student.list_of_course_offerings):
      # skip building data that will be discarded
      if drop_student:
        break
      for course_offering in semester_course_offerings:
        # skip building data that will be discarder
        if drop_student:
          break

        # student did not reach desired_semester as of end_semester
        if course_offering.semester == ending_semester:
          if student_sem < desired_semester:
            drop_student = True

        course_no = course_offering.course.course_number
        x_vector[course_dict[course_no]] = 1

        # Add the prereg data into the x vector
        if course_no == desired_course:
          # Determine the 'year' the student is in to extract their prereg data
          prereg_index = -1
          if current_semester == 0 or current_semester == 1:
            prereg_index = 0
          elif current_semester == 2 or current_semester == 3:
            prereg_index = 1
          elif current_semester == 4 or current_semester == 5:
            prereg_index = 2
          else:
            prereg_index = 3
          # Enter the prereg data into the x vector
          if course_offering.prereg_predicted_enrollment[prereg_index] != -1:
            x_vector[num_courses + len(major_dict) + 1] = int(course_offering.prereg_predicted_enrollment[prereg_index])
            x_vector[num_courses + len(major_dict) + 1 + 1] = 0
          else: 
            x_vector[num_courses + len(major_dict) + 1] = 0
            x_vector[num_courses + len(major_dict) + 1 + 1] = 1

        # don't include courses from "the future"
        if course_offering.semester > ending_semester:
          x_vector[course_dict[course_no]] = 0

        # don't include courses that have had less than 100 students enrolled in them (ever)
        elif course_offering.course.total_number_of_students < 100:
          x_vector[course_dict[course_no]] = 0

        # designate the students that actually did take the desired course during the desired semester
        elif course_no == desired_course and student_sem == desired_semester:
          x_vector[course_dict[course_no]] = 0
          y_value = 1

        # if the course is in a semester beyond what we're considering, set the y value to 0
        # (not including the 'future' information in our calculations)
        # TODO: change this when course_offering changes
        elif student_sem > current_semester:
          x_vector[course_dict[course_no]] = 0

        # if student has already taken class
        elif course_no == desired_course and student_sem <= current_semester:
          drop_student = True 

    if drop_student:
        continue

    all_x_vectors.append(x_vector)
    all_y_values.append(y_value)

  return [all_x_vectors, all_y_values]


def make_random_training_data(x_vector, y_vector, test_size):
  """ Takes as input all of the x values in a list and the y values in a list and then designates
      a certain number of them (test_size) as test cases and the rest as training data
  """
  # np.random.seed(0)
  indices = np.random.permutation(len(x_vector))
  x_train = [x_vector[i] for i in indices[:-test_size]]
  y_train = [y_vector[i] for i in indices[:-test_size]]
  x_test = [x_vector[i] for i in indices[-test_size:]]
  y_test = [y_vector[i] for i in indices[-test_size:]]

  return [x_train, y_train, x_test, y_test]

