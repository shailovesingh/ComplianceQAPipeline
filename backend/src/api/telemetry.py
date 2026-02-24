# Azure Opentelemetry integration

import os
import logging
from azure.monitor.opentelemetry import configure_azure_monitor


# Create a dedicated logger
logger = logging,getLogger("brand-guardian-telemetry")

def setup_telemetry():
    '''
    Initializes Azure Monitor OpenTelemetry
    Tracks: HTTP requests, database queries, errors, performance metrics
    sends this data to azure monitor

    It auto captures every API request
    No need to manually log each endpoint
    '''

    # retrieve connection string
    connection_string = os.getenv("APPLICATIONSIGHTS_CONNECTION_STRING")

    # check if configured
    if not connection_string:
        logger.warning("No instrumentation key found.Telemtry is DISABLED.")
        return
    # configure the azure monitor
    try:
        configure_azure_monitor(
            connection_string=connection_string,
            logger_name = "brand-guardian-tracer"
        )
        logger.info("Azure Montior Tracking Enabled and Connected")
    except Exception as e:
        logger.error(f"Failed to Initialize Azure Monitor: {e}")

'''
Why do we use telemetry?

Without :
API is slow -> No idea which part
How many users today ? No visibility

With :
/audit endpoint averages 4.5 s(Indexer takes 3.8s)
Error logs show : 12% of audits fall due to Youtube download errors
Metrics show : 450 API calls today, 89% success rate
'''