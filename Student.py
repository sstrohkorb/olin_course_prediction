# Sarah is ID# 721 in the old data, #493 in the updated data
# Berit is ID# 572

class Student:

  def __init__(self, ID, gender, graduating_class, major, concentration, academic_status):
    self.ID = ID
    self.gender = gender
    self.list_of_course_offerings = x = [[] for i in range(8)]
    self.graduating_class = graduating_class
    self.major = major
    self.concentration = concentration
    self.academic_status = academic_status
    self.final_semester = None # last academic semester in student's career
    self.first_semester = None # int representing the year semester since Olin's inception
    # self.major_set = set()
    self.major_history = {}

  def __str__(self):
    return self.ID + ", " + self.gender + ", " + self.graduating_class + ", " + self.major

  def add_course_offering(self, course_offering, student_semester_no):
  	self.list_of_course_offerings[student_semester_no].append(course_offering)

  def set_final_semester(self):
    max_semester = 0
    for i in range(len(self.list_of_course_offerings)):
      if self.list_of_course_offerings[i]:
        max_semester = i
    self.final_semester = max_semester

  def set_first_semester(self, semester_list, semesters):
    min_semester_index = 100
    for semester in semester_list:
      if semesters[semester] < min_semester_index:
        min_semester_index = semesters[semester]

    min_semester_string = ''
    for sem_str in semesters:
      if semesters[sem_str] == min_semester_index:
        min_semester_string = sem_str

    self.first_semester = min_semester_string

  def set_major_history(self):
    semesters = {'FF':0, 'FR':1, 'SO1':2, 'SO2':3, 'JR1':4, 'JR2':5, 'SR1':6, 'SR2':7}
    sem_list = ['FF', 'FR', 'SO1', 'SO2', 'JR1', 'JR2', 'SR1', 'SR2']
    final = self.final_semester
    # Set major to that of previous semester if no major set (for cases before final semester)
    for i in range(final):
      if i not in self.major_history:
        try:
          self.major_history[i] = self.major_history[i-1]
        except:
          self.major_history[i] = 'Undeclared'

    self.major = self.major_history[self.final_semester]
