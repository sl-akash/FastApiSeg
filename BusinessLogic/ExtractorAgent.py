from datetime import datetime


class ExtractorAgent:
    def __init__(self):
        self.itemCategory = ["Subtotal", "Tax", "Total Amount", "Insurance Payment", "Patient Responsibility"]
        self.diagoniseCategory = ["Admission Date", "Discharge Date", "Attending Physician", "Admission Diagnosis"]

    def itemizedBillAgent(self, pageList):
        returnList = {"item" : []}
        extracted = False
        for page in pageList:
            list1 = page.split("DATE\nDESCRIPTION\nQTY\nRATE\nAMOUNT\n")
            try:
                last_index = 0
                if extracted:
                    list2 = page.split("\n")
                else:
                    try:
                        list2 = list1[1].split("\n")
                    except:
                        continue
                for i in range(0, len(list2), 5):
                    if self.validate_date(list2[i]):
                        jData = {"date": list2[i],
                                 "description": list2[i + 1],
                                 "quantity": list2[i + 2],
                                 "rate": list2[i + 3],
                                 "amount": list2[i + 4]}
                        returnList["item"].append(jData)
                        last_index = i + 4
                        extracted = True
                    else:
                        break
                if extracted:
                    for i in range(last_index, len(list2)):
                        if any(element in list2[i] for element in self.itemCategory):
                            data = next((word for word in self.itemCategory if word in list2[i]), None)
                            if not None:
                                returnList[str(data)] = list2[i + 1]
            except:
                pass
        return returnList

    def validate_date(self, date):
        try:
            datetime.strptime(date, "%m/%y/%d").date()
            return True
        except:
            return False

    def idAgent(self, pageList):
        returnList = {"ID Number": []}
        nameFound = False
        dobFound = False
        for page in pageList:
            list1 = page.split("Full Name:\n")
            list2 = page.split("Date of Birth:\n")
            list3 = page.split("ID Number:\n")
            if not nameFound:
                try:
                    returnList["Full Name"] = list1[1].split("\n")[0]
                    nameFound = True
                except:
                    nameFound = False
            if not dobFound:
                try:
                    returnList["Date of Birth"] = list2[1].split("\n")[0]
                    dobFound = True
                except:
                    dobFound = False
            try:
                for i in range(1, len(list3)):
                    try:
                        returnList["ID Number"].append(list3[1].split("\n")[0])
                    except:
                        pass
            except:
                pass
        return returnList

    def dischargeSummaryAgent(self, pageList):
        returnList = {}
        diagoniseCategory = self.diagoniseCategory
        for page in pageList:
            for i, diagonise in enumerate(diagoniseCategory):
                list1 = page.split(f"{diagonise}:\n")
                try:
                    returnList[diagonise] = list1[1].split("\n")[0]
                except:
                    pass
        return returnList

