from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City Name where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, lt=3, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, lt=500, description="Weight of the patient in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / self.height ** 2, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "healthy"
        elif self.bmi < 30:
            return "normal"
        return "obese"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)] = None
    city: Annotated[Optional[str], Field(default=None)] = None
    age: Annotated[Optional[int], Field(default=None, gt=0)] = None
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)] = None
    height: Annotated[Optional[float], Field(default=None, gt=0)] = None
    weight: Annotated[Optional[float], Field(default=None)] = None


def load_data():
    with open("Patient.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open("Patient.json", "w") as f:
        json.dump(data, f, indent=2)


@app.get("/patients/")
def list_patients():
    return load_data()


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {patient_id: data[patient_id]}


@app.post("/create/")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully"})


@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info["id"] = patient_id
    patient_pydantic_info = Patient(**existing_patient_info)
    data[patient_id] = patient_pydantic_info.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=202, content={"message": "Patient Updated Successfully"})


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient deleted successfully"})
