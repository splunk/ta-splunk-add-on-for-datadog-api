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
import json

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


def build_event_url(datadog_site, start, end, priority, sources, tags, unaggregated):
    endpoint = "https://api.datadoghq.{}/api/v1/events?".format(datadog_site)
    param = "start=" + str(start)
    param += "&end=" + str(end)
    if priority:
        param += "&priority=" + str(priority)
    if sources:
        param += "&sources=" + str(sources)
    if tags:
        param += "&tags=" + str(tags)
    if unaggregated:
        param += "&unaggregated=true"
    url = endpoint + param
    return url


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # api_key = definition.parameters.get('api_key', None)
    # app_key = definition.parameters.get('app_key', None)
    # start_time = definition.parameters.get('start_time', None)
    # end_time = definition.parameters.get('end_time', None)
    # priority = definition.parameters.get('priority', None)
    # sources = definition.parameters.get('sources', None)
    # tags = definition.parameters.get('tags', None)
    # unaggregated = definition.parameters.get('unaggregated', None)
    start_time = definition.parameters.get('start_time', None)
    end_time = definition.parameters.get('end_time', None)

    priority = definition.parameters.get('priority', None)

    try:
        datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError(
            "Incorrect date format, should be YYYY-MM-DD hh:mm:ss")
    pass


def collect_events(helper, ew):
    """Implement your data collection logic here

    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_api_key = helper.get_arg('api_key')
    opt_app_key = helper.get_arg('app_key')
    opt_start_time = helper.get_arg('start_time')
    opt_end_time = helper.get_arg('end_time')
    opt_priority = helper.get_arg('priority')
    opt_sources = helper.get_arg('sources')
    opt_tags = helper.get_arg('tags')
    opt_unaggregated = helper.get_arg('unaggregated')
    # In single instance mode, to get arguments of a particular input, use
    opt_api_key = helper.get_arg('api_key', stanza_name)
    opt_app_key = helper.get_arg('app_key', stanza_name)
    opt_start_time = helper.get_arg('start_time', stanza_name)
    opt_end_time = helper.get_arg('end_time', stanza_name)
    opt_priority = helper.get_arg('priority', stanza_name)
    opt_sources = helper.get_arg('sources', stanza_name)
    opt_tags = helper.get_arg('tags', stanza_name)
    opt_unaggregated = helper.get_arg('unaggregated', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get account credentials as dictionary
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
    # Get account info   
    global_account = helper.get_arg('global_account')
    opt_api_key = global_account['api_key']
    opt_app_key = global_account['app_key']
    opt_datadog_site = global_account['dd_site']
 
    opt_start_time = helper.get_arg('start_time')
    opt_end_time = helper.get_arg('end_time')

    opt_interval = helper.get_arg('interval')
    
    helper.log_debug("[-] DataDog Events: datadog site {}".format(opt_datadog_site))
    
    helper.log_debug("[-] DataDog Events: UI start time {}".format(opt_start_time))
    helper.log_debug("[-] DataDog Events: UI end time {}".format(opt_end_time))

    opt_start_time = datetime.datetime.strptime(
        opt_start_time, '%Y-%m-%d %H:%M:%S')
    opt_start_time = int(
        (opt_start_time - datetime.datetime(1970, 1, 1)).total_seconds())

    opt_end_time = datetime.datetime.strptime(
        opt_end_time, '%Y-%m-%d %H:%M:%S')
    opt_end_time = int(
        (opt_end_time - datetime.datetime(1970, 1, 1)).total_seconds())

    opt_priority = helper.get_arg('priority')
    opt_sources = helper.get_arg('sources')
    opt_tags = helper.get_arg('tags')
    opt_unaggregated = helper.get_arg('unaggregated')

    # Slice
    steps = 60*60*24

    #payload = {}
    headers = {
        'Content-type': 'application/json',
        'DD-API-KEY': opt_api_key,
        'DD-APPLICATION-KEY': opt_app_key
    }

    # checkpoint key
    current_url = build_event_url(opt_datadog_site, opt_start_time, opt_end_time,
                            opt_priority, opt_sources, opt_tags, opt_unaggregated)
    key = "{}_DATADOG_EVENTS_processing".format(
        helper.get_input_stanza_names())
    last_ran_key = "last_ran_{}".format(key)

    # check checkpoint

    helper.log_debug("[-] DataDog Events: check checkpoint")
    helper.log_debug(
        "[-] DataDog Events: Last run time: {}".format(helper.get_check_point(last_ran_key)))

    now = datetime.datetime.utcnow()
    now = int((now - datetime.datetime(1970, 1, 1)).total_seconds())
    helper.log_debug("[-] DataDog Events: now - {}".format(now))

    if helper.get_check_point(last_ran_key) is None:
        helper.save_check_point(last_ran_key, opt_start_time)
    else:
        opt_start_time = int(helper.get_check_point(last_ran_key) + 1)

    if now < opt_end_time:
        opt_end_time = now

    helper.log_debug("[-] DataDog Events: opt_start_time - {}".format(opt_start_time))
    helper.log_debug("[-] DataDog Events: opt_end_time - {}".format(opt_end_time))

    helper.log_debug(
        "\t[-] DataDog Events: last run checkpoint: {} -- value: {}".format(last_ran_key, helper.get_check_point(last_ran_key)))

    # Pageing

    time_list = get_slice_time(int(opt_start_time), int(opt_end_time), steps)

    helper.log_debug(
        "Processing DataDog Events time_list: {}".format(len(time_list)))
    for time in time_list:
        helper.log_debug(
            "\t[-] DataDog Events:In for: processing time {}".format(time))
        # build url according to user's inputs
        url = build_event_url(opt_datadog_site, time[0], time[1], opt_priority,
                        opt_sources, opt_tags, opt_unaggregated)

        response = helper.send_http_request(url, "GET", parameters=None, payload=None,
                                            headers=headers, cookies=None, verify=True, cert=None, timeout=None, use_proxy=True)

        helper.log_debug("[-] DataDog Events API: Response code: {}".format(response.status_code))

        if response.status_code != 200:
            helper.log_debug(
                "\t[-] DataDog Events API Error: {}".format(response.text))

        events = response.json()

        if "events" in events:
            for event in events['events']:
                try:
                    event['ddhost'] = event['host']
                    event['ddsource'] = event['source']
                    del event['host']
                    del event['source']
                except Exception as e:
                    helper.log_debug(
                        "\t[-] Try Block 1: DataDog Events Exception {}".format(e))
                    pass

                try:
                    event_time = event['date_happened']
                    event = helper.new_event(json.dumps(
                        event), time=event_time, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
                    ew.write_event(event)

                    # save checkpoint for every event
                    timestamp = helper.get_check_point(last_ran_key)
                    if timestamp is None:
                        timestamp = event_time
                    else:
                        timestamp = max(int(timestamp), int(event_time))
                    helper.save_check_point(last_ran_key, timestamp)
                except Exception as e:
                    helper.log_debug(
                        "\t[-] Try Block 2: DataDog Events Exception {}".format(e))
        else:
            helper.log_debug("\t[-] No events to retrieve for {}.".format(url))
