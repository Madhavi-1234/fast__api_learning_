from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator, computed_field
from typing import List, Dict

# Model
class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    height: float # mtrs
    weight: float = Field(gt=0, lt=110)   #kg
    married: bool
    contact_details: Dict[str, str]
    allergies: List[str] = Field(max_length=5)

    # validator inside class

    @model_validator(mode='after')
    @classmethod

    def validate_emergency_contacts(cls, model):
        if model.age>60 and 'emergency'not in model.contact_details:
         raise ValueError("Patient older then 60 must have emergency contact")
        return model
    
    @computed_field
    @property

    def calculate_bmi(self)->float:
      bmi= round(self.weight/(self.height **2))
      return bmi

   
    
    



# function
def patient_data(patient: Patient):
    print("Name:", patient.name)
    print("Age:", patient.age)
    print('BMI',patient.calculate_bmi)


# input data
patient_info = {
    'name': 'Madhavi',
    'age': 70,
    'email': 'abc@hdfc'
    '.com',  # fixed domain
    'linkedin_url': 'http://linkedin.com/1232',
    'height':45.8,
    'weight': 47.5,
    'married': False,
    'allergies': ['dust'],
    'contact_details': {'phone': '12345678'}
}

# create object
patient1 = Patient(**patient_info)

# call function
patient_data(patient1)
