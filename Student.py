# Sarah is ID# 721
# Berit is ID# 572

class Student:

  def __init__(self, ID, gender, graduating_class, major, concentration, academic_status):
    self.ID = ID
    self.gender = gender
    self.list_of_course_offerings = []
    self.graduating_class = graduating_class
    self.major = major
    self.concentration = concentration
    self.academic_status = academic_status
    self.final_semester = None
    self.major_set = set()
    self.major_history = []

  def __str__(self):
    return self.ID + ", " + self.gender + ", " + self.graduating_class + ", " + self.major

  def add_course_offering(self, course_offering):
  	self.list_of_course_offerings.append(course_offering)

  def set_final_semester(self):
    semesters = {'FF':0, 'FR':1, 'SO1':2, 'SO2':3, 'JR1':4, 'JR2':5, 'SR1':6, 'SR2':7}
    max_semester_index = 0
    for course_offering in self.list_of_course_offerings:
      if semesters[course_offering.student_year] > max_semester_index:
        max_semester_index = semesters[course_offering.student_year]
    
    for semester in semesters:
      if semesters[semester] == max_semester_index:
        self.final_semester = semester

  def set_major_history(self):
    semesters = {'FF':0, 'FR':1, 'SO1':2, 'SO2':3, 'JR1':4, 'JR2':5, 'SR1':6, 'SR2':7}
    majors = list(self.major_set)
    self.major_history = majors.sort(key=lambda x: semesters[x[0]])
