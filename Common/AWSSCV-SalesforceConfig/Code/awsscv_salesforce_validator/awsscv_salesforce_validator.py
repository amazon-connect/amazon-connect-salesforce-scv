"""
**********************************************************************************************************************
*  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved                                            *
*                                                                                                                    *
*  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated      *
*  documentation files (the "Software"), to deal in the Software without restriction, including without limitation   *
*  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and  *
*  to permit persons to whom the Software is furnished to do so.                                                     *
*                                                                                                                    *
*  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO  *
*  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
*  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF         *
*  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS *
*  IN THE SOFTWARE.                                                                                                  *
**********************************************************************************************************************
"""

import os, logging
from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    try:
        sf = Salesforce()
        qr = sf.query("SELECT Id, Username FROM User LIMIT 1")

        logger.debug(qr)

        return {
            "Status": "SUCCESS"
        }

    except Exception as e:
        logger.error(e)

        return {
            "Status": "FAILURE",
            "Reason": str(e)
        }