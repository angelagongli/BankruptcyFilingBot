import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path
import re

# Parse Summary of Schedules from the first bankruptcy filing of the CACB 2001 "100 Sample"
# SummaryOfSchedulesPageImageArr = convert_from_path("PDFToParse\\docket 4 - Summary of schedules.pdf",
#     poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
# SummaryOfSchedulesImage = SummaryOfSchedulesPageImageArr[0]
# SummaryOfSchedulesImage.save("ParsedPDFImage\\SummaryOfSchedules.png")
import cv2
SummaryOfSchedulesImage = cv2.imread('ParsedPDFImage\\SummaryOfSchedules.png')

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')
res = ocr_agent.detect(SummaryOfSchedulesImage, return_response=True)
layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)

SummaryOfSchedulesLayoutTextImage = lp.draw_text(SummaryOfSchedulesImage, layout,
    font_size=12, with_box_on_text=True, text_box_width=1)
SummaryOfSchedulesLayoutTextImage.save("ParsedPDFImage\\SummaryOfSchedulesLayoutTextImage.png")
SummaryOfSchedulesLayoutBoxImage = lp.draw_box(SummaryOfSchedulesImage, layout, box_width=3)
SummaryOfSchedulesLayoutBoxImage.save("ParsedPDFImage\\SummaryOfSchedulesLayoutBoxImage.png")

name_of_schedules = layout.filter_by(lp.Rectangle(x_1=100, y_1=700, x_2=500, y_2=1700))
NameOfSchedulesTextImage = lp.draw_text(SummaryOfSchedulesImage, name_of_schedules, font_size=16,
    with_box_on_text=True, text_box_width=1)
NameOfSchedulesTextImage.save("ParsedPDFImage\\NameOfSchedulesTextImage.png")

total_assets = layout.filter_by(lp.Rectangle(x_1=595, y_1=1850, x_2=1100, y_2=1890))
TotalAssetsTextImage = lp.draw_text(SummaryOfSchedulesImage, total_assets, font_size=16,
    with_box_on_text=True, text_box_width=1)
TotalAssetsTextImage.save("ParsedPDFImage\\TotalAssetsTextImage.png")

total_liabilities = layout.filter_by(lp.Rectangle(x_1=850, y_1=1955, x_2=1400, y_2=1990))
TotalLiabilitiesTextImage = lp.draw_text(SummaryOfSchedulesImage, total_liabilities, font_size=16,
    with_box_on_text=True, text_box_width=1)
TotalLiabilitiesTextImage.save("ParsedPDFImage\\TotalLiabilitiesTextImage.png")

for box in layout:
    print(box, end='\n---\n')

DataPointDictionary = {}

DataPointRegex = re.compile("[\d\.,]+")

for i in range(0, len(layout) - 1):
    if (layout[i].text == "Total") & (layout[i + 1].text == "Assets"):
        print(layout[i].block)
        print(layout[i + 1].block)
        j = i + 2
        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        while DataPointRegexMatch is None:
            j += 1
            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        DataPointDictionary["Total Assets"] = layout[j].text
    if (layout[i].text == "Total") & (layout[i + 1].text == "Liabilities"):
        print(layout[i].block)
        print(layout[i + 1].block)
        j = i + 2
        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        while DataPointRegexMatch is None:
            j += 1
            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
        DataPointDictionary["Total Liabilities"] = layout[j].text

print(DataPointDictionary)
