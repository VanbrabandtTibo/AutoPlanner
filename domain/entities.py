from enum import Enum

class DayOfTheWeek(Enum):
    MONDAY = 1,
    TUESDAY = 2,
    WEDNESDAY = 3,
    THURSDAY = 4,
    FRIDAY = 5,
    SATURDAY = 6,
    SUNDAY = 7


class ScheduleTemplateItem():

    def __init__(self, week_number:int, week_day: int, from_hours: float, to_hours: float, patient_group: int):
        self.week_number = week_number
        self.week_day = week_day
        self.from_hours = from_hours
        self.to_hours = to_hours
        self.patient_group = patient_group
    
    def get_numeric_values(self):
        """
        Returns an float value that represents the from and to for a specific week number and day
        E.g. Week 1 monday from 9.5 until 11.5 becomes from 1109.5 to 1111.5
        E.g. Week 2 from friday 13 until 14.5 becomes from 2513 to 2514.5

        Output: tuple containing (from_value, to_value, group_id)
        """
        numeric_week_and_day = f"{self.week_number}{self.week_day}"
        numeric_from = f"{numeric_week_and_day}{str(self.from_hours).ljust(2,'0')}" 
        numeric_to = f"{numeric_week_and_day}{str(self.to_hours).ljust(2,'0')}" 
        return (numeric_from, numeric_to, self.patient_group)
    
    def __str__(self):
            return f'{DayOfTheWeek(self.week_day).name} from {self.from_hours} to {self.to_hours} scheduled {self.patient_group}'

         

class SchedulingTemplate():
    
    def __init__(self, items: list[ScheduleTemplateItem] = None):
        if items:
            self.items = items
        else:
            self.items = []

    def add_item(self, week_number: int, week_day: DayOfTheWeek, from_hours: float, to_hours: float, patient_group: int):
        self.items.append(ScheduleTemplateItem(week_number=week_number, week_day=week_day.value, from_hours=from_hours, to_hours=to_hours, patient_group=patient_group))
    
    def add_items(self, items: list[tuple[int, DayOfTheWeek, float, float, int]]):
        [self.add_item(week_number = week_number, week_day=week_day, from_hours=from_hours, to_hours=to_hours, patient_group=patient_group) 
         for week_number, week_day, from_hours, to_hours, patient_group in items]
        
    def get_numeric_template(self):
        return list([item.get_numeric_values() for item in self.items])
        
    def __str__(self):
        return '\n'.join([str(item) for item in self.items])

    
class Person():

    def __init__(self, id: int, schedule: SchedulingTemplate = None):
        self.id = id
        if schedule:
            self.schedule = schedule
        else:
            self.schedule = SchedulingTemplate()


class Employee(Person):
    def __init__(self, id: int, schedule: SchedulingTemplate = None):
        super().__init__(id, schedule)

    def __str__(self) -> str:
        return f'Schedule template for employee {self.id}\n{str(self.schedule)}'


class Patient(Person):
    def __init__(self, id: int, schedule: SchedulingTemplate = None):
        super().__init__(id, schedule)
        
    def __str__(self) -> str:
        return f'Schedule template for patient {self.id}\n{str(self.schedule)}'

