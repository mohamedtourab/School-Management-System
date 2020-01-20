from django.test import TestCase
from application.models import *


class TeacherTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('a', 'c@mail.com', 'cc')
        Teacher.objects.create(user=user, ID=1, first_name="Corentin", last_name="Dieudonne",
                               email="corentin.dieudonne@gmail.com", fiscalCode="DDNCNT97B08Z110P",
                               appointmentSchedule=" ", )

    def test_on(self):
        teach = Teacher.objects.get(last_name="Dieudonne")
        self.assertEqual(teach.first_name, "Corentin")


'''
class ClassInfoTestCase(TestCase):
    def setUp(self):
        class1 = ClassInfo.objects.create(ID=6, name="1A", totalStudentsNumber=22, gender_ratio=0.2, skill_average=5)
        class2 = ClassInfo.objects.create(ID=66, name="1A", totalStudentsNumber=22, gender_ratio=0.4, skill_average=5)

        Student.objects.create(grade_choice="FIRST", ID=2, first_name="Victor", last_name="Seguin",
                               classID=class1, studentYear=1)
        Student.objects.create(grade_choice="FIRST", ID=229, first_name="Victr", last_name="Sguin",
                               classID=class2, studentYear=2)

    def test_on(self):
        student = Student.objects.get(ID=229)
        self.assertEqual(student.last_name(), "Sguin")


class AdminOfficerTestCase(TestCase):
    def setUp(self):
        admnof = User.objects.create_user('Abbi')
        admnoff = User.objects.create_user('Many')
        AdministrativeOfficer.objects.create(user=admnof, first_name="Ab", last_name="Bi", email="ab.bi@gmail.com",
                                             ID=4)
        AdministrativeOfficer.objects.create(user=admnoff, first_name="Bi", last_name="Bi", email="bi.bi@gmail.com",
                                             ID=44)


class ParentTestCase(TestCase):
    def setUp(self):
        parent = User.objects.create_user('Baba')
        parent2 = User.objects.create_user('Papa')
        Parent.objects.create(user=parent, ID=5, lastLogin=False)
        Parent.objects.create(user=parent2, ID=59, lastLogin=True)


class ClassCourseTestCase(TestCase):
    def setUp(self):
        ClassCourse.objects.create(ID=57, class_id=7, course_id=10, teacher_id=1)
        ClassCourse.objects.create(ID=7, class_id=7, course_id=100, teacher_id=1)


class ParentStudentTestCase(TestCase):
    def setUp(self):
        ParentStudent.objects.create(ID=11, parentID=5, student_id=20)
        ParentStudent.objects.create(ID=110, parentID=5, student_id=200)


class TeacherCourseTestCase(TestCase):
    def setUp(self):
        TeacherCourse.objects.create(ID=12, teacherID=1, course_id=10)
        TeacherCourse.objects.create(ID=125, teacherID=1, course_id=100)


class PrincipleTestCase(TestCase):
    def setUp(self):
        principle = User.objects.create_user("AD")
        principle_2 = User.objects.create_user("BC")
        Principle.objects.create(user=principle, first_name="Antony", last_name="Davis", email="antony.davis@gmail.com",
                                 ID=3)
        Principle.objects.create(user=principle_2, first_name="Anony", last_name="Davis",
                                 email="antony.davs@gmail.com",
                                 ID=39)


class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(year_choice=1, ID=10, name="Maths", numberOfHoursPerWeek=3, year=1)
        Course.objects.create(year_choice=1, ID=100, name="Art", numberOfHoursPerWeek=5, year=2)


class AssignmentTestCase(TestCase):
    def setUp(self):
        Assignment.objects.create(ID=14, assignmentFile="test.pdf", assignmentTitle="Forst",
                                  course_id=10, additionDate="12-01-2020", deadlineDate="12-10-2020")
        Assignment.objects.create(ID=142, assignmentFile="add.pdf", assignmentTitle="June",
                                  course_id=100, additionDate="12-01-2019", deadlineDate="12-10-2022")

class StudentCourseTestCase(TestCase):
    def setUp(self):
        StudentCourse.objects.create(ID=21, student_id=20, course_id=10, finalGrade=5, publishFinalGrade=True)
        StudentCourse.objects.create(ID=21, student_id=20, course_id=10, finalGrade=5, publishFinalGrade=True)


class PerformanceGradeTestCase(TestCase):
    def setUp(self):
        AssignFinalGrade.objects.create(ID=22, studentCourseID=10, date="12-10-2020", grade=5)
        AssignFinalGrade.objects.create(ID=228, studentCourseID=10, date="10-10-2020", grade=5)


class NoteTestCase(TestCase):
    def setUp(self):
        Note.objects.create(ID=23, studentCourseID=21, noteDate="01-01-2020", noteText="oui")
        Note.objects.create(ID=235, studentCourseID=210, noteDate="01-01-2020", noteText="oui")


class ContentTestCase(TestCase):
    def setUp(self):
        Content.objects.create(ID=25, course_id=10, contentString="trr",
                               material="a.pdf", materialTitle="e", additionDate="01-01-2020")
        Content.objects.create(ID=25, course_id=100, contentString="trr",
                               material="attr.pdf", materialTitle="egfd", additionDate="12-01-2020")


class AnnouncementTestCase(TestCase):
    def setUp(self):
        Announcement.objects.create(ID=26, announcementText="ab", announcementTitle="es", date="01-01-2020")
        Announcement.objects.create(ID=263, announcementText="arb", announcementTitle="eaz", date="02-02-2020")


class AttendanceTestCase(TestCase):
    def setUp(self):
        Attendance.objects.create(ID=27, studentCourseID=10, presence=False, date="01-01-2020")
        Attendance.objects.create(ID=279, studentCourseID=100, presence=False, date="01-01-2020")


class BehaviorTestCase(TestCase):
    def setUp(self):
        Behavior.objects.create(ID=28, studentCourseID=10, date='01-01-2020', behavior="deac")
        Behavior.objects.create(ID=282, studentCourseID=100, date='11-01-2020', behavior="dac")


class FreeSlotsTestCase(TestCase):
    def setUp(self):
        FreeSlots.objects.create(teacherID=1, date="02-02-2020", schedule="a")
        FreeSlots.objects.create(teacherID=1, date="03-03-2020", schedule="pmk")'''
