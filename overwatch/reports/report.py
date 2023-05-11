import reports.html as html
import reports.plain as plain
import reports.json as json
from datetime import datetime

outputFormat = ''
storedMessages = {}

def storeMessage(typ, msg):
    storedMessages[typ] = msg

def setOutputFormat(fmt):
    global outputFormat
    outputFormat = fmt

def render(reportType: str):
    global storedMessages
    reportType = reportType.lower().replace(" ", "_")

    preparedMessages = prepare(reportType, storedMessages)

    rendered = ""
    if outputFormat == "html":
        rendered = html.render(reportType, preparedMessages)
    elif outputFormat == "txt":
        rendered = plain.render(reportType, preparedMessages)
    elif outputFormat == "json":
        rendered = json.render(reportType, preparedMessages)

    if rendered == "":
        return
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = f'/tmp/report-{reportType}-{timestamp}.{outputFormat}'
    print('Printing file into', filepath)
    f = open(filepath, 'w')
    f.write(rendered)
    f.close()
    storedMessages = {}

def prepare(reportType: str, storedMessages: dict) -> dict:
    storedMessages["reportType"] = reportType
    storedMessages["report_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return storedMessages