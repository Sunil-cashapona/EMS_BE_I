from pydantic import BaseModel, ConfigDict
 
 
class UserAddressBase(BaseModel):
    address: str
    city: str
    state: str
    pincode: str
 
 
class UserAddressCreate(UserAddressBase):
    employee_id: int
 
 
class UserAddressUpdate(BaseModel):
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
 
 
class UserAddressResponse(UserAddressBase):
    id: int
    employee_id: int
 
    model_config = ConfigDict(from_attributes=True)