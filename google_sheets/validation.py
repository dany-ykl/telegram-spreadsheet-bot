from pydantic import BaseModel
from .spreadsheet import GoogleSheet

class Entry(BaseModel):
    email: str
    tablename: str
    entry_id: str
    date_entry: str
    date_exit: str
    name_renter: str
    phone: str
    amount: str

    class Config:
        arbitrary_types_allowed = True

class EntryId(BaseModel):
    email: str
    tablename: str
    entry_id: str
