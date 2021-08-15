import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path
import re

# Parse Voluntary Petition from the first bankruptcy filing of the CACB 2001 "100 Sample"
# VoluntaryPetitionPageImageArr = convert_from_path("PDFToParse\\docket 1 - Voluntary petition under chapter 7.pdf",
#     poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
# VoluntaryPetitionImage = VoluntaryPetitionPageImageArr[0]
# VoluntaryPetitionImage.save("ParsedPDFImage\\VoluntaryPetition.png")
import cv2
VoluntaryPetitionImage = cv2.imread('ParsedPDFImage\\VoluntaryPetition.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')
res = ocr_agent.detect(VoluntaryPetitionImage, return_response=True)
layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)

VoluntaryPetitionLayoutTextImage = lp.draw_text(VoluntaryPetitionImage, layout,
    font_size=12, with_box_on_text=True, text_box_width=1)
VoluntaryPetitionLayoutTextImage.save("ParsedPDFImage\\VoluntaryPetitionLayoutTextImage.png")
VoluntaryPetitionLayoutBoxImage = lp.draw_box(VoluntaryPetitionImage, layout, box_width=3)
VoluntaryPetitionLayoutBoxImage.save("ParsedPDFImage\\VoluntaryPetitionLayoutBoxImage.png")

debtor_ZIP_code = layout.filter_by(lp.Rectangle(x_1=100, y_1=510, x_2=750, y_2=600))
DebtorZIPCodeTextImage = lp.draw_text(VoluntaryPetitionImage, debtor_ZIP_code, font_size=16,
    with_box_on_text=True, text_box_width=1)
DebtorZIPCodeTextImage.save("ParsedPDFImage\\DebtorZIPCodeTextImage.png")

for box in debtor_ZIP_code:
    print(box, end='\n---\n')

DataPointDictionary = {}

DataPointRegex = re.compile("[\d\s]+")
i = len(debtor_ZIP_code) - 1
DataPointRegexMatch = DataPointRegex.match(debtor_ZIP_code[i].text)
DebtorZIPCodeString = ""
while DataPointRegexMatch is not None:
    print(debtor_ZIP_code[i].block)
    DebtorZIPCodeString = debtor_ZIP_code[i].text.strip() + DebtorZIPCodeString
    i -= 1
    DataPointRegexMatch = DataPointRegex.match(debtor_ZIP_code[i].text)
DataPointDictionary["Debtor ZIP Code"] = DebtorZIPCodeString

print(DataPointDictionary)
