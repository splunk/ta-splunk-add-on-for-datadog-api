#   ########################################################################
#   Copyright 2020 Splunk Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#   ########################################################################
# encoding = utf-8

import os
import sys
import time
import datetime
import requests
import re
import json
from datetime import datetime, timedelta 

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def get_slice_time(start, end, steps):
    time_list = []
    chunks = range(start, end, steps)
    counter = 0
    for chunk in chunks:
        counter += 1
        if len(chunks) is counter:
            time_list.append((chunk, end))
        else:
            time_list.append((chunk, chunk+steps-1))
    return time_list


def build_metric_url(datadog_site, start, end, query):
    endpoint = "https://app.datadoghq.{}/api/v1/query?".format(datadog_site)
    param = "&from=" + str(start)
    param += "&to=" + str(end)
    param += "&query=" + query
    url = endpoint + param
    return url

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # start_time = definition.parameters.get('start_time', None)
    # end_time = definition.parameters.get('end_time', None)
    # query = definition.parameters.get('query', None)
    # custom_metrics = definition.parameters.get('custom_metrics', None)
    start_time = definition.parameters.get('start_time', None)
    duration = definition.parameters.get('duration', None)
    try:
        datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError(
            "Incorrect date format, should be YYYY-MM-DD hh:mm:ss")
    try:
        int(duration)
    except ValueError:
        raise ValueError(
            "Incorrect duration format, should be an integer")
    pass


def collect_events(helper, ew):
    # Get account info
    global_account = helper.get_arg('global_account')
    opt_api_key = global_account['api_key']
    opt_app_key = global_account['app_key']
    opt_datadog_site = global_account['dd_site']
    
    opt_start_time = helper.get_arg('start_time')
    opt_duration = helper.get_arg('duration')
    opt_duration_unit = helper.get_arg('duration_unit')
    # opt_interval = int(helper.get_arg('interval'))
    
    opt_custom_metrics  = helper.get_arg('custom_metrics')
    if opt_custom_metrics:
        query = opt_custom_metrics
    else:
        query = helper.get_arg('query')
    
    # Generate sourcetype based on datadog metrics
    # i.e. datadog:metric:cpu_system, datadog:metric:inventory
    runtime_sourcetype = "datadog:metric:" +  query.split('{')[0].replace('.','_');
    
    helper.log_debug("[-] DataDog Metrics: datadog site {}".format(opt_datadog_site))
    
    # Parse and construct humar readable "to" parameter
    to_with_unit = int(re.search(r'\d+', opt_duration).group())
    if "Sec" in opt_duration_unit:
        parsed = "second"
        duration = to_with_unit
    elif "Min" in opt_duration_unit:
        parsed = "minute"
        duration = to_with_unit * 60
    elif "Hour" in opt_duration_unit:
        parsed = "hour"
        duration = to_with_unit * 60 * 60
    elif "Day" in opt_duration_unit:
        parsed = "day"
        duration = to_with_unit * 60 * 60 * 24
    elif "Week" in opt_duration_unit:
        parsed = "week"
        duration = to_with_unit * 60 * 60 * 24 * 7
    elif "Year" in opt_duration_unit:
        parsed = "year"
        duration = to_with_unit * 60 * 60 * 24 * 365
    else:
        parsed = "default"
        duration = to_with_unit
    
    helper.log_debug("[-] DataDog Metrics: duration {}".format(duration))



    # TODO add checkpoint
    # set checkpoint key
    key = "{}_DATADOG_METRICS_processing_for_{}_{}_{}_{}".format(
        helper.get_input_stanza_names(), opt_start_time, opt_duration, opt_duration_unit, query)

    # check checkpoint

    helper.log_debug("[-] DataDog Metrics: check checkpoint")

    helper.log_debug(
        "[-] DataDog Metrics: Last start time: {}".format(helper.get_check_point(key)))
    
    # Fist time: use start time from UI and save it in checkpoint
    if helper.get_check_point(key) is None:
        # convert start time to datetime type
        opt_start_time = datetime.strptime(
            opt_start_time, '%Y-%m-%d %H:%M:%S')
        # calculate end time by adding duration to start time
        opt_end_time = (opt_start_time + timedelta(seconds=duration))

        # convert start time and end time to integer
        opt_start_time = int(
            (opt_start_time - datetime(1970, 1, 1)).total_seconds())
        opt_end_time = int(
            (opt_end_time - datetime(1970, 1, 1)).total_seconds())
        
        # save the initial start time in checkpoint
        helper.save_check_point(key, opt_start_time)
    else:
        opt_start_time = int(helper.get_check_point(key))
        opt_end_time = opt_start_time + duration
       
    helper.log_debug("[-] DataDog Metrics: start time {}".format(opt_start_time))
    helper.log_debug("[-] DataDog Metrics: end time {}".format(opt_end_time))

    # check if endtime > now
    now = datetime.utcnow()
    helper.log_debug("[-] DataDog Metrics: now -- {}".format(now))
    # convert now to epoch time
    now = int((now - datetime(1970, 1, 1)).total_seconds())
    helper.log_debug("[-] DataDog Metrics: now (epoch) -- {}".format(now))
    if int(opt_end_time) > int(now):
        helper.log_debug("[-] DataDog Metrics: The duration you set will make the end time hit the future time. Change to use NOW as End Time")
        opt_end_time = now
    helper.log_debug("[-] DataDog Metrics: end time later {}".format(opt_end_time))

        
    # build url according to user's inputs
    url = build_metric_url(opt_datadog_site, opt_start_time, opt_end_time, query)
    
    headers = {
        'Content-type': 'application/json',
        'DD-API-KEY': opt_api_key,
        'DD-APPLICATION-KEY': opt_app_key
    }

    response = helper.send_http_request(url, "GET", parameters=None, payload=None,
                                        headers=headers, cookies=None, verify=True, cert=None, timeout=None, use_proxy=True)

    helper.log_debug("[-] DataDog Metrics API: Response code: {}".format(response.status_code))
    if response.status_code != 200:
        helper.log_error(
            "\t[-] DataDog Metrics API Error: {}".format(response.text))
        e = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype="datadog:metric:errors", data=json.dumps(json.loads(response.text)))
        try:
            ew.write_event(e)
        except Exception as ex:
            raise ex
    else:
        events = response.json()
        if events.get('status', None) and events['status'] == "ok":
            if len(events['series']) > 0:
                for event in events['series']:
                    # event['Timestamp'] = str(event['start'])[:-3]
                    event['Timestamp'] = str(event['start']/1000)
            
                    # Calculated field: pointlist_average = sum of pointlist entries / count of pointlist entries
                    if event.get('pointlist', None):
                        total=0
                        for point in event['pointlist']:
                            total += point[1]
                                
                        event['pointlist_count'] = len(event['pointlist'])
                        if event['pointlist_count'] == 0:
                            event['pointlist_average'] = 0
                        else:
                            event['pointlist_average'] = total / event['pointlist_count']
                                      
                    # Calcuated field: Host
                    # runtime_host = re.split(':', event['scope'])[1]
                    runtime_host = None
                    scope = event.get('scope', None)
                    helper.log_debug("[-] scope: {}".format(scope))
                    if scope:
                        if len(re.split(':', scope)) == 2 and re.split(':', scope)[0] == "host":
                            runtime_host = re.split(':', scope)[1]
                    helper.log_debug("[-] runtime_host: {}".format(runtime_host))

            
                    # Build Event
                    # e = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=json.dumps(event))
                    event_time = str(event['start'])[:-3]
                    e = helper.new_event(time=event_time, host=runtime_host, source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=runtime_sourcetype, data=json.dumps(event), done=True, unbroken=True)
                    try:
                        ew.write_event(e)

                        # update checkpoint with event['end'] 
                        timestamp = str(event['end'])[:-3] 
                        helper.save_check_point(key, timestamp)

                    except Exception as ex:
                        raise ex
            else:
                events['Timestamp'] = str(events['from_date']/1000)

                event_time = str(events['from_date'])[:-3]
        
                # Build Event
                # e = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=json.dumps(event))
                e = helper.new_event(time=event_time, host=None, source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=runtime_sourcetype, data=json.dumps(events), done=True, unbroken=True)
                try:
                    ew.write_event(e)
                    # update checkpoint with events['to_date'] 
                    timestamp = str(events['to_date'])[:-3]
                    helper.save_check_point(key, timestamp)
                except Exception as ex:
                    raise ex
            
        # when "status" != ok -- e.g. invalid query string 
        # write into datadog:metric:errors and log error
        else:
            helper.log_error(
            "\t[-] DataDog Metrics API Error: {}".format(events["error"]))
            e = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype="datadog:metric:errors", data=json.dumps(events))
            try:
                ew.write_event(e)
            except Exception as ex:
                raise ex

        
        
            
