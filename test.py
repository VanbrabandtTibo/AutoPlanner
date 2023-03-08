import pulp as plp
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, LpInteger, LpContinuous, LpBinary, LpMinimize
from domain.entities import DayOfTheWeek, Employee, Patient, Combination, PersonList
import itertools

employee1 = Employee(1)

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

print("Done")