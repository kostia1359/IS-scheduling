import models
import random
from collections import defaultdict

time_mapper = {
    0: "8:40 - 10:15",
    1: "10:35 - 12:10",
    2: "12:20 - 13:55",
    3: "14:05 - 15:40",
}

day_mapper = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday"
}


class ScheduleItem:
    def __init__(self, course, groups):
        self.course = course
        self.room = None
        self.time_slot = None
        self.teacher = random.choice(course.teacher)
        self.groups = groups
        self.time = ""
        self.day = ""
        self.students = 0


    def __str__(self):
        return f"{self.course.id}\t{self.room.id}\t{self.time_slot}\t{self.teacher}" + \
               f"\t{' '.join([x.id for x in self.groups])}"


class Schedule:
    def __init__(self):
        self.items = []
        self.fitness = 0
        self.total_violations = 0

    def calculate_fitness(self):
        schedule = defaultdict(list)
        for item in self.items:
            schedule[item.time_slot].append(item)
        for slot in schedule:
            lecturers = [x.teacher for x in schedule[slot]]
            groups = [group.id for x in schedule[slot] for group in x.groups]
            classrooms = [x.room.id for x in schedule[slot]]
            for constraint in [lecturers, groups, classrooms]:
                self.total_violations += len(constraint) - len(set(constraint))
            for item in schedule[slot]:
                if sum([x.students_count for x in item.groups]) > item.room.capacity:
                    self.total_violations += 1
        self.fitness = 1 / (self.total_violations + 1)

    def add_item(self, item):
        self.items.append(item)

    def recombination(self, partner):
        child = Schedule()
        for i in range(len(self.items)):
            item, partner_item = self.items[i], partner.items[i]
            child_item = ScheduleItem(item.course, item.groups)
            child_item.room = random.choice([item.room, partner_item.room])
            child_item.time_slot = random.choice([item.time_slot, partner_item.time_slot])
            child_item.teacher = random.choice([item.teacher, partner_item.teacher])
            child.add_item(child_item)
        return child

    def __str__(self):
        return '\n'.join(["Course\tRoom\tTime slot\tTeacher\tGroup"] + [str(x) for x in
                                                                        sorted(self.items, key=lambda x: x.time_slot)])


class Scheduler:

    def __init__(self):
        self.teachers = models.Teacher.get_teachers()
        self.courses = models.Course.get_courses()
        self.classrooms = models.Classroom.get_classrooms()
        self.grades = models.Grade.get_grades()
        self.groups = models.Group.get_groups()
        self.time_slots = [i for i in range(20)]

        self.teachers_mapper = {x.id: x.name for x in self.teachers}

    def build_random_schedule(self):
        schedule = Schedule()
        mapper = self.build_subject_group_binding()
        courses = []
        for course in self.courses:
            if course.multiple == 1:
                courses.append(ScheduleItem(course, mapper[course.id]))
            else:
                for group in mapper[course.id]:
                    courses.append(ScheduleItem(course, [group]))

        courses = sum([[x] * x.course.lectures_count for x in courses], [])
        for course in courses:
            course.time_slot = random.choice(self.time_slots)
            course.room = random.choice(self.classrooms)
            schedule.add_item(course)
        schedule.calculate_fitness()
        return schedule

    def build_subject_group_binding(self):
        mapper = defaultdict(list)
        for group in self.groups:
            for course in group.courses:
                mapper[course].append(group)
        return mapper

    def generate(self):
        population = [self.build_random_schedule() for _ in range(40)]
        generation = 1
        fitness = max(population, key=lambda x: x.fitness).fitness
        # print(f"Generation: {generation}, Best fitness: {fitness}")
        while generation < 1000 and fitness < 1:
            generation += 1
            population = self.selection(population)
            fitness = max(population, key=lambda x: x.fitness).fitness
            print(f"Generation: {generation}, Best fitness: {fitness}")
        winner = max(population, key=lambda x: x.fitness)
        print(winner)
        return self.schedule_to_dict(winner)

    def selection(self, population):
        population = sorted(population, key=lambda x: x.fitness)[2:]
        most_fit = sorted(random.sample(population, 30), key=lambda x: x.fitness)[-2:]
        population.append(self.mutate(most_fit[1].recombination(most_fit[0])))
        population.append(self.mutate(most_fit[1].recombination(most_fit[0])))
        return population

    def mutate(self, child):
        for item in child.items:
            if random.random() <= 0.01:
                item.room = random.choice(self.classrooms)
            if random.random() <= 0.01:
                item.time_slot = random.choice(self.time_slots)
            if random.random() <= 0.01:
                item.teacher = random.choice(item.course.teacher)
        child.calculate_fitness()
        return child

    def schedule_to_dict(self, schedule):
        res = []
        for item in schedule.items:
            ditem = {
                'course': item.course.subject,
                'room': item.room.id,
                'day': day_mapper[item.time_slot // 4],
                'time': time_mapper[item.time_slot % 4],
                'time_slot': item.time_slot,
                'teacher': self.teachers_mapper[item.teacher],
                'group': [x.id for x in item.groups],
                'type': item.course.course_type
            }
            res.append(ditem)
        return {'schedule': res}
