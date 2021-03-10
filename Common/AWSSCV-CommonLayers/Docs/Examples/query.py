from awsscv.sf import Salesforce

logger = logging.getLogger()

def lambda_handler(event, context):
    sf = Salesforce()

    response = sf.query("SELECT Id, Name FROM Contact LIMIT 1")

    return response