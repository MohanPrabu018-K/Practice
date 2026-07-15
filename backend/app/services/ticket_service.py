"""QR code and PDF ticket generation services."""
import io, base64, qrcode
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generate_qr_base64(data: str, size: int = 200) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def generate_ticket_pdf(booking: dict) -> bytes:
    buf = io.BytesIO()
    w, h = A6  # 105mm x 148mm
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.setTitle(f"Ticket - {booking['booking_reference']}")
    c.setFillColor(HexColor("#0f0f1a")); c.rect(0, 0, w, h, fill=True, stroke=False)
    c.setFillColor(HexColor("#7b4fbf")); c.rect(0, h - 28*mm, w, 28*mm, fill=True, stroke=False)
    c.setFillColor(HexColor("#ffffff")); c.setFont("Helvetica-Bold", 16)
    c.drawString(6*mm, h-12*mm, "MovieBooker"); c.setFont("Helvetica", 9)
    c.drawString(6*mm, h-20*mm, "CINEMA TICKET"); c.setFont("Helvetica-Bold", 12)
    c.drawRightString(w-6*mm, h-12*mm, booking['booking_reference'])
    c.setFillColor(HexColor("#e0aaff")); c.setFont("Helvetica-Bold", 14)
    c.drawString(6*mm, h-38*mm, booking.get('movie_title','N/A'))
    c.setFillColor(HexColor("#aab")); c.setFont("Helvetica", 8)
    y = h-48*mm
    for lbl, val in [("Theatre", booking.get('hall_name','')),("Screen", booking.get('screen_name','')),("Date & Time", booking.get('show_time_str','')),("Seats", ', '.join(booking.get('seats',[]))),("Amount", f"INR {booking.get('total_amount',0):.2f}"),("Status", booking.get('status','confirmed').upper())]:
        c.setFillColor(HexColor("#888")); c.drawString(6*mm, y, f"{lbl}:")
        c.setFillColor(HexColor("#e4e4f0")); c.drawString(32*mm, y, str(val)); y -= 7*mm
    qr_data = f"MOVIEBOOKER|{booking['booking_reference']}|{booking.get('movie_title','')}"
    qr_bytes = base64.b64decode(generate_qr_base64(qr_data, 180))
    qr_img = ImageReader(io.BytesIO(qr_bytes))
    c.drawImage(qr_img, w-42*mm, 25*mm, width=38*mm, height=38*mm)
    c.setFillColor(HexColor("#555")); c.setFont("Helvetica", 6)
    c.drawCentredString(w/2, 10*mm, "Computer-generated ticket. Present QR code at entrance.")
    c.drawCentredString(w/2, 6*mm, f"Booked: {booking.get('booking_time_str','')}")
    c.save(); buf.seek(0); return buf.read()
