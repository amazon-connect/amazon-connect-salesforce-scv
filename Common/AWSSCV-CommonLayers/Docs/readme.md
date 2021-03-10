# API

# aws.sf

## Methods

**search**
- **Parameters**
    - SOSL Query (string)
- **Return**
    - Object
- [**Example**](Examples/query.py)
    
**query**
- **Parameters**
    - SOQL Query (string)
- **Return**
    - Object
- **Example**
    
**parameterized_search**
- **Parameters**
    - SOQL Query (string)
- **Return**
    - Object
- **Example**
    
**update**
- **Parameters**
    - Object Type (string)
    - Object Id (string)
    - Data (object)
- **Return**
    - Status Code (number)
- **Example**
    
**update_by_external**
- **Parameters**
    - Object Type (string)
    - External Field Name (string)
    - Object Id (string)
    - Data (object)
- **Return**
    - Status Code (number)
- **Example**
    
**create**
- **Parameters**
    - Object Type (string)
    - Data (object)
- **Return**
    - Object Id (number)
- **Example**
    
**delete**
- **Parameters**
    - Object Type (string)
    - Object Id (string)
- **Return**
    - Status Code (number)
- **Example**
    
**call_flow**
- **Parameters**
    - Flow Id (string)
    - Data (object)
- **Return**
    - Object
- **Example**
    
**create_simple_chatter_post**
- **Parameters**
    - Chatter Group Id (string)
    - Message (string)
    - Visibility (string)
- **Return**
    - Object
- **Example**
    
**create_formatted_chatter_post**
- **Parameters**
    - Chatter Group Id (string)
    - Message Segments (object)
    - Visibility (string)
- **Return**
    - Object
- **Example**
