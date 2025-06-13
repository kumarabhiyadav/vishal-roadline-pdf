from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing  import List, Optional
from fpdf import FPDF
from num2words import num2words
from fastapi.responses import FileResponse
import os
from backend.schemas import InvoiceSchema
from backend.db import invoice_collection
from bson import ObjectId
from pymongo import DESCENDING, ASCENDING
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



# Allow all origins (for development, not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or list specific URLs like ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entry(BaseModel):
    TruckNo: str
    LRNo: str
    Date: str
    Quantity: int
    Detention: int
    Particulars: str
    Amount: int

class InvoiceMetadata(BaseModel):
    CompanyName: str
    BillNumber: str
    Source: str
    Destination: str
    InvoiceDate: str

class InvoiceRequest(BaseModel):
    metadata: InvoiceMetadata
    entries: List[Entry]

@app.post("/generate-invoice")
async def generate_invoice(invoice: InvoiceRequest):

    pdf = FPDF()
    pdf.add_page()
    fontfamily = "helvetica"

    # Header
    pdf.set_font(fontfamily, '', 13.0)
    pdf.set_xy(105.0, 8.0)
    pdf.set_text_color(252, 3, 3)
    pdf.cell(ln=0, align='C', w=1, txt='||Om Sai||', border=0)
    pdf.set_xy(105.0, 13)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(fontfamily, style='BU', size=9)
    pdf.cell(ln=0, align='C', w=1, txt='Subject to Thane Jurisdiction', border=0)
    pdf.set_xy(185, 8.0)
    pdf.set_font(fontfamily, style='B', size=9)
    pdf.cell(ln=0, align='C', w=1, txt='Tel.:(002)-25802718', border=0)
    pdf.set_xy(186, 11)
    pdf.cell(ln=0, align='C', w=1, txt='Mob.:9987198275', border=0)
    pdf.set_xy(190, 14)
    pdf.cell(ln=0, align='C', w=1, txt='9920833549', border=0)
    pdf.set_xy(105.0, 19)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font(fontfamily, style='B', size=20)
    pdf.cell(ln=0, align='C', w=1, txt='VISHAL ROADLINES', border=0)
    pdf.set_xy(105.0, 24)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(fontfamily, style='B', size=9)
    pdf.cell(ln=0, align='C', w=1, txt='Fleet Owners & Transport Contractor', border=0)
    pdf.set_xy(105.0, 27)
    pdf.cell(ln=0, align='C', w=1, txt='Stainless Steel Tanker For Petroleum', border=0)
    pdf.set_xy(105.0, 30)
    pdf.cell(ln=0, align='C', w=1, txt='All Kinds of Oil & Chemical Solvent', border=0)
    pdf.line(10, 32, 200, 32)

    # Metadata info
    pdf.set_xy(10, 44)
    pdf.cell(ln=0, align='L', w=1, txt='Bill No:', border=0)
    pdf.set_xy(22, 44)
    pdf.cell(ln=0, align='L', w=1, txt=invoice.metadata.BillNumber, border=0)

    pdf.set_xy(165, 44)
    pdf.cell(ln=0, align='L', w=1, txt='Date:', border=0)
    pdf.set_xy(175, 44)
    pdf.cell(ln=0, align='L', w=1, txt=invoice.metadata.InvoiceDate, border=0)

    pdf.set_xy(10, 55)
    pdf.cell(ln=0, align='L', w=1, txt='M/s.', border=0)
    pdf.set_xy(20, 55)
    pdf.cell(ln=0, align='L', w=1, txt=invoice.metadata.CompanyName, border=0)

    pdf.set_xy(10, 75)
    pdf.cell(ln=0, align='L', w=1, txt='From:', border=0)
    pdf.line(22, 76, 70, 76)
    pdf.set_xy(30, 74)
    pdf.cell(ln=0, align='L', w=1, txt=invoice.metadata.Source, border=0)

    pdf.set_xy(75, 75)
    pdf.cell(ln=0, align='L', w=1, txt='To:', border=0)
    pdf.line(85, 76, 130, 76)
    pdf.set_xy(85, 74)
    pdf.cell(ln=0, align='L', w=1, txt=invoice.metadata.Destination, border=0)

    pdf.set_xy(192, 61)
    pdf.set_font(fontfamily, style='B', size=14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(ln=0, align='R', w=1, txt='PAN NO.ACGPY 8550 P', border=0)
    pdf.rect(135, 55, 60, 12, 'D')
    pdf.line(20, 57, 130, 57)
    pdf.line(10, 62, 130, 62)
    pdf.line(10, 67, 130, 67)

    pdf.set_xy(105, 70)
    pdf.set_font(fontfamily, style='B', size=9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(ln=0, align='C', w=1, txt='Bearing cost of Transporting Your products in our Tanker as under:', border=0)

    # Draw table frame
    pdf.line(10, 80, 200, 80)  # top line
    pdf.line(10, 250, 10, 80)  # left line
    pdf.line(10, 250, 200, 250)  # bottom line
    pdf.line(200, 80, 200, 250)  # right line
    pdf.line(10, 85, 200, 85)  # top secondary line

    # Lines for columns
    for x in [35, 60, 80, 98, 120, 180]:
        pdf.line(x, 80, x, 250)

    # Table headers
    headers = ['Truck No.', 'LR No.', 'Date', 'Quantity', 'Detention(Rs)', 'PARTICULARS', 'Amount(Rs.)']
    header_positions = [18, 42, 65, 88, 109, 135, 190]
    for i, header in enumerate(headers):
        pdf.set_xy(header_positions[i], 83)
        pdf.cell(ln=0, align='C', w=1, txt=header, border=0)

    pdf.set_xy(170, 248)
    pdf.cell(ln=0, align='C', w=1, txt='Total Rs.', border=0)
    pdf.line(180, 245, 200, 245)

    pdf.set_xy(25, 260)
    pdf.cell(ln=0, align='C', w=1, txt='Rupees:', border=0)
    pdf.line(35, 262, 140, 262)
    pdf.line(35, 268, 140, 268)

    pdf.set_xy(180, 255)
    pdf.set_text_color(255, 0, 0)
    pdf.set_font(fontfamily, style='B', size=10)
    pdf.cell(ln=0, align='C', w=1, txt='For VISHAL ROADLINES', border=0)

    pdf.set_xy(190, 276)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(fontfamily, style='B', size=9)
    pdf.cell(ln=0, align='C', w=1, txt='Proprietor', border=0)

    pdf.set_xy(20, 276)
    pdf.cell(ln=0, align='C', w=1, txt='E.&. O.E.', border=0)

    # Fill table rows
    y_position = 90
    total_amount = 0
    for entry in invoice.entries:
        pdf.set_xy(22, y_position)
        pdf.cell(ln=0, align='C', w=1, txt=entry.TruckNo, border=0)
        pdf.set_xy(44, y_position)
        pdf.cell(ln=0, align='C', w=1, txt=entry.LRNo, border=0)
        pdf.set_xy(70, y_position)
        pdf.cell(ln=0, align='C', w=1, txt=entry.Date, border=0)
        pdf.set_xy(90, y_position)
        pdf.cell(ln=0, align='C', w=1, txt=str(entry.Quantity)+ 'KG', border=0)
        pdf.set_xy(111, y_position)
        pdf.cell(ln=0, align='C', w=1, txt=str(entry.Detention), border=0)
        y_position -= 1.5
        pdf.set_xy(120, y_position)
        pdf.multi_cell(60, 3, txt=entry.Particulars, border=0)
        y_position += 1.5
        pdf.set_xy(192, y_position)
        pdf.cell(ln=0, align='C', w=1, txt=f"{entry.Amount}.00", border=0)
        y_position += 10
        total_amount += entry.Amount

    # Total amount
    pdf.set_xy(190, 248)
    pdf.cell(ln=0, align='C', w=1, txt=f"{total_amount}.00", border=0)

    # Amount in words
    total_in_words = num2words(total_amount,lang='en_IN').upper()
    pdf.set_xy(35, 257)
    pdf.multi_cell(100, 6, txt=total_in_words, border=0)

    # Save pdf
    save_dir = "invoices"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{invoice.metadata.BillNumber}.pdf"
    filepath = os.path.join(save_dir, filename)
    pdf.output(filepath, "F")

    invoice_data = invoice.model_dump()
    invoice_data["createdAt"] = datetime.utcnow()
    invoice_data["updatedAt"] = datetime.utcnow()
    
    existing = await invoice_collection.find_one({"metadata.BillNumber": invoice.metadata.BillNumber})
    print('Invoice already exists:', existing)
    if not existing:
        print('Inserting new invoice')
        result = await invoice_collection.insert_one(invoice_data)

    return FileResponse(path=filepath, filename=filename, media_type='application/pdf')

def serialize_invoice(invoice):
    invoice["_id"] = str(invoice["_id"])
    return invoice



@app.get("/invoices")
async def get_invoice_history(
    search: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    sort_by: str = Query("createdAt"),
    sort_dir: str = Query("desc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    try:
        # Build query
        query = {}
        
        # Search filter
        if search:
            query["$or"] = [
                {"metadata.BillNumber": {"$regex": search, "$options": "i"}},
                {"metadata.CompanyName": {"$regex": search, "$options": "i"}},
                {"metadata.Source": {"$regex": search, "$options": "i"}},
                {"metadata.Destination": {"$regex": search, "$options": "i"}}
            ]
        
        # Date filter
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = datetime.fromisoformat(start_date)
            if end_date:
                date_query["$lte"] = datetime.fromisoformat(end_date)
            query["metadata.InvoiceDate"] = date_query
        
        # Sort direction
        sort_direction = DESCENDING if sort_dir == "desc" else ASCENDING
        
        # Get total count
        total = await invoice_collection.count_documents(query)
        
        # Execute query
        cursor = (
            invoice_collection.find(query)
            .sort(sort_by, sort_direction)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
        
        invoices = [serialize_invoice(invoice) for invoice in await cursor.to_list(length=None)]
        
        return {
            "invoices": invoices,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: str):
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(invoice_id)
        
        # Try to delete the invoice
        result = await invoice_collection.delete_one({"_id": obj_id})
        
        # Check if a document was actually deleted
        if result.deleted_count == 1:
            return {"message": "Invoice deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Invoice not found")
            
    except Exception as e:
        # Handle invalid ObjectId format or other errors
        raise HTTPException(status_code=400, detail=str(e))
    

    