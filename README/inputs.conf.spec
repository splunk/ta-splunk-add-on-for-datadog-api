[datadog_metric_inventory://<name>]
global_account = Please select a global account for this input.
query = Query string
custom_metrics = Note: You may use "Custom Metrics" parameters from datadog (https://docs.datadoghq.com/integrations/system/) to override pre-populated "Query" parameter.
start_time = This is the start time from where you want to ingest the data. Please enter UTC time. Example Format: 2020-02-08 00:00:00
duration = 
duration_unit = 

[datadog_event_stream://<name>]
global_account = Please select a global account for this input.
start_time = This is the start time from where you want to ingest the data. Please enter UTC time. Example Format: 2020-02-08 00:00:00
end_time = This is the end time to where you want to ingest the data. It could be a future time. Please enter UTC time. Example Format: 2030-03-08 22:11:59
priority = Priority of your events. (optional)
sources = A comma separated string of sources. (optional)
tags = A comma separated list indicating what tags, if any, should be used to filter the list of monitors by scope. (optional)
unaggregated = Set unaggregated to true to return all events within the specified [start,end] timeframe.