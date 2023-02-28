from pulp import *

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

# Initialize the problem
prob = LpProblem("Therapy Scheduling Problem", LpMaximize)

# Define the decision variable x
x = LpVariable.dicts("x", [(t,d,s,p) for t in therapists.keys() for d in days for s in time_slots for p in patients.keys()], cat='Binary')

# Define the objective function
prob += lpSum([x[(therapist,day,time_slot,p)] for therapist in therapists.keys() for day in days for time_slot in time_slots for p in patients.keys()])

# Add the constraints

# Patient availability constraint
for patient in patients.keys():
    for day in days:
        if patients[patient]['Week'][day] is not None:
            start, end, patient_group = patients[patient]['Week'][day]
            prob += lpSum([x[(therapist,day,time_slot,patient)] for therapist in therapists.keys() for time_slot in range(start,end)]) == 1

# Therapist availability constraint
for therapist in therapists.keys():
    for day in days:
        if therapists[therapist]['Week'][day] is not None:
            start, end, therapist_group = therapists[therapist]['Week'][day]
            prob += lpSum([x[(therapist,day,time_slot,p)] for time_slot in range(start,end) for p in patients.keys() if patients[p]['Week'][day] is not None and therapist_group == patients[p]['Week'][day][2]]) <= 1

# Therapist + patient same group constraint
for therapist in therapists.keys():
    for patient in patients.keys():
        for day in days:
            if therapists[therapist]['Week'][day] is not None and patients[patient]['Week'][day] is not None:
                if therapists[therapist]['Week'][day][2] == patients[patient]['Week'][day][2]:
                    prob += lpSum([x[(therapist,day,time_slot,patient)] for time_slot in time_slots]) <= 1
                else:
                    prob += lpSum([x[(therapist,day,time_slot,patient)] for time_slot in time_slots]) == 0

# Therapist + patient no conflict constraint
for therapist in therapists.keys():
    for patient in patients.keys():
        for day in days:
            if therapists[therapist]['Week'][day] is not None and patients[patient]['Week'][day] is not None:
                start_t, end_t, therapist_group = therapists[therapist]['Week'][day]
                start_p, end_p, patient_group = patients[patient]['Week'][day]
                prob += lpSum([x[(therapist,day,time_slot,p)] for p in patients.keys() if p != patient for time_slot in range(start_p,end_p)]) + lpSum([x[(th,d,t,patient)] for th in therapists.keys() if th != therapist for d in days for t in range(start_t,end_t)]) <= (end_p - start_p) / 0.5 + (end_t - start_t) / 0.5

# Solve the problem
prob.solve()

# Print the status of the solution
print("Status:", LpStatus[prob.status])

# Print the optimal schedule
for patient in patients.keys():
    print(f"\nSchedule for {patient}:")
    for day in days:
        for time_slot in time_slots:
            for therapist in therapists.keys():
                if x[(therapist,day,time_slot,patient)].value() == 1:
                    print(f"  {day}: {therapist
