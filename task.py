class Task:
    def __init__(self, identityNumber = -1, taskName = None, taskStartingDate = None, taskEndingDate = None, taskDescription = None):
        self._identityNumber = identityNumber
        self._taskName = taskName
        self._taskStartingDate = taskStartingDate
        self._taskEndingDate = taskEndingDate
        self._taskDescription = taskDescription
    
    def getTaskIdentityNumber(self) -> int:
        return self._identityNumber
    
    def getTaskName(self) -> str:
        return self._taskName
    
    def getTaskStartingDate(self) -> str:
        return self._taskStartingDate
    
    def getTaskEndingDate(self) -> str:
        return self._taskEndingDate
    
    def getTaskDescription(self) -> str:
        return self._taskDescription
    
    def setTaskIdentityNumber(self, taskId: int):
        self._identityNumber = taskId
    
    def setTaskName(self, taskName: str):
        self._taskName = taskName
    
    def setTaskStartingDate(self, taskStartingDate: str):
        self._taskStartingDate = taskStartingDate
    
    def setTaskEndingDate(self, taskEndingDate: str):
        self._taskEndingDate = taskEndingDate
        
    def setTaskDescription(self, taskDescription: str):
        self._taskDescription = taskDescription
    
    def isEmpty(self) -> bool:
        isEmpty = True
        if(self._identityNumber > 0):
            isEmpty = False
        return isEmpty
    
    def displayDetails(self):
        print("id : " + str(self._identityNumber))
        print("taskName : " + self._taskName)
        print("taskStartingDate : " + self._taskStartingDate)
        print("taskEndingDate : " + self._taskEndingDate)
        print("taskDescription : " + self._taskDescription)