import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='root',
                                password=None,
                                host='127.0.0.1',
                                database='BankruptcyFiling_DB')
cursor = cnx.cursor()

DB_NAME = 'BankruptcyFiling_DB'
TABLES = {}

TABLES['CACB_100Sample2001_Raw'] = (
    "CREATE TABLE `CACB_100Sample2001_Raw` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `filedDate` varchar(100) NOT NULL,"
    "  `ZIPCode` varchar(100) NOT NULL,"
    "  `totalAssets` varchar(100),"
    "  `totalLiabilities` varchar(100),"
    "  `totalCombinedMonthlyIncome` varchar(100),"
    "  `attoneyFee` varchar(100),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['CACB_100Sample2001_Clean'] = (
    "CREATE TABLE `CACB_100Sample2001_Clean` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `filedDate` date NOT NULL,"
    "  `ZIPCode` int NOT NULL,"
    "  `totalAssets` decimal,"
    "  `totalLiabilities` decimal,"
    "  `totalCombinedMonthlyIncome` decimal,"
    "  `attoneyFee` decimal,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table exists")
        else:
            print(err.msg)
    else:
        print("Table created")

cursor.close()
cnx.close()
