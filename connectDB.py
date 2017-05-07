import sqlite3

def _execute(query,query2=0):
        dbPath = 'chatgame.db'
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()
        try:
                cursorobj.execute(query)
                if(query2!=0):
                        cursorobj.execute(query2)
                result = cursorobj.fetchall()
                connection.commit()
        except Exception:
                raise
        connection.close()
        return result


# def _getLastId(query1,query2):
#         dbPath = 'chatgame.db'
#         connection2 = sqlite3.connect(dbPath)
#         cursorobj2 = connection2.cursor()
#         try:
#                 cursorobj2.execute(query1)
#                 cursorobj2.execute(query2)
#                 result = cursorobj2.fetchall()
#                 connection2.commit()
#         except Exception:
#                 raise
#         connection2.close()
#         print("ok2")
#         return result