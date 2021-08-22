import layoutparser as lp
import pytesseract
from pdf2image import convert_from_path
import re
import os
import mysql.connector

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
ocr_agent = lp.TesseractAgent(languages='eng')

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='BankruptcyFiling_DB')
cursor = cnx.cursor()

insert_raw_bankruptcy_filing = ("INSERT INTO CACB_100Sample2001_Raw "
    "(name, filedDate, ZIPCode, totalAssets, "
    "totalLiabilities, attoneyFee, totalCombinedMonthlyIncome) "
    "VALUES (%(name)s, %(filedDate)s, %(ZIPCode)s, %(totalAssets)s, "
    "%(totalLiabilities)s, %(attoneyFee)s, %(totalCombinedMonthlyIncome)s)")

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
        RawBankruptcyFiling = {
            'name': folder.split(" =")[0]
        }
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
                # Define the Box Containing the Filer's Address:
                address_box_x_1 = 0
                address_box_x_2 = 0
                address_box_y_1 = 0
                address_box_y_2 = 0
                for i in range(0, len(layout) - 1):
                    if layout[i].text.upper() == "FILED":
                        RawBankruptcyFiling["filedDate"] = layout[i + 1].text
                    elif ("STREET" in layout[i].text.upper() and
                        "ADDRESS" in layout[i + 1].text.upper() and
                        address_box_x_1 == 0):
                        address_box_x_1 = layout[i].block.x_1
                        address_box_y_1 = layout[i].block.y_1
                    elif ("ZIP" in layout[i].text.upper() and
                        "CODE" in layout[i + 1].text.upper() and
                        address_box_x_2 == 0):
                        address_box_x_2 = layout[i + 1].block.x_2
                        address_box_y_1 = min(address_box_y_1, layout[i + 1].block.y_1)
                    elif "COUNTY" in layout[i].text.upper():
                        # Stop at the top of the first County of Residence box
                        address_box_y_2 = layout[i].block.y_1
                        break
                    # Much better chance that the person is not named
                    # Street Address/ZIP Code though it is still possible
                debtor_ZIP_code = layout.filter_by(
                    lp.Rectangle(x_1=address_box_x_1, y_1=address_box_y_1,
                                x_2=address_box_x_2, y_2=address_box_y_2))
                DebtorZIPCodeTextImage = lp.draw_text(VoluntaryPetitionImage,
                    debtor_ZIP_code, font_size=16,
                    with_box_on_text=True, text_box_width=1)
                DebtorZIPCodeTextImage.save(
                    os.path.join(root, 'LayoutParserOutput', folder,
                    'DebtorZIPCodeTextImage.png'))
                DataPointRegex = re.compile("[\d\s]+")
                i = len(debtor_ZIP_code) - 1
                DataPointRegexMatch = DataPointRegex.match(debtor_ZIP_code[i].text)
                DebtorZIPCodeString = ""
                while DataPointRegexMatch is not None:
                    DebtorZIPCodeString = debtor_ZIP_code[i].text.strip() + DebtorZIPCodeString
                    i -= 1
                    DataPointRegexMatch = DataPointRegex.match(debtor_ZIP_code[i].text)
                RawBankruptcyFiling["ZIPCode"] = DebtorZIPCodeString
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
                    if layout[i].text.upper() == "TOTAL" and layout[i + 1].text.upper() == "ASSETS":
                        j = i + 2
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        RawBankruptcyFiling["totalAssets"] = layout[j].text
                    if layout[i].text.upper() == "TOTAL" and layout[i + 1].text.upper() == "LIABILITIES":
                        j = i + 2
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        RawBankruptcyFiling["totalLiabilities"] = layout[j].text
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
                    if (layout[i].text.upper() == "TOTAL" and
                        layout[i + 1].text.upper() == "COMBINED" and
                        layout[i + 2].text.upper() == "MONTHLY" and
                        layout[i + 3].text.upper() == "INCOME"):
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
                        RawBankruptcyFiling["totalCombinedMonthlyIncome"] = TotalCombinedMonthlyIncomeString
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
                    if (layout[i].text.upper() == "FOR" and
                        layout[i + 1].text.upper() == "LEGAL" and
                        layout[i + 2].text.upper() == "SERVICES"):
                        j = i + 3
                        DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        while DataPointRegexMatch is None:
                            j += 1
                            DataPointRegexMatch = DataPointRegex.match(layout[j].text)
                        RawBankruptcyFiling["attoneyFee"] = layout[j].text
                        break
        print(RawBankruptcyFiling)
        if ('name' not in RawBankruptcyFiling or
            'filedDate' not in RawBankruptcyFiling or
            'ZIPCode' not in RawBankruptcyFiling):
            continue
        if 'totalAssets' not in RawBankruptcyFiling:
            RawBankruptcyFiling['totalAssets'] = None
        if 'totalLiabilities' not in RawBankruptcyFiling:
            RawBankruptcyFiling['totalLiabilities'] = None
        if 'attoneyFee' not in RawBankruptcyFiling:
            RawBankruptcyFiling['attoneyFee'] = None
        if 'totalCombinedMonthlyIncome' not in RawBankruptcyFiling:
            RawBankruptcyFiling['totalCombinedMonthlyIncome'] = None
    cursor.execute(insert_raw_bankruptcy_filing, RawBankruptcyFiling)
    cnx.commit()

cursor.close()
cnx.close()
