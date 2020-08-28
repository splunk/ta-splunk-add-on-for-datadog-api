# Datadog Add-on for Splunk

> The **Datadog Add-on for Splunk** uses the _Datadog HTTP API_ to fetch data and ingest it into Splunk.

## Getting Started
This is a TA to pull in data from Datadog HTTP API. 
The [events](https://docs.datadoghq.com/api/v1/events/#query-the-event-stream) endpoint and [metrics](https://docs.datadoghq.com/api/v1/metrics/#query-timeseries-points) endpoint are being hit to fetch data. 

#### Installation and Configuration Steps
This application can be installed on-prem and cloud. 

##### Installation Steps for `on-prem`
Install the TA on one of the Heavy Forwarder(s).

##### Installation Steps for `cloud`
Create a support ticket with `APP-CERT` reference to get it installed on the Cloud instance *OR* follow the cloud-ops steps to install non-published applications.

#### Configuration steps
The configuration steps are common for `on-prem` and `cloud`. Please follow the following steps in order:
1. Open the Web UI for the Heavy Forwarder (or IDM).
2. Access the TA from the list of applications.
3. Set global setings.
- Click on `Configuration` button on the top left corner.
- Click on `Add-on Settings` button.
- Enter the following details:
  - **API Key** (_required_): This is Datadog API Key. 
  - **APP Key** (_required_): This is Datadog Application Key
  - **Datadog Site** (_required_): Please enter "com" if you are on Datadog US site or enter "eu" if you are on Datadog EU site.
- Click on the `Save` green button.
4. Create an input.
4.1 Create a datadog event stream input
- Click on `Inputs` button on the top left corner.
- Click on `Create New Input` button on the top right corner.
- Select datadog event stream
- Enter the following details in the pop up box:
    - **Name** (_required_): Unique name for the data input.
    - **Interval** (_required_): Time interval of input in seconds. 
    - **Index** (_required_): Index for storing data.
    - **Start Time** (_required_): This is the start time from where you want to ingest the data. Please enter UTC time. Required Format: 2020-02-08 00:00:00.
    - **End Time** (_required_): This is the end time to where you want to ingest the data. It could be a future time. Please enter UTC time. Required Format: 2030-03-08 22:11:59.
    - **Priority** (_optional_): Priority of your events.
    - **Sources** (_optional_): A comma separated string of sources.
    - **Tags** (_optional_): A comma separated list indicating what tags, if any, should be used to filter the list of monitors by scope.
    - **Unaggregated** : Set unaggregated to `true` to return all events within the specified [start,end] timeframe. Otherwise if an event is aggregated to a parent event with a timestamp outside of the timeframe, it won’t be available in the output. The default value is `true`. 
- Click on the `Add` green button on the bottom right of the pop up box.
4.2 Create a datadog metric inventory input
- Click on `Inputs` button on the top left corner.
- Click on `Create New Input` button on the top right corner.
- Select datadog metric inventory
- Enter the following details in the pop up box:
    - **Name** (_required_): Unique name for the data input.
    - **Interval** (_required_): Time interval of input in seconds. 
    - **Index** (_required_): Index for storing data.
    - **Query** (_required_): Metric query string
    - **Custom Metrics (optional)** (_optional_): You may use "Custom Metrics" parameters from datadog (https://docs.datadoghq.com/integrations/system/) to override pre-populated "Query" parameter
    - **Start Time** (_required_): This is the start time from where you want to ingest the data. Please enter UTC time. Required Format: 2020-02-08 00:00:00.
    - **Duration (To)** (_required_): This duration that you want to get the metric summary. For example, if you set it to 1 day. The add-on will inegst the data from start_time to 1 day later. Please make sure you set the interval to be consistent with the duration. 
    - **Duration (To) Unit** : Unit of Duration. 
- Click on the `Add` green button on the bottom right of the pop up box.
5. Set Proxy Setting (optional)
 - Click on `Configuration` button on the top left corner.
- Click on `Proxy` button.
- Enter the following details:
  - **Enable** (_required_) : Check `Enable` box if you want to enable proxy support
  - **Proxy Type** (_required_) : Select a Proxy Type: `http`, `socks4`, `socks5`.
  - **Host** (_required_) : Proxy URL.
  - **Port** (_required_) : Proxy Port.
  - **Username** : Proxy Username.
  - **Password** : Proxy Password.
  - **Remote DNS resolution** : Checkbox for enabling remote DNS resolution.
- Click on the `Save` green button.

## Versions Supported

  - Tested for installation and basic ingestion on Splunk 8.0.1, 8.0.0, 7.3, 7.2.9, 7.1 and 7.0 based on Datadog test account.


> Built by Splunk's FDSE Team (#team-fdse).

## Credits & Acknowledgements
* Yuan Ling
* Mayur Pipaliya
