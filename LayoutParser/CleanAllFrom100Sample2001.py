import re
import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='BankruptcyFiling_DB')
outerCursor = cnx.cursor(buffered=True)
innerCursor = cnx.cursor(buffered=True)

pull_all_raw_bankruptcy_filing = ("SELECT name, filedDate, ZIPCode, totalAssets, "
                            "totalLiabilities, attoneyFee, totalCombinedMonthlyIncome "
                            "FROM CACB_100Sample2001_Raw")

insert_clean_bankruptcy_filing = ("INSERT INTO CACB_100Sample2001_Clean "
                            "(name, filedDate, ZIPCode, totalAssets, "
                            "totalLiabilities, attoneyFee, totalCombinedMonthlyIncome) "
                            "VALUES (%(name)s, %(filedDate)s, %(ZIPCode)s, %(totalAssets)s, "
                            "%(totalLiabilities)s, %(attoneyFee)s, %(totalCombinedMonthlyIncome)s)")

ZIPCodeRegex = re.compile("[\d\s]+")

outerCursor.execute(pull_all_raw_bankruptcy_filing)

for (name, filedDate, ZIPCode, totalAssets, totalLiabilities,
    attoneyFee, totalCombinedMonthlyIncome) in outerCursor:
    ZIPCodeRegexMatch = ZIPCodeRegex.match(ZIPCode)
    CleanBankruptcyFiling = {
        'name': name,
        'filedDate': datetime.strptime(filedDate.strip(' .~'), '%m/%d/%y'),
        'ZIPCode': int(ZIPCode.replace(' ','')) if ZIPCodeRegexMatch else -1,
        'totalAssets': float(totalAssets.strip(' .$').replace(',',''))
            if totalAssets else None,
        'totalLiabilities': float(totalLiabilities.strip(' .$').replace(',',''))
            if totalLiabilities else None,
        'attoneyFee': float(attoneyFee.strip(' .$').replace(',',''))
            if attoneyFee else None,
        'totalCombinedMonthlyIncome': float(totalCombinedMonthlyIncome.strip(' .$').replace(',',''))
            if totalCombinedMonthlyIncome else None,
    }
    innerCursor.execute(insert_clean_bankruptcy_filing, CleanBankruptcyFiling)
    cnx.commit()

innerCursor.close()
outerCursor.close()
cnx.close()
