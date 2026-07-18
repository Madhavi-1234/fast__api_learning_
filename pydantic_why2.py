def insert_patient_data(name, age):

    if (age<0) or (age>150):
         raise ValueError("age should be between 0 and 150")
    else:

         if (type(name)==str) and (type(age)== int):    # fine but not scalable right ?
           print(name),
           print(age),
           print("interested into database")

def update_patient_data(name, age):

    if (type(name)==str) and (type(age)== int):    # fine but not scalable right ?
        print(name),
        print(age),
        print("update into database")



# what if we have 100s of fields to validate ? we need to write 100s of if conditions which is not scalable and also error prone.