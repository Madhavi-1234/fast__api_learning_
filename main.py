from fastapi import FastAPI, Path, HTTPException, Query
import json

def load_data():
    with open("Patient.json", "r")as f:
     data= json.load(f)
    return data

app= FastAPI()
@app.get("/")

def hello():
    return {"message":"Patient Management System API"}


@app.get("/about")

def about():
    return {"message": "Fully Functional Patient Managment sytem API to manage your patient records"}


@app.get("/view")

def view():
   data= load_data()
   return data


@app.get("/Patient/{patient_id}")
def patient_view(patient_id: str= Path(..., description= "ID of the patient in DB",example= 'P001')):
    data = load_data()

    if patient_id in data["Patients"]:
        return data["Patients"][patient_id]
    raise HTTPException(status_code = 404, detail= 'Patient Not Found')

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="sort on basis of age, height, weight or bmi"),
    order: str = Query(..., description="sort either in asc or desc order")
):
    
    valid_fields = ["age", "height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order selection between asc and desc"
        )

    data = load_data()

    patients = data.get("patients", [])

    sort_order = True if order == "desc" else False

    sorted_data = sorted(
        patients,
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )

    return sorted_data

@app.get('/edit/{patient_id}')
def edit_patient(patient_id: )


   





