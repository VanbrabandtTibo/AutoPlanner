from fastapi import FastAPI
import uvicorn
from classdir.TherapistScheduling import TherapistScheduler
import json

app = FastAPI()

@app.get("/api/planning")
async def getPlanning():
    ts = TherapistScheduler()
    ts.solve()
    pJSON = ts.get_schedule()
    return {json.dumps(pJSON)}

from typing import Dict, Optional, Tuple
from pydantic import BaseModel

class TherapistSchedule(BaseModel):
    Monday: Optional[Tuple[int, int]]
    Tuesday: Optional[Tuple[int, int]]
    Wednesday: Optional[Tuple[int, int]]
    Thursday: Optional[Tuple[int, int]]
    Friday: Optional[Tuple[int, int]]
    Saturday: Optional[Tuple[int, int]]
    Sunday: Optional[Tuple[int, int]]

class TherapistsDict(BaseModel):
    __root__: Dict[str, TherapistSchedule]

class PatientSchedule(BaseModel):
    Monday: Optional[Tuple[int, int]]
    Tuesday: Optional[Tuple[int, int]]
    Wednesday: Optional[Tuple[int, int]]
    Thursday: Optional[Tuple[int, int]]
    Friday: Optional[Tuple[int, int]]
    Saturday: Optional[Tuple[int, int]]
    Sunday: Optional[Tuple[int, int]]

class PatientsDict(BaseModel):
    __root__: Dict[str, PatientSchedule]

@app.post("/api/planning")
async def setPlanning(therapists: TherapistsDict, patients: PatientsDict):
    t_dict = {}
    for name, therapist in therapists.dict().items():
        t_dict[name] = {
            'Monday': therapist['Monday'],
            'Tuesday': therapist['Tuesday'],
            'Wednesday': therapist['Wednesday'],
            'Thursday': therapist['Thursday'],
            'Friday': therapist['Friday'],
            'Saturday': therapist['Saturday'],
            'Sunday': therapist['Sunday']
        }

    p_dict = {}
    for name, patient in patients.dict().items():
        p_dict[name] = {
            'Monday': patient['Monday'],
            'Tuesday': patient['Tuesday'],
            'Wednesday': patient['Wednesday'],
            'Thursday': patient['Thursday'],
            'Friday': patient['Friday'],
            'Saturday': patient['Saturday'],
            'Sunday': patient['Sunday']
        }

    ts = TherapistScheduler(t_dict, p_dict)
    ts.solve()
    pJSON = ts.get_schedule()
    return {json.dumps(pJSON)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)