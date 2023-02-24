import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Input, Dense, Embedding, Flatten, Concatenate
from tensorflow.keras.models import Model

# Load data
therapists_df = pd.read_csv('therapists.csv')
patients_df = pd.read_csv('patients.csv')
appointments_df = pd.read_csv('appointments.csv')

# Preprocess data
le = LabelEncoder()
therapists_df['id'] = le.fit_transform(therapists_df['id'])
patients_df['id'] = le.fit_transform(patients_df['id'])
therapists_df['expertise'] = le.fit_transform(therapists_df['expertise'])
patients_df['preferences'] = le.fit_transform(patients_df['preferences'])

# Merge data
appointments_df['patient_id'] = le.fit_transform(appointments_df['patient_id'])
appointments_df['therapist_id'] = le.fit_transform(appointments_df['therapist_id'])
appointments_df = appointments_df.merge(patients_df, left_on='patient_id', right_on='id')
appointments_df = appointments_df.merge(therapists_df, left_on='therapist_id', right_on='id')

# Split data into train and test sets
train_df, test_df = train_test_split(appointments_df, test_size=0.2)

# Define neural network architecture
num_therapists = len(therapists_df['id'].unique())
num_preferences = len(patients_df['preferences'].unique())

therapist_input = Input(shape=(1,))
therapist_embedding = Embedding(num_therapists, 10)(therapist_input)
therapist_embedding = Flatten()(therapist_embedding)

preference_input = Input(shape=(1,))
preference_embedding = Embedding(num_preferences, 10)(preference_input)
preference_embedding = Flatten()(preference_embedding)

concatenated = Concatenate()([therapist_embedding, preference_embedding])
dense1 = Dense(64, activation='relu')(concatenated)
dense2 = Dense(32, activation='relu')(dense1)
output = Dense(num_therapists, activation='softmax')(dense2)

model = Model(inputs=[therapist_input, preference_input], outputs=output)

# Train neural network
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit([train_df['therapist_id'], train_df['preference_id']], train_df['therapist_id'], batch_size=32, epochs=10, validation_data=([test_df['therapist_id'], test_df['preference_id']], test_df['therapist_id']))

# Evaluate neural network
loss, accuracy = model.evaluate([test_df['therapist_id'], test_df['preference_id']], test_df['therapist_id'], verbose=0)
print(f'Test accuracy: {accuracy}')

# Generate full schedule with hours
schedule_df = pd.DataFrame(columns=['therapist_id', 'patient_id', 'start_time', 'end_time'])

for patient_id in patients_df['id'].unique():
    patient_df = appointments_df[appointments_df['patient_id'] == patient_id].iloc[0]
    new_appointment = {'patient_id': patient_id, 'therapist_id': None, 'start_time': None, 'end_time': None}
    new_appointment_df = pd.DataFrame([new_appointment])
    new_appointment_df['preferences'] = le.transform(new_appointment_df['preferences'])
    recommendations = model.predict([new_appointment_df['therapist_id'], new_appointment_df['preferences']])
    therapist_id = np.argmax(recommendations)
    therapist_df = therapists_df[therapists_df['id'] == therapist_id].iloc[0]
    start_time = pd.Timestamp('2023-02-23 09:00:00')
    end_time = pd.Timestamp('2023-02-23 10:00:00')
    appointment = {'therapist_id': therapist_id, 'patient_id': patient_id, 'start_time': start_time, 'end_time': end_time}
    schedule_df = schedule_df.append(appointment, ignore_index=True)
    for i in range(1, patient_df['duration']):
        start_time += pd.Timedelta(minutes=30)
        end_time += pd.Timedelta(minutes=30)
        appointment = {'therapist_id': therapist_id, 'patient_id': patient_id, 'start_time': start_time, 'end_time': end_time}
        schedule_df = schedule_df.append(appointment, ignore_index=True)

# Print schedule
print(schedule_df)