import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path

# Parse Schedule E from the first bankruptcy filing of the CACB 2001 "100 Sample" =>
# Empty bankruptcy filing PDF document containing no identifying information of the filer
ScheduleEPageImageArr = convert_from_path("PDFToParse\\docket 9 - Schedule E filed.pdf",
    poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')

ScheduleEImage = ScheduleEPageImageArr[0]
ScheduleEImage.save("ParsedPDFImage\\ScheduleE.png")

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')
res = ocr_agent.detect(ScheduleEImage, return_response=True)
layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)

ScheduleELayoutTextImage = lp.draw_text(ScheduleEImage, layout,
    font_size=12, with_box_on_text=True, text_box_width=1)
ScheduleELayoutTextImage.save("ParsedPDFImage\\ScheduleELayoutTextImage.png")
ScheduleELayoutBoxImage = lp.draw_box(ScheduleEImage, layout, box_width=3)
ScheduleELayoutBoxImage.save("ParsedPDFImage\\ScheduleELayoutBoxImage.png")

for txt in layout.get_texts():
    print(txt, end='\n---\n')
