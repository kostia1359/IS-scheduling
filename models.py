import json


def string_to_int(s):
    ord3 = lambda x: '%.3d' % ord(x)
    return int(''.join(map(ord3, s)))


class Course:
    database_file_name = "subjects"

    def __init__(self, id, course_type, subject, teacher, lectures_count=1, multiple=0):
        self.subject = subject
        self.course_type = course_type
        self.teacher = teacher
        self.lectures_count = lectures_count
        self.id = id
        self.multiple = multiple

    @staticmethod
    def get_courses():
        entries = Course.get_entries()
        courses = []
        for entree in entries:
            courses.append(
                Course(entree['id'], entree['type'], entree['subject'], entree['teacher'], entree['lectures_count'],
                       entree['multiple']))
        return courses

    @staticmethod
    def get_entries():
        return json.load(open(f'data/{Course.database_file_name}.json'))['data']

    def __hash__(self):
        return self.id


class Teacher:
    database_file_name = 'teachers'

    def __init__(self, id, name):
        self.name = name
        self.id = id

    @staticmethod
    def get_teachers():
        entries = Teacher.get_entries()
        teachers = []
        for entree in entries:
            teachers.append(Teacher(entree['id'], entree['name']))
        return teachers

    @staticmethod
    def get_entries():
        return json.load(open(f'data/{Teacher.database_file_name}.json'))['data']

    def save_to_database(self):
        data = self.get_entries()
        for item in data:
            if item['id'] == self.id:
                data.remove(item)
        data.append(self.to_dict())

        json.dump({'data': data}, open(f'data/{self.database_file_name}.json', 'w'), ensure_ascii=False)

    @staticmethod
    def remove_from_database(id):
        data = Teacher.get_entries()
        for item in data:
            if item['id'] == id:
                data.remove(item)
                json.dump({'data': data}, open(f'data/{Teacher.database_file_name}.json', 'w'), ensure_ascii=False)
                return

    def __hash__(self):
        return self.id

    @staticmethod
    def from_json(data):
        return Teacher(len(Teacher.get_entries()), data['name'])

    def to_dict(self):
        return {'id': self.id,
                'name': self.name}


class Classroom:
    database_file_name = 'classrooms'

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

    @staticmethod
    def get_classrooms():
        entries = Classroom.get_entries()
        classrooms = []
        for entree in entries:
            classrooms.append(Classroom(entree['id'], entree['capacity']))
        return classrooms

    @staticmethod
    def get_entries():
        return json.load(open(f'data/{Classroom.database_file_name}.json'))['data']

    def save_to_database(self):
        data = self.get_entries()
        for item in data:
            if item['id'] == self.id:
                data.remove(item)
        data.append(self.to_dict())
        json.dump({'data': data}, open(f'data/{self.database_file_name}.json', 'w'), ensure_ascii=False)

    @staticmethod
    def remove_from_database(id):
        data = Classroom.get_entries()
        for item in data:
            if item['id'] == id:
                data.remove(item)
                json.dump({'data': data}, open(f'data/{Classroom.database_file_name}.json', 'w'), ensure_ascii=False)
                return

    def __hash__(self):
        return self.id

    @staticmethod
    def from_json(data):
        return Classroom(data['name'], data['capacity'])

    def to_dict(self):
        return {'id': self.id,
                'capacity': self.capacity}


class Grade:
    database_file_name = 'grades'

    def __init__(self, id, courses=None):
        self.id = id
        self.courses = courses if courses else set()

    @staticmethod
    def get_grades():
        entries = Grade.get_entries()
        grades = []
        for entree in entries:
            grades.append(Classroom(entree['id'], entree['courses']))
        return grades

    @staticmethod
    def get_entries():
        return json.load(open(f'data/{Grade.database_file_name}.json'))['data']

    def add_course(self, course_id):
        self.courses.add(course_id)

    def remove_course(self, course_id):
        if course_id in self.courses:
            self.courses.remove(course_id)

    def __hash__(self):
        return self.id


class Group:
    database_file_name = 'groups'

    def __init__(self, id, grade_id, courses, students_count=0):
        self.grade_id = grade_id
        self.students_count = students_count
        self.courses = courses
        self.id = id

    @staticmethod
    def get_groups():
        entries = Group.get_entries()
        groups = []
        for entree in entries:
            groups.append(Group(entree['id'], entree['grade_id'], entree['courses'], entree['students_count']))
        return groups

    @staticmethod
    def get_entries():
        return json.load(open(f'data/{Group.database_file_name}.json'))['data']

    def __hash__(self):
        return self.id


type_mapper = {
    'teachers': Teacher,
    'classrooms': Classroom,
    'groups': Group
}


class DataManager:
    @staticmethod
    def get_data(data_type):
        return type_mapper[data_type].get_entries()

    @staticmethod
    def create(data_type, data):
        item = type_mapper[data_type].from_json(data)
        item.save_to_database()

    @staticmethod
    def delete(data_type, id):
        type_mapper[data_type].remove_from_database(id)
