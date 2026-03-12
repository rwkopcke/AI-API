# Create a combined PDF travel guide using the uploaded DOCX files and the generated Trieste map
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from pathlib import Path

docx_files = [
    "/mnt/data/chat_trieste_response_2026_03_11a.docx",
    "/mnt/data/gem_trieste_response_2026_03_11.docx"
]

map_path = "/mnt/data/a_map_of_central_trieste_italy_is_displayed_with.png"
output_pdf = "/mnt/data/Trieste_Travel_Guide.pdf"

styles = getSampleStyleSheet()
story = []

# Title page
story.append(Paragraph("Trieste, Italy Travel Planning Guide", styles['Title']))
story.append(Spacer(1,20))
story.append(Paragraph("Hotels, Attractions, Restaurants and Travel Planning Resources", styles['Heading2']))
story.append(Spacer(1,20))
story.append(Paragraph("Compiled from travel research documents and planning notes.", styles['BodyText']))
story.append(Spacer(1,40))

# Insert map if available
if Path(map_path).exists():
    story.append(Paragraph("Map of Central Trieste: Hotels, Attractions and Restaurants", styles['Heading2']))
    story.append(Spacer(1,10))
    story.append(Image(map_path, width=6.5*inch, height=4.5*inch))
    story.append(Spacer(1,30))

story.append(PageBreak())

# Function to add docx text
def add_docx_content(path):
    doc = Document(path)
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            story.append(Spacer(1,8))
        else:
            story.append(Paragraph(text.replace("&","&amp;"), styles['BodyText']))
            story.append(Spacer(1,6))

# Add both documents
for f in docx_files:
    story.append(Paragraph(f"Source Document: {Path(f).name}", styles['Heading2']))
    story.append(Spacer(1,12))
    add_docx_content(f)
    story.append(PageBreak())

# Build PDF
pdf = SimpleDocTemplate(output_pdf, pagesize=letter)
pdf.build(story)

output_pdf