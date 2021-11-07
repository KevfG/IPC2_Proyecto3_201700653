from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=24)

a = 1

lista = [1,2,3,4,5,6,7,8,9, 10]
for i in lista:
    pdf.cell(200, 10, txt=str(i), ln=a, align="C")
    a =+ 1

pdf.output("ejemplo.pdf")
