import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path
import re

# Parse Schedule I from the first bankruptcy filing of the CACB 2001 "100 Sample"
# ScheduleIPageImageArr = convert_from_path("PDFToParse\\docket 13 - Schedule I filed.pdf",
#     poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
# ScheduleIImage = ScheduleIPageImageArr[0]
# ScheduleIImage.save("ParsedPDFImage\\ScheduleI.png")
import cv2
ScheduleIImage = cv2.imread('ParsedPDFImage\\ScheduleI.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')
res = ocr_agent.detect(ScheduleIImage, return_response=True)
layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)

ScheduleILayoutTextImage = lp.draw_text(ScheduleIImage, layout,
    font_size=12, with_box_on_text=True, text_box_width=1)
ScheduleILayoutTextImage.save("ParsedPDFImage\\ScheduleILayoutTextImage.png")
ScheduleILayoutBoxImage = lp.draw_box(ScheduleIImage, layout, box_width=3)
ScheduleILayoutBoxImage.save("ParsedPDFImage\\ScheduleILayoutBoxImage.png")

total_combined_monthly_income = layout.filter_by(lp.Rectangle(x_1=120, y_1=1960, x_2=820, y_2=2000))
TotalCombinedMonthlyIncomeTextImage = lp.draw_text(ScheduleIImage, total_combined_monthly_income, font_size=16,
    with_box_on_text=True, text_box_width=1)
TotalCombinedMonthlyIncomeTextImage.save("ParsedPDFImage\\TotalCombinedMonthlyIncomeTextImage.png")

for box in layout:
    print(box, end='\n---\n')

DataPointDictionary = {}

DataPointRegex = re.compile("[\d\.,\$]+")

for i in range(0, len(layout) - 1):
    if ((layout[i].text == "TOTAL") &
        (layout[i + 1].text == "COMBINED") &
        (layout[i + 2].text == "MONTHLY") &
        (layout[i + 3].text == "INCOME")):
        j = i + 4
        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        while DataPointRegexMatch is None:
            j += 1
            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        TotalCombinedMonthlyIncomeString = ""
        while DataPointRegexMatch is not None:
            print(layout[j].block)
            TotalCombinedMonthlyIncomeString += layout[j].text
            j += 1
            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        DataPointDictionary["Total Combined Monthly Income"] = TotalCombinedMonthlyIncomeString
        break

print(DataPointDictionary)
