from pulp import *

# Define therapists and their availability
therapists = {
    'Therapist 1': {
        'Group': ['1/hersenletsel', '4/COS'],
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
        'Group': ['5/ADHD'],
        'Week' : {
            'Monday': None,
            'Tuesday': (12, 16),
            'Wednesday': (11, 16),
            'Thursday': (12, 17),
            'Friday': (9, 17),
            'Saturday': None,
            'Sunday': None
        }
    },
    'Therapist 3': {
        'Group': ['4/COS'],
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
        'Group': ['1/hersenletsel'],
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
        'Group': ['4/COS'],
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
        'Group': ['5/ADHD'],
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

# Patient availability constraint
for patient in patients.keys():
    for day in therapists['Therapist 1']['Week'].keys():
        if patients[patient]['Week'][day] is not None:
            start, end = patients[patient]['Week'][day]
            patient_group = patients[patient]['Group']
            prob += lpSum([x[(therapist,day,patient,'Group')] for therapist in therapists.keys() if any(item in therapists[therapist]['Group'] for item in patient_group)]) <= (end - start) / 0.5

# Therapist availability constraint
for therapist in therapists.keys():
    for day in therapists[therapist]['Week'].keys():
        if therapists[therapist]['Week'][day] is None:
            for patient in patients.keys():
                prob += x[(therapist,day,patient,'Group')] == 0
        else:
            start, end = therapists[therapist]['Week'][day]
            prob += lpSum([x[(therapist,day,patient,'Group')] for patient in patients.keys()]) <= (end - start) / 0.5

# One-patient-per-therapist constraint
for therapist in therapists.keys():
    for patient in patients.keys():
        prob += lpSum([x[(therapist,day,patient,'Group')] for day in therapists[therapist]['Week'].keys()]) <= 1

# Therapist + patient same group constraint
for therapist in therapists.keys():
    for patient in patients.keys():
        if any(item in therapists[therapist]['Group'] for item in patients[patient]['Group']):
            prob += lpSum([x[(therapist,day,patient,'Group')] for day in therapists[therapist]['Week'].keys()]) <= 1
        else:
            prob += lpSum([x[(therapist,day,patient,'Group')] for day in therapists[therapist]['Week'].keys()]) == 0

# Solve the problem
status = prob.solve()

# Print the optimal schedule
print(f"Total appointments scheduled: {int(value(prob.objective))}\n")
for patient in patients.keys():
    print(f"Schedule for {patient}:")
    for day in therapists['Therapist 1']['Week'].keys():
        if patients[patient]['Week'][day] is not None:
            start, end = patients[patient]['Week'][day]
            scheduled = [therapist for therapist in therapists.keys() if value(x[(therapist,day,patient,'Group')]) == 1]
            if len(scheduled) > 0:
                scheduled_str = ', '.join(scheduled)
                for therapist in scheduled:
                    if not any(item in therapists[therapist]['Group'] for item in patients[patient]['Group']):
                        print(f"  WARNING: {therapist} has a different group than {patient}")
                print(f"  {day}: {scheduled_str} ({start}-{end}h)")
    print()