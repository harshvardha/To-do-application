import sqlite3
class DatabaseManager:
    def __init__(self, databaseFilePath):
        self._databaseFileName = databaseFilePath
        self._connection = sqlite3.connect(self._databaseFileName)
    
    def insertIntoTable(self, columnValues: dict):
        valuesList = []
        for value in columnValues.values():
            valuesList.append(value)
        insertQuery = "INSERT INTO task(taskName,taskStartingDate,taskEndingDate,taskDescription)VALUES(?,?,?,?);" % valuesList
        self._connection.execute(insertQuery, valuesList)
        self._connection.commit()
    
    def readFromTable(self):
        readQuery = "SELECT * FROM task;"
        return self._connection.execute(readQuery).fetchall()
    
    def updateTable(self, columnValues: dict):
        updateQuery = "UPDATE task SET "
        for i, items in enumerate(columnValues.items()):
            if(items[0] != "id"):
                updateQuery += items[0] + "='" + items[1] + "'"
                if(i != len(columnValues)-2):
                    updateQuery += ","
                else:
                    updateQuery += " "
        updateQuery += "WHERE id=" + str(columnValues["id"]) + ";"
        self._connection.execute(updateQuery)
        self._connection.commit()
    
    def deleteTask(self, taskId):
        deleteQuery = "DELETE FROM task WHERE id = " + str(taskId) + ";"
        self._connection.execute(deleteQuery)
        self._connection.commit()
    
    def getRecentlyAddedTaskId(self) -> int:
        query = "SELECT MAX(id) FROM task;"
        return self._connection.execute(query).fetchone()[0]
    
    def isEmpty(self):
        if(len(self.readFromTable()) == 0):
            return True
        else:
            return False
    
    def closeDatabaseConnection(self):
        self._connection.close()