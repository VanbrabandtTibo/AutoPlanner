from pulp import *

therapistsH = {
            'Therapist 1': {
                'Monday': (9, 17),
                'Tuesday': (9, 17),
                'Wednesday': (13, 17),
                'Thursday': (10, 15),
                'Friday': None,
                'Saturday': None,
                'Sunday': None
            },
            'Therapist 2': {
                'Monday': None,
                'Tuesday': None,
                'Wednesday': (11, 16),
                'Thursday': (12, 17),
                'Friday': (9, 15),
                'Saturday': None,
                'Sunday': None
            },
            'Therapist 3': {
                'Monday': (10, 15),
                'Tuesday': (10, 14),
                'Wednesday': (10, 14),
                'Thursday': None,
                'Friday': (9, 16),
                'Saturday': None,
                'Sunday': None
            }
        }

patientsH = {
            'Patient 1': {
                'Monday': (10, 11),
                'Tuesday': (12, 13),
                'Wednesday': (15, 16),
                'Thursday': (11, 12),
                'Friday': None,
                'Saturday': None,
                'Sunday': None
            },
            'Patient 2': {
                'Monday': None,
                'Tuesday': None,
                'Wednesday': (13, 14),
                'Thursday': (14, 15),
                'Friday': None,
                'Saturday': None,
                'Sunday': None
            },
            'Patient 3': {
                'Monday': None,
                'Tuesday': (14, 15),
                'Wednesday': None,
                'Thursday': None,
                'Friday': (15, 16),
                'Saturday': None,
                'Sunday': None
            }
        }

class TherapistScheduler:
    def __init__(self, therapists=therapistsH, patients=patientsH):
        self.therapists = therapists
        self.patients = patients
        self.prob = LpProblem("Therapist scheduling", LpMaximize)
        # therapist,day,patient,group,driver
        self.x = LpVariable.dicts('x', [(therapist,day,patient) for therapist in self.therapists.keys() for day in self.therapists[therapist].keys() for patient in self.patients.keys()], cat=LpBinary)
        self.create_objective_function()
        self.create_constraints()
    
    def create_objective_function(self):
        # therapist,day,patient,group,driver
        self.prob += lpSum([(therapist,day,patient) for therapist in self.therapists.keys() for day in self.therapists[therapist].keys() for patient in self.patients.keys()])

    def create_constraints(self):
        # Patient availability constraint
        for patient in self.patients.keys():
            for day in self.therapists['Therapist 1'].keys():
                if self.patients[patient][day] is not None:
                    start, end = self.patients[patient][day]
                    self.prob += lpSum([self.x[(therapist,day,patient)] for therapist in self.therapists.keys()]) <= (end - start) / 0.5

        # Therapist availability constraint
        for therapist in self.therapists.keys():
            for day in self.therapists[therapist].keys():
                if self.therapists[therapist][day] is None:
                    for patient in self.patients.keys():
                        self.prob += self.x[(therapist,day,patient)] == 0
                else:
                    start, end = self.therapists[therapist][day]
                    self.prob += lpSum([self.x[(therapist,day,patient)] for patient in self.patients.keys()]) <= (end - start) / 0.5

        # One-patient-per-therapist constraint
        for therapist in self.therapists.keys():
            for patient in self.patients.keys():
                self.prob += lpSum([self.x[(therapist,day,patient)] for day in self.therapists[therapist].keys()]) <= 1
                
        # Group participation contraint
        # Session (amount of children at the same time, with the same specialist)
        # Driver availability constraint

    def solve(self):
        status = self.prob.solve()
        return status

    def get_schedule(self):
        schedule = {}
        for patient in self.patients.keys():
            schedule[patient] = {}
            for day in self.therapists['Therapist 1'].keys():
                if self.patients[patient][day] is not None:
                    start, end = self.patients[patient][day]
                    scheduled = [therapist for therapist in self.therapists.keys() if value(self.x[(therapist,day,patient)]) == 1]
                    if len(scheduled) > 0:
                        schedule[patient][day] = {"therapists": scheduled, "start_time": start, "end_time": end}
        return schedule 