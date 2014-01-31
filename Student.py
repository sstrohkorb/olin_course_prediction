class Student:

  def __init__(self, ID, gender, list_of_course_offerings, graduating_class, major):
    self.ID = ID
    self.gender = gender
    self.list_of_course_offerings = list_of_course_offerings
    self.graduating_class = graduating_class
    self.major = major

  def __str__(self):
    return self.ID + ", " + self.gender + ", " + self.graduating_class + ", " + self.major