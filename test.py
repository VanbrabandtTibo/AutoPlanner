import pulp as plp
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, LpInteger, LpContinuous, LpBinary, LpMinimize
from domain.entities import DayOfTheWeek, Employee, Patient, Combination, PersonList
import itertools

employee1 = Employee(1)
employee2 = Employee(2)
employee3 = Employee(3)

#print(employee1)

patient1 = Patient(1)
patient2 = Patient(2)
patient3 = Patient(3)

employee1.schedule.add_items([
        (1, DayOfTheWeek.MONDAY, 7,8.5),
        (1, DayOfTheWeek.MONDAY, 9.5,12),
        (1, DayOfTheWeek.MONDAY, 12.5,14),
        (1, DayOfTheWeek.TUESDAY, 7,8.5),
        (1, DayOfTheWeek.TUESDAY, 9.5,12),
        (1, DayOfTheWeek.THURSDAY,7,8.5),
        (1, DayOfTheWeek.THURSDAY,9.5,12),
        (1, DayOfTheWeek.FRIDAY, 7,9.5),
    ])

employee2.schedule.add_items([
        (1, DayOfTheWeek.MONDAY, 9.5,12),
        (1, DayOfTheWeek.TUESDAY, 7.5,8.5),
        (1, DayOfTheWeek.TUESDAY, 9.5,10.5),
        (1, DayOfTheWeek.WEDNESDAY, 7,7.5),
        (1, DayOfTheWeek.WEDNESDAY,7.5,8.5),
        (1, DayOfTheWeek.WEDNESDAY,9.5,12),
        (1, DayOfTheWeek.THURSDAY, 7,8),
        (1, DayOfTheWeek.THURSDAY, 10.5,12)
    ])

employee3.schedule.add_items([
    (1, DayOfTheWeek.TUESDAY,7,8),
    (1, DayOfTheWeek.TUESDAY,9,9.5),
    (1, DayOfTheWeek.TUESDAY,10,11),
    (1, DayOfTheWeek.WEDNESDAY,7,8.5),
    (1, DayOfTheWeek.WEDNESDAY,9.5,11),
    (1, DayOfTheWeek.FRIDAY,7,8.5),
    (1, DayOfTheWeek.FRIDAY,9,9.5),
    (1, DayOfTheWeek.FRIDAY,9.5,11),
])

patient1.schedule.add_items([
        (1, DayOfTheWeek.MONDAY, 9.5,10.5),
        (1, DayOfTheWeek.MONDAY, 11,11.5),
        (1, DayOfTheWeek.FRIDAY, 7.5,9.5),
    ])

patient2.schedule.add_items([
    (1, DayOfTheWeek.TUESDAY,7,8),
    (1, DayOfTheWeek.FRIDAY,7.5,9.5),
    ])

patient3.schedule.add_items([
    (1, DayOfTheWeek.WEDNESDAY,7,8.5),
    (1, DayOfTheWeek.WEDNESDAY,9.5,11),
    (1, DayOfTheWeek.THURSDAY,10,11.5),
])

l_employees = [employee1, employee2, employee3]
l_patients = [patient1, patient2, patient3]

print("Done")
print(employee1)

combinations = Combination(l_employees, l_patients)
c_arr = combinations.get_combinations()

print(c_arr[0])
print(c_arr[1])
print(c_arr[2])