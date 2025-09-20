from pydantic import BaseModel

class DataForStudentRegistrationModel(BaseModel):
    firstName: str
    lastName: str
    email: str
    gender: str
    phoneNumber: str
    date_of_birth: str
    subjects: list[str]
    hobbies: list[str]
    pictureFileName: str
    currentAddress: str
    state: str
    city: str
