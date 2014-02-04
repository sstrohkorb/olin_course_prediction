class Student:

  def __init__(self, ID, gender, graduating_class, major, academic_status):
    self.ID = ID
    self.gender = gender
    self.list_of_course_offerings = []
    self.graduating_class = graduating_class
    self.major = major
    self.academic_status = academic_status

  def __str__(self):
    return self.ID + ", " + self.gender + ", " + self.graduating_class + ", " + self.major

  def add_course_offering(self, course_offering):
  	self.list_of_course_offerings.append(course_offering)