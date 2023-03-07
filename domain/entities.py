from enum import Enum
from typing import Callable
import numpy as np
import pandas as pd

# DAYOFTHEWEEK CLASS
class DayOfTheWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

# SCHEDULETEMPLATEITEM CLASS
class ScheduleTemplateItem():
    def __init__(self, timeslot_id: int):
        self.timeslot_id = timeslot_id

# SCHEDULETEMPLATE CLASS
class SchedulingTemplate():
    def __init__(self, items: list[ScheduleTemplateItem] = None):
        if items:
            self.items = items
        else:
            self.items = []

    def add_item(self, week_number: int, week_day: DayOfTheWeek, from_hours: float, to_hours: float):
        # get all possible timslots
        generate_time_slots = self.generate_time_slots()
        # get the numeric codes for the from and to values
        from_numeric, to_numeric = self.get_numeric_values(week_number, week_day, from_hours, to_hours)
        # get the timeslot_ids that are between the from and to values
        timeslot_ids = self.get_timeslots(from_numeric, to_numeric, generate_time_slots)
        # add the timeslots to the template
        self.items.extend(ScheduleTemplateItem(timeslot_id) for timeslot_id in timeslot_ids)
    
    def add_items(self, items: list[tuple[int, DayOfTheWeek, float, float]]):
        [self.add_item(week_number = week_number, week_day=week_day, from_hours=from_hours, to_hours=to_hours) 
         for week_number, week_day, from_hours, to_hours in items]
        
    # def get_numeric_template(self):
    #     return list([item.get_numeric_values() for item in self.items])
    
    def get_timeslots(self, from_numeric: str, to_numeric: str, generate_time_slots: dict):
        start_timeslot_id =  generate_time_slots.keys().find(from_numeric)
        end_timeslot_id = generate_time_slots.keys().find(to_numeric)
        return range(start_timeslot_id, end_timeslot_id + 1)
    
    @staticmethod
    def get_numeric_values(week_number: int, week_day: DayOfTheWeek, from_hours: float, to_hours: float):
        """
        Returns an float value that represents the from and to for a specific week number and day
        E.g. Week 1 monday from 9.5 until 11.5 becomes from 1109.5 to 1111.5
        E.g. Week 2 from friday 13 until 14.5 becomes from 2513 to 2514.5

        Output: tuple containing (from_value, to_value, group_id)
        """

        # this will pad zeros left so that there are 5 digits total with 2 digits after the decimal point.
        pad_float = lambda float: '%05.2f'% float

        numeric_week_and_day = f"{week_number}{week_day}"
        numeric_from = f"{numeric_week_and_day}{pad_float(from_hours)}" 
        numeric_to = f"{numeric_week_and_day}{pad_float(to_hours)}" 
        return (numeric_from, numeric_to)
    
    @staticmethod
    def generate_time_slots():
        time_slots = {}
        time_slot_id = 0
        
        for week_number in range(1, 53):
            for week_day in DayOfTheWeek:
                for hour in range(24):
                    for minute in range(0, 60, 30):
                        time_slot_code = f"{week_number}{week_day.value}{hour:02d}.{minute:02d}"
                        time_slots[time_slot_code] = ScheduleTemplateItem(time_slot_id)
                        time_slot_id += 1
        
        return time_slots
        
    def __str__(self):
        return '\n'.join([str(item) for item in self.items])

# PERSON CLASS    
class Person():
    def __init__(self, id: int, schedule: SchedulingTemplate = None):
        self.id = id
        if schedule:
            self.schedule = schedule
        else:
            self.schedule = SchedulingTemplate()

# EMPLOYEE CLASS
class Employee(Person):
    def __init__(self, id: int, schedule: SchedulingTemplate = None):
        super().__init__(id, schedule)

    def __str__(self) -> str:
        return f'Schedule template for employee {self.id}\n{str(self.schedule)}'

# PATIENT CLASS
class Patient(Person):
    def __init__(self, id: int, schedule: SchedulingTemplate = None):
        super().__init__(id, schedule)
        
    def __str__(self) -> str:
        return f'Schedule template for patient {self.id}\n{str(self.schedule)}'
    
# PERSONLIST CLASS
class PersonList:
    def __init__(self, persons: list[Person]): 
        self._persons = persons
        self.group_persons_by_time_slot()

    def group_persons_by_time_slot(self):
        templates = set(map(lambda x:x.schedule.get_numeric_template() ,self._persons))
        grouped_persons = [[person for person in self._persons if person.schedule.get_numeric_template()[0] == template[0] and 
                                                                  person.schedule.get_numeric_template()[1] == template[1]] for template in templates]
        return grouped_persons

# COMBINATION CLASS     
class Combination:
    def __init__(self, employee: list[Employee], patient: list[Patient]):
        self.employee = employee
        self.patient = patient
    
    # get 3 dimensional array of all combinations of employees and patients and time slots
    def get_combinations(self):
        time_slots = set()
        for person in self.employee + self.patient:
            for item in person.schedule.items:
                time_slots.add(item.timeslot_id)
        time_slots = sorted(time_slots)

        # Create 1-dimensional arrays of employees, patients, and time slots
        employees_arr = np.array([employee.id for employee in self.employee])
        patients_arr = np.array([patient.id for patient in self.patient])
        timeslots_arr = np.array(time_slots)

        # Use meshgrid to create 3-dimensional array of all combinations
        # combinations = np.array(np.meshgrid(employees_arr, patients_arr, timeslots_arr)).T.reshape(-1, 3)

        combinations = [[employee, patient, timeslot] for employee in employees_arr for patient in patients_arr for timeslot in timeslots_arr]

        return combinations