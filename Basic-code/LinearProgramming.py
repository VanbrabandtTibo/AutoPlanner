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

# Create a maximization problem
prob = LpProblem("Therapist scheduling", LpMaximize)

days = [day for therapist in therapists.values() for day in therapist['Week'].keys()]

# Decision variables
x = LpVariable.dicts("Therapist", [(therapist,day,patient) 
                                   for therapist in therapists.keys() 
                                   for day in days 
                                   for patient in patients.keys()], cat='LpBinary')

# Define objective function
prob += lpSum([x[(therapist,day,patient)] 
               for therapist in therapists.keys() 
               for day in days
               for patient in patients.keys()])

# Constraint to look if a patient can be scheduled on a day and time slot by a therapist
for patient in patients.keys():
    for day in days:
        if patients[patient]['Week'][day] is not None:
            start, end, g = patients[patient]['Week'][day]
            prob += lpSum([x[(therapist,day,patient)] 
                           for therapist in therapists.keys() 
                           if therapists[therapist]['Week'][day] is not None 
                           and therapists[therapist]['Week'][day][0] <= start 
                           and therapists[therapist]['Week'][day][1] >= end]) == 1

# Constraint to look if a patient has the same group as the therapist
for patient in patients.keys():
    for day in days:
        if patients[patient]['Week'][day] is not None:
            start, end, g = patients[patient]['Week'][day]
            prob += lpSum([x[(therapist,day,patient)] 
                           for therapist in therapists.keys() 
                           if therapists[therapist]['Week'][day] is not None 
                           and therapists[therapist]['Week'][day][2] == g]) == 1

# Solve the problem
status = prob.solve()
print("Status:", LpStatus[status])

# Print the optimal schedule
print(f"Total appointments scheduled: {int(value(prob.objective))}\n")
for patient in patients.keys():
    print(f"Schedule for {patient}:")
    for day in therapists['Therapist 1']['Week'].keys():
        if patients[patient]['Week'][day] is not None:
            start, end, g = patients[patient]['Week'][day]
            scheduled = [therapist for therapist in therapists.keys() if value(x[(therapist,day,patient)]) == 1]
            if len(scheduled) > 0:
                scheduled_str = ', '.join(scheduled)
                print(f"  {day}: {scheduled_str} ({start}-{end}h)")
    print()