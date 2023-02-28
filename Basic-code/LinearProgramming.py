from pulp import *

# Define therapists and their availability
therapists = {
    'Therapist 1': {
        'Week' : {
            'Monday': (9, 17, 1),
            'Tuesday': (9, 17, 1),
            'Wednesday': (13, 17, 4),
            'Thursday': (10, 15, 4),
            'Friday': None,
            'Saturday': None,
            'Sunday': None
        }
    },
    'Therapist 2': {
        'Week' : {
            'Monday': None,
            'Tuesday': (12, 16, 5),
            'Wednesday': (11, 16, 5),
            'Thursday': (12, 17, 5),
            'Friday': (9, 17, 5),
            'Saturday': None,
            'Sunday': None
        }
    },
    'Therapist 3': {
        'Week' : {
            'Monday': (10, 15, 4),
            'Tuesday': (10, 14, 4),
            'Wednesday': (10, 14, 4),
            'Thursday': None,
            'Friday': (9, 16, 4),
            'Saturday': None,
            'Sunday': None
        }
    }
}

# Define patients and their preferred appointment times
patients = {
    'Patient 1': {
        'Week' : {
            'Monday': (10, 11, 1),
            'Tuesday': (12, 13, 1),
            'Wednesday': (15, 16, 1),
            'Thursday': (11, 12, 1),
            'Friday': None,
            'Saturday': None,
            'Sunday': None
        },
        'Session': True
    },
    'Patient 2': {
        'Week' : {
            'Monday': None,
            'Tuesday': None,
            'Wednesday': (13, 14, 4),
            'Thursday': (14, 15, 4),
            'Friday': None,
            'Saturday': None,
            'Sunday': None
        },
        'Session': True
    },
    'Patient 3': {
        'Week' : {
            'Monday': None,
            'Tuesday': (14, 15, 5),
            'Wednesday': None,
            'Thursday': None,
            'Friday': (15, 16, 5),
            'Saturday': None,
            'Sunday': None
        },
        'Session': False
    }
}

invoice = {}

# Create a maximization problem
prob = LpProblem("Therapist scheduling", LpMaximize)

days = [day for therapist in therapists.values() for day in therapist['Week'].keys()]
# Define decision variables
x = LpVariable.dicts('x', [(therapist,day,patient,'Group') 
                           for therapist in therapists.keys() 
                           for day in days 
                           for patient in patients.keys()], cat=LpBinary)
print(x)

# Define objective function
prob += lpSum([x[(therapist,day,patient,'Group')] 
               for therapist in therapists.keys() 
               for day in days
               for patient in patients.keys()])

# Patient availability constraint
for patient in patients.keys():
    for day in therapists['Therapist 1']['Week'].keys():
        if patients[patient]['Week'][day] is not None:
            start, end, patient_group = patients[patient]['Week'][day]
            for therapist in therapists.keys():
                if therapists[therapist]['Week'][day] is not None:
                    therapist_group = therapists[therapist]['Week'][day][2]
                    prob += lpSum([x[(therapist,day,patient,'Group')] for therapist in therapists.keys() if therapist_group == patient_group]) <= (end - start) / 0.5

# Therapist availability constraint
for therapist in therapists.keys():
    for day in therapists[therapist]['Week'].keys():
        if therapists[therapist]['Week'][day] is not None:
            start, end, therapist_group = therapists[therapist]['Week'][day]
            for patient in patients.keys():
                if patients[patient]['Week'][day] is not None:
                    patient_group = patients[patient]['Week'][day][2]
                    prob += lpSum([x[(therapist,day,patient,'Group')] for patient in patients.keys() if patient_group == therapist_group]) <= (end - start) / 0.5

# Therapist + patient same group constraint
for therapist in therapists.keys():
    for patient in patients.keys():
        for day in therapists['Therapist 1']['Week'].keys():
            if therapists[therapist]['Week'][day] is not None and patients[patient]['Week'][day] is not None:
                if therapists[therapist]['Week'][day][2] == patients[patient]['Week'][day][2]:
                    prob += lpSum([x[(therapist,day,patient,'Group')] for day in therapists[therapist]['Week'].keys()]) <= 1
                else:
                    prob += lpSum([x[(therapist,day,patient,'Group')] for day in therapists[therapist]['Week'].keys()]) == 0

# Session up to 4 children (check if the child wants a groupsession, if yes, check if the child can be set together with other children)
# Invoice constraint
# Driver constrained (driver available + child needs driver?)

# Solve the problem
status = prob.solve()

# Print the optimal schedule
print(f"Total appointments scheduled: {int(value(prob.objective))}\n")
for patient in patients.keys():
    print(f"Schedule for {patient}:")
    for day in therapists['Therapist 1']['Week'].keys():
        if patients[patient]['Week'][day] is not None:
            start, end, g = patients[patient]['Week'][day]
            scheduled = [therapist for therapist in therapists.keys() if value(x[(therapist,day,patient,'Group')]) == 1]
            if len(scheduled) > 0:
                scheduled_str = ', '.join(scheduled)
                print(f"  {day}: {scheduled_str} ({start}-{end}h)")
    print()