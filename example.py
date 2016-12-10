

def process(companyArg):
    import csv
    import os

    companyArg = companyArg.lower().strip().replace("\"", "")
    maxProb = -1
    finalDepartment = None

    with open(os.getcwd() + '/training.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|', )
        spamreader.next()
        for row in spamreader:
            company = row[1]
            department = row[2]
            prob = row[3]

            company = company.lower().strip().replace("\"", "")

            if company == companyArg and prob > maxProb:
                maxProb = prob
                finalDepartment = department

        return finalDepartment.strip()
print process("Microsoft")