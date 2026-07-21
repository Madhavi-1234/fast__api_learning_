from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List,Dict, Annotated

def Patient(BaseModel):
    name: Annotated([str, Field(max_length= 50, title= "Name of teh Patient",description="Give the name of tha patient within 50 length characters")])
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: float = Field(gt=0,lt=110)
    married: bool
    conatct_details: dict[str, str]
    allergies:List[str]= Field(max_length= 5)

def patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)

patient_info={'name':'Madhavi', 'age':20, 'email':'abc@gmail.com','linkedin_url':'http://linkedin.com/1232','weight':47.5, 'married': False,'allergies':['dust,'],'contact_details':{'phone': '12345678'}}

patient1= Patient(patient_info)

patient_data(patient1)