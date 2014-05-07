from Course_Offering import *

class Course: 
  
  def __init__(self, title, section_title, course_number, total_number_of_students = 0):
    self.title = title
    self.section_title = section_title
    self.course_number = course_number
    self.course_offerings = {}
    self.total_number_of_students = total_number_of_students

  def __str__(self):
    display_str = self.course_number + ' : ' + self.title + ' '
    if self.section_title != '':
      display_str += self.section_title
    for semester in self.course_offerings:
      display_str += "\n\t" + semester + " : " + str(self.course_offerings[semester].enrollment) + ", " 
      for professor in self.course_offerings[semester].professors:
        display_str += professor.name + "; "
    return display_str + "\n"

  def add_course_offering(self, semester):
    if semester not in self.course_offerings:
      new_course_offering = Course_Offering(semester, self)
      self.course_offerings[semester] = new_course_offering
    return self.course_offerings[semester]
