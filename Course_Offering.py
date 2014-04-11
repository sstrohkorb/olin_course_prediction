from sets import Set;

class Course_Offering: 
  
  def __init__(self, semester, Course, enrollment = 0):
    self.course = Course
    self.enrollment = enrollment
    self.prereg_predicted_enrollment = [-1, -1, -1, -1]
    self.professors = Set()
    self.semester = semester

  def __str__(self):
    return self.course.title + ": " + self.semester

  def add_professor(self, professor):
    if not self.professors:
      self.professors.add(professor)
    else: 
      if professor not in self.professors:
        self.professors.add(professor)
