import sqlite3

tableName= "#"
dbName = "#"

islem = int(input("""Yapılacak işlemi Giriniz"
                ------------------------------------
                DIKKAT!! Yapılacak olan tüm işlemler tableName ve dbName adlı değişkenler üzerinde gerçekleşecektir .
                ------------------------------------
                0-Iptal
                1-Tablo oluştur
                2-Tüm tablo içeriğini sil
                3-Tüm tabloyu listele
"""))


def SqlClearTable():
    connection = sqlite3.connect(dbName)
    command = connection.cursor()
    command.execute(f"delete from {tableName}")
    command.execute(f"select * from {tableName}")
    connection.commit()
    connection.close()
def SqlSelectAllTable():
    connection = sqlite3.connect(dbName)
    command = connection.cursor()
    command.execute(f"select * from {tableName}")
    fetched =command.fetchall()
    connection.commit()
    connection.close()
    return fetched
def SqlTableCreate():
    connection = sqlite3.connect(dbName)
    command = connection.cursor()
    command.execute(f"""create table {tableName}(
                    kelime text,
                    anlam text
                    )""")
    connection.commit()
    connection.close()

match islem:
    case 0  :
        print("İptal Edildi.")
    case 1  :
        SqlTableCreate()
        print("Tablo oluştu")
    case 2 :
        SqlClearTable()      
        print("Tablo içeriği silindi")   
    case 3 :
        SqlSelectAllTable()

