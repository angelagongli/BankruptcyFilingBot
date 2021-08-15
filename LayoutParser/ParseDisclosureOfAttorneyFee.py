import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path
import re

# Parse Disclosure of Attorney Fees from the first bankruptcy filing of the CACB 2001 "100 Sample"
# DisclosureOfAttorneyFeesPageImageArr = convert_from_path("PDFToParse\\docket 18 - Disclosure of attorney fees.pdf",
#     poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
# DisclosureOfAttorneyFeesImage = DisclosureOfAttorneyFeesPageImageArr[0]
# DisclosureOfAttorneyFeesImage.save("ParsedPDFImage\\DisclosureOfAttorneyFees.png")
import cv2
DisclosureOfAttorneyFeesImage = cv2.imread('ParsedPDFImage\\DisclosureOfAttorneyFees.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')
res = ocr_agent.detect(DisclosureOfAttorneyFeesImage, return_response=True)
layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)

DisclosureOfAttorneyFeesLayoutTextImage = lp.draw_text(DisclosureOfAttorneyFeesImage, layout,
    font_size=12, with_box_on_text=True, text_box_width=1)
DisclosureOfAttorneyFeesLayoutTextImage.save("ParsedPDFImage\\DisclosureOfAttorneyFeesLayoutTextImage.png")
DisclosureOfAttorneyFeesLayoutBoxImage = lp.draw_box(DisclosureOfAttorneyFeesImage, layout, box_width=3)
DisclosureOfAttorneyFeesLayoutBoxImage.save("ParsedPDFImage\\DisclosureOfAttorneyFeesLayoutBoxImage.png")

attorney_fee = layout.filter_by(lp.Rectangle(x_1=140, y_1=1060, x_2=1600, y_2=1110))
AttorneyFeeTextImage = lp.draw_text(DisclosureOfAttorneyFeesImage, attorney_fee, font_size=16,
    with_box_on_text=True, text_box_width=1)
AttorneyFeeTextImage.save("ParsedPDFImage\\AttorneyFeeTextImage.png")

for box in layout:
    print(box, end='\n---\n')

DataPointDictionary = {}

DataPointRegex = re.compile("[\d\.,]+")

for i in range(0, len(layout) - 1):
    if ((layout[i].text == "For" or layout[i].text == "for") &
        (layout[i + 1].text == "legal") &
        (layout[i + 2].text == "services")):
        j = i + 3
        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        while DataPointRegexMatch is None:
            j += 1
            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        DataPointDictionary["Attorney Fee"] = layout[j].text
        print(layout[j].block)
        break

print(DataPointDictionary)
