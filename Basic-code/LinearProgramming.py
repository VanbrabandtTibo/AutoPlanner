from pulp import *

# Define therapists and their availability
therapists = {
    'Therapist 1': {
        'Group': ('1/hersenletsel'),
        'Week' : {
            'Monday': (9, 17),
            'Tuesday': (9, 17),
            'Wednesday': (13, 17),
            'Thursday': (10, 15),
            'Friday': None,
            'Saturday': None,
            'Sunday': None
        }
    },
    'Therapist 2': {
        'Group': ('5/ADHD'),
        'Week' : {
            'Monday': None,
            'Tuesday': None,
            'Wednesday': (11, 16),
            'Thursday': (12, 17),
            'Friday': (9, 15),
            'Saturday': None,
            'Sunday': None
        }
    },
    'Therapist 3': {
        'Group': ('4/COS'),
        'Week' : {
            'Monday': (10, 15),
            'Tuesday': (10, 14),
            'Wednesday': (10, 14),
            'Thursday': None,
            'Friday': (9, 16),
            'Saturday': None,
            'Sunday': None
        }
    }
}

# Define patients and their preferred appointment times
patients = {
    'Patient 1': {
        'Group': ('1/hersenletsel'),
        'Week' : {
            'Monday': (10, 11),
            'Tuesday': (12, 13),
            'Wednesday': (15, 16),
            'Thursday': (11, 12),
            'Friday': None,
            'Saturday': None,
            'Sunday': None
        }
    },
    'Patient 2': {
        'Group': ('4/COS'),
        'Week' : {
            'Monday': None,
            'Tuesday': None,
            'Wednesday': (13, 14),
            'Thursday': (14, 15),
            'Friday': None,
            'Saturday': None,
            'Sunday': None
        }
    },
    'Patient 3': {
        'Group': ('5/ADHD'),
        'Week' : {
            'Monday': None,
            'Tuesday': (14, 15),
            'Wednesday': None,
            'Thursday': None,
            'Friday': (15, 16),
            'Saturday': None,
            'Sunday': None
        }
    }
}

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

# Define constraints
for patient in patients.keys():
    for day in therapists['Therapist 1'].keys():
        if patients[patient][day] is not None:
                start, end = patients[patient][day]
                prob += lpSum([x[(therapist,day,patient)] for therapist in therapists.keys()]) <= (end - start) / 0.5

for therapist in therapists.keys():
    for day in therapists[therapist].keys():
        if therapists[therapist][day] is None:
            for patient in patients.keys():
                prob += x[(therapist,day,patient)] == 0
        else:
            start, end = therapists[therapist][day]
            prob += lpSum([x[(therapist,day,patient)] for patient in patients.keys()]) <= (end - start) / 0.5

for therapist in therapists.keys():
    for patient in patients.keys():
        prob += lpSum([x[(therapist,day,patient)] for day in therapists[therapist].keys()]) <= 1

# Solve the problem
status = prob.solve()

# Print the optimal schedule
print(f"Total appointments scheduled: {int(value(prob.objective))}\n")
for patient in patients.keys():
    print(f"Schedule for {patient}:")
    for day in therapists['Therapist 1'].keys():
        if patients[patient][day] is not None:
            start, end = patients[patient][day]
            scheduled = [therapist for therapist in therapists.keys() if value(x[(therapist,day,patient)]) == 1]
            if len(scheduled) > 0:
                scheduled_str = ', '.join(scheduled)
                print(f"  {day}: {scheduled_str} ({start}-{end}h)")
    print()