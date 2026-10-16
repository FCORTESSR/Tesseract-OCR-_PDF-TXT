import pytesseract
from pdf2image import convert_from_path
import pytesseract.pytesseract as tess_core
import os
import sys
from datetime import datetime

ruta_pdf = sys.argv[1]
ruta_tesseract = sys.argv[2]
ruta_poppler = sys.argv[3] if len(sys.argv) > 3 else r"C:\poppler\Library\bin"
tessdata_prefix = os.path.join(ruta_tesseract, "tessdata")
pytesseract.pytesseract.tesseract_cmd = os.path.join(ruta_tesseract, "tesseract.exe")
tess_core.DEFAULT_ENCODING = "cp1252"
os.environ["TESSDATA_PREFIX"] = tessdata_prefix

imagenes = convert_from_path(ruta_pdf, poppler_path=ruta_poppler)

texto_total = ""
for img in imagenes:
    texto = pytesseract.image_to_string(img, lang="spa", output_type=pytesseract.Output.STRING)
    texto_total += texto + "\n"

hoy = datetime.now()

# ✅ Guardar TXT en Output\año\mes\dia
carpeta_output = os.path.join(os.path.dirname(os.path.dirname(ruta_pdf)), "Output",
                              str(hoy.year),
                              str(hoy.month).zfill(2),
                              str(hoy.day).zfill(2))
os.makedirs(carpeta_output, exist_ok=True)

nombre_txt = os.path.basename(ruta_pdf).replace(".pdf", "_ocr.txt")
ruta_salida = os.path.join(carpeta_output, nombre_txt)

with open(ruta_salida, "w", encoding="utf-8") as f:
    f.write(texto_total)

# ✅ Mover PDF a Input\año\mes\dia
carpeta_input_fecha = os.path.join(os.path.dirname(ruta_pdf),
                                   str(hoy.year),
                                   str(hoy.month).zfill(2),
                                   str(hoy.day).zfill(2))
os.makedirs(carpeta_input_fecha, exist_ok=True)

ruta_pdf_destino = os.path.join(carpeta_input_fecha, os.path.basename(ruta_pdf))
os.rename(ruta_pdf, ruta_pdf_destino)

print(ruta_salida)