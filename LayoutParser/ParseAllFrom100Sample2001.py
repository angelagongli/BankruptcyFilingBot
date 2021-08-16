import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path
import re
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')

root = 'C:\\Users\\angel\\Documents\\Automation\\CACB'
if not os.path.isdir(os.path.join(root, 'LayoutParserOutput')):
    os.mkdir(os.path.join(root, 'LayoutParserOutput'))
for folder in os.listdir(os.path.join(root, '100 sample\\2001')):
    fullBankruptcyFilingFolderPath = os.path.join(
        root, '100 sample\\2001', folder)
    print(fullBankruptcyFilingFolderPath)
    if not os.path.isdir(os.path.join(root, 'LayoutParserOutput', folder)):
        os.mkdir(os.path.join(root, 'LayoutParserOutput', folder))
    if os.path.isdir(fullBankruptcyFilingFolderPath):
        DataPointDictionary = {}
        for file in os.listdir(fullBankruptcyFilingFolderPath):
            if "Voluntary petition" in file:
                VoluntaryPetitionPageImageArr = convert_from_path(
                    os.path.join(fullBankruptcyFilingFolderPath, file),
                    poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
                VoluntaryPetitionImage = VoluntaryPetitionPageImageArr[0]
                res = ocr_agent.detect(VoluntaryPetitionImage, return_response=True)
                layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)
                VoluntaryPetitionLayoutTextImage = lp.draw_text(VoluntaryPetitionImage, layout,
                    font_size=12, with_box_on_text=True, text_box_width=1)
                VoluntaryPetitionLayoutTextImage.save(
                    os.path.join(root, 'LayoutParserOutput', folder,
                    'VoluntaryPetitionLayoutTextImage.png'))
            elif "Summary of schedules" in file:
                SummaryOfSchedulesPageImageArr = convert_from_path(
                    os.path.join(fullBankruptcyFilingFolderPath, file),
                    poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
                SummaryOfSchedulesImage = SummaryOfSchedulesPageImageArr[0]
                res = ocr_agent.detect(SummaryOfSchedulesImage, return_response=True)
                layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)
                SummaryOfSchedulesLayoutTextImage = lp.draw_text(SummaryOfSchedulesImage, layout,
                    font_size=12, with_box_on_text=True, text_box_width=1)
                SummaryOfSchedulesLayoutTextImage.save(
                    os.path.join(root, 'LayoutParserOutput', folder,
                    'SummaryOfSchedulesLayoutTextImage.png'))
                DataPointRegex = re.compile("[\d\.,]+")
                for i in range(0, len(layout) - 1):
                    if layout[i].text == "Total" and layout[i + 1].text == "Assets":
                        j = i + 2
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        DataPointDictionary["Total Assets"] = layout[j].text
                    if layout[i].text == "Total" and layout[i + 1].text == "Liabilities":
                        j = i + 2
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        DataPointDictionary["Total Liabilities"] = layout[j].text
            elif "Schedule I" in file:
                ScheduleIPageImageArr = convert_from_path(
                    os.path.join(fullBankruptcyFilingFolderPath, file),
                    poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
                ScheduleIImage = ScheduleIPageImageArr[0]
                res = ocr_agent.detect(ScheduleIImage, return_response=True)
                layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)
                ScheduleILayoutTextImage = lp.draw_text(ScheduleIImage, layout,
                    font_size=12, with_box_on_text=True, text_box_width=1)
                ScheduleILayoutTextImage.save(
                    os.path.join(root, 'LayoutParserOutput', folder,
                    'ScheduleILayoutTextImage.png'))
                DataPointRegex = re.compile("[\d\.,\$]+")
                for i in range(0, len(layout) - 1):
                    if (layout[i].text == "TOTAL" and
                        layout[i + 1].text == "COMBINED" and
                        layout[i + 2].text == "MONTHLY" and
                        layout[i + 3].text == "INCOME"):
                        j = i + 4
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        TotalCombinedMonthlyIncomeString = ""
                        while DataPointRegexMatch is not None:
                            TotalCombinedMonthlyIncomeString += layout[j].text
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        DataPointDictionary["Total Combined Monthly Income"] = TotalCombinedMonthlyIncomeString
                        break
            elif "Disclosure of attorney fee" in file:
                DisclosureOfAttorneyFeesPageImageArr = convert_from_path(
                    os.path.join(fullBankruptcyFilingFolderPath, file),
                    poppler_path=r'C:\\Program Files\\Poppler21.03.0\\Library\\bin')
                DisclosureOfAttorneyFeesImage = DisclosureOfAttorneyFeesPageImageArr[0]
                res = ocr_agent.detect(DisclosureOfAttorneyFeesImage, return_response=True)
                layout = ocr_agent.gather_data(res, agg_level=lp.TesseractFeatureType.WORD)
                DisclosureOfAttorneyFeesLayoutTextImage = lp.draw_text(DisclosureOfAttorneyFeesImage, layout,
                    font_size=12, with_box_on_text=True, text_box_width=1)
                DisclosureOfAttorneyFeesLayoutTextImage.save(
                    os.path.join(root, 'LayoutParserOutput', folder,
                    'DisclosureOfAttorneyFeesLayoutTextImage.png'))
                DataPointRegex = re.compile("[\d\.,]+")
                for i in range(0, len(layout) - 1):
                    if ((layout[i].text == "For" or layout[i].text == "for") and
                        layout[i + 1].text == "legal" and
                        layout[i + 2].text == "services"):
                        j = i + 3
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        DataPointDictionary["Attorney Fee"] = layout[j].text
                        break
        print(DataPointDictionary)
