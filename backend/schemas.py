from pydantic import BaseModel
from typing import List

class InvoiceEntry(BaseModel):
    TruckNo: str
    LRNo: str
    Date: str
    Quantity: str
    Detention: float
    Particulars: str
    Amount: float

class InvoiceMetadata(BaseModel):
    CompanyName: str
    BillNumber: str
    Source: str
    Destination: str
    InvoiceDate: str

class InvoiceSchema(BaseModel):
    metadata: InvoiceMetadata
    entries: List[InvoiceEntry]
