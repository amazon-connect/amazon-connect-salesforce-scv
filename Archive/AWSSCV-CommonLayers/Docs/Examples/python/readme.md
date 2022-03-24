# API

# awsscv.sf
## Logging
All methods support specifiying a "lambda_logging_level" environment variable to control the level of logging.

Levels are:
- CRITICAL
- ERROR
- WARNING
- INFO (default)
- DEBUG

## Methods

[**search**](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_sosl.htm)
- **Parameters**
    - SOSL (string)
- **Return**
    - search_records (object)
- **Example**
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
      
    try:
      sf = Salesforce()

      search_records = sf.query("SELECT Id, Name FROM Contact LIMIT 1")

      return search_records

    except Exception as e:
        logger.error(e)
  ````

[**query**](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm)
- **Parameters**
    - SOQL (string)
- **Return**
    - records (object)
- **Example**
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
  
      records = sf.query("SELECT Id, Name FROM Contact LIMIT 1")

      return records
  
    exception Exception as e:
      logger.error(e)
  ````
  
[**parameterized_search**](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_search_parameterized.htm)
- **Parameters**
    - method (string) - "get" or "post"
    - param_data (string or object)
- **Return**
    - search_records (object)
- **Example**
  #### Get
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
    
      param_data = 'q=Joe&sobject=Contact&Contact.fields=id,name&Contact.limit=10'
  
      search_records = sf.parameterized_search('get', param_data)

      return search_records
    
    except Exception as e:
      logger.error(e)
  ````
  #### Post 
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
    
      param_data = {}
  
      search_records = sf.parameterized_search('post', param_data)

      return search_records
  
    except Exception as e:
      logger.error(e)
  ````

[**create**](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_sobject_create.htm)
- **Parameters**
  - sobject (string) - Salesforce object type
  - data (object) - Map of field name / value pairs
- **Return**
  - id (number)
- **Example**
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
  
      data = {
          'Subject': 'This is a test case',
          'Description': 'Test case showing case creation',
          'Status': 'New',
          'Priority': 'Low',
          'Origin': 'Phone'
      }
  
      id = sf.create('Case', data);

      return id
    
  except Exception as e:
    logger.error(e)
  ````
      
**update**
- **Parameters**
    - sobject (string) - Salesforce object type
    - sobject_id (string) - Salesforce object id
    - data (object) - Map of field name / value pairs
- **Return**
    - status_code (number)
- **Example**
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
  
      data = {
        'Subject': 'This is an updated subject',
        'Priority': 'High'
      }
  
      status_code = sf.update('Contact', 'ABC123', data)

      return status_code
  
    except Exception as e:
      logger.error(e)
  ````
    
**update_by_external**
- **Parameters**
    - sobject (string) - Salesforce object type
    - field (string) - Salesforce object field name
    - sobject_id (string) - Salesforce object id
    - data (object) - Map of field name / value pairs
- **Return**
    - status_code (number)
- **Example**
  ````
  TODO
  
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
  
      status_code = sf.update_by_external(sobject, field, sobject_id, data)

      return status_code
  
    except Exception as e:
      logger.error(e)
  ````

**delete**
- **Parameters**
    - sobject (string) - Salesforce object type
    - sobject_id (string) - Salesforce object id
- **Return**
    - status_code (number)
- **Example**
  ````
  import os, logging
  from awsscv.sf import Salesforce

  logger = logging.getLogger()
  logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

  def lambda_handler(event, context):
    logger.debug(event)
  
    try:
      sf = Salesforce()
  
      status_code = sf.delete('Case', ABC123');

      return status_code
  
    except Exception as e:
      logger.error(e)
  ````
    
**call_flow**
- **Parameters**
    - Flow Id (string)
    - Data (object)
- **Return**
    - Object
- **Example**
  ````
  TODO
  ````
    
**create_simple_chatter_post**
- **Parameters**
    - Chatter Group Id (string)
    - Message (string)
    - Visibility (string)
- **Return**
    - Object
- **Example**
  ````
  TODO
  ````
    
**create_formatted_chatter_post**
- **Parameters**
    - Chatter Group Id (string)
    - Message Segments (object)
    - Visibility (string)
- **Return**
    - Object
- **Example**
  ````
  TODO
  ````
