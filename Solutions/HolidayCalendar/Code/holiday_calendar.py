# Version: 2022.03.16
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
import json
import time
import os
import logging
from datetime import datetime, date, timezone, timedelta

from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))

def lambda_handler(event, context):
    logger.debug(event)
    if 'source' in event:
        logger.debug('**********EventBridge Warmer**********')
        return 'warm'

    logger.debug('**********Start Holiday Check**********')

    response = {'isHoliday':'0'}

    # Get Current Date and time in a good format
    if 'tz' in event['Details']['ContactData']['Attributes']:
        if event['Details']['ContactData']['Attributes']:
            timezone_offset = int(event['Details']['ContactData']['Attributes']['tz'])
            logger.debug('TZ Offset found in event: ' + str(timezone_offset))
    else:
        timezone_offset =int(os.getenv('tz_offset'))
        logger.debug('Default offset used: ' + str(timezone_offset))

    tzinfo = timezone(timedelta(hours=timezone_offset))

    now = datetime.now(tzinfo)
    current_time = now.strftime('%H:%M:%S')
    today_date  = now.strftime('%Y-%m-%d')


    # Pull the entire holiday list
    try:
        sf = Salesforce()
        get_holidays = sf.query('SELECT Name, ActivityDate, EndTimeInMinutes, StartTimeInMinutes, IsAllDay, IsRecurrence, Description FROM Holiday')
        logger.debug(get_holidays)

    except Exception as e:
        logger.error(e)

        response.update({'status':'fail'})
        return response

    logger.debug(get_holidays)

    # Iterate through the holiday list
    for h in get_holidays:
        logger.debug(h)

        if h['ActivityDate'] == today_date:
            response.update({'isHoliday':'1','holidayName':h['Name'],'description':h['Description']})
            logger.debug('Direct holiday match')

        elif h['IsRecurrence']:

            if date.today().strftime('%m-%d') == h['ActivityDate'].partition('-')[2]:
                response.update({'isHoliday':'1','holidayName':h['Name'],'description':h['Description']})
                logger.debug('Recurring holiday match')

            else:
                logger.debug('Recurring holiday does not match')
                continue

        else:
            logger.debug('No holidays match')
            continue

        # Check hours for holiday
        if not h['IsAllDay']:
            start_time = '{:02d}:{:02d}:00'.format(*divmod(h['StartTimeInMinutes'], 60))
            end_time = '{:02d}:{:02d}:00'.format(*divmod(h['EndTimeInMinutes'], 60))

            if datetime.strptime(current_time,'%H:%M:%S') > datetime.strptime(start_time,'%H:%M:%S') and datetime.strptime(current_time,'%H:%M:%S') < datetime.strptime(end_time,'%H:%M:%S'):
                response.update({'isInHours':'1'})
                logger.debug('Recurring holiday is in time frame')
                break

            else:
                response.update({'isHoliday':'0'})
                logger.debug('Recurring holiday is NOT in time frame')
                continue

        else:
            response.update({'isInHours':'1'})
            logger.debug('Recurring holiday is an all day event')

    logger.debug(response)
    logger.debug('**********Stop Holiday Check**********')
    return response
