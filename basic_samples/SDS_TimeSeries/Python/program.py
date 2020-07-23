"""
This sample script demonstrates how to invoke the
Sequential Data Store REST API with Time Series data
"""


import configparser
import json
import time
from ocs_sample_library_preview import (SdsType, SdsTypeCode, SdsTypeProperty,
                                        EDSClient, OCSClient, SdsStream)

SENDING_TO_OCS = True
TYPE_VALUE_TIME_NAME = "Value_Time"
TYPE_PRESSURE_TEMPERATURE_TIME_NAME = "Pressure_Temp_Time"

STREAM_PRESSURE_NAME = "Pressure_Tank1"
STREAM_TEMP_NAME = "Temperature_Tank1"
STREAM_TANK_0 = "Vessel"
STREAM_TANK_1 = "Tank1"
STREAM_TANK_2 = "Tank2"

VALUE_CACHE = []
VALUE_CACHE_2 = []


def get_type_value_time():
    """Creates a type for value/time events"""

    type_value_time = SdsType(
        id=TYPE_VALUE_TIME_NAME,
        description="A Time-Series indexed type with a value",
        sdsTypeCode=SdsTypeCode.Object)

    double_type = SdsType()
    double_type.Id = "doubleType"
    double_type.SdsTypeCode = SdsTypeCode.Double

    time_type = SdsType()
    time_type.Id = "string"
    time_type.SdsTypeCode = SdsTypeCode.DateTime

    value = SdsTypeProperty()
    value.Id = "value"
    value.SdsType = double_type

    time_prop = SdsTypeProperty()
    time_prop.Id = "time"
    time_prop.SdsType = time_type
    time_prop.IsKey = True

    type_value_time.Properties = []
    type_value_time.Properties.append(value)
    type_value_time.Properties.append(time_prop)

    return type_value_time


def get_type_press_temp_time():
    """Creates a type for press/temp/time events"""

    type_press_temp_time = SdsType(
        id=TYPE_PRESSURE_TEMPERATURE_TIME_NAME,
        description="A Time-Series indexed type with 2 values",
        sdsTypeCode=SdsTypeCode.Object)

    double_type = SdsType()
    double_type.Id = "doubleType"
    double_type.SdsTypeCode = SdsTypeCode.Double

    time_type = SdsType()
    time_type.Id = "string"
    time_type.SdsTypeCode = SdsTypeCode.DateTime

    temperature = SdsTypeProperty()
    temperature.Id = "temperature"
    temperature.SdsType = double_type

    pressure = SdsTypeProperty()
    pressure.Id = "pressure"
    pressure.SdsType = double_type

    time_prop = SdsTypeProperty()
    time_prop.Id = "time"
    time_prop.SdsType = time_type
    time_prop.IsKey = True

    type_press_temp_time.Properties = [temperature, pressure, time_prop]

    return type_press_temp_time


def get_data():
    """Creates a set of data for use in the sample"""

    values = []
    values.append({"pressure": 346, "temperature": 91,
                   "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 0, "temperature": 0,
                   "time": "2017-01-11T22:22:23.430Z"})
    values.append({"pressure": 386, "temperature": 93,
                   "time": "2017-01-11T22:24:23.430Z"})
    values.append({"pressure": 385, "temperature": 92,
                   "time": "2017-01-11T22:25:23.430Z"})
    values.append({"pressure": 385, "temperature": 0,
                   "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92,
                   "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2,
                   "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 0,
                   "time": "2017-01-11T22:28:29.430Z"})
    return values


def get_data_tank_2():
    """Creates a set of data for use in the sample"""

    values = []
    values.append({"pressure": 345, "temperature": 89,
                   "time": "2017-01-11T22:20:23.430Z"})
    values.append({"pressure": 356, "temperature": 0,
                   "time": "2017-01-11T22:21:23.430Z"})
    values.append({"pressure": 354, "temperature": 88,
                   "time": "2017-01-11T22:22:23.430Z"})
    values.append({"pressure": 374, "temperature": 87,
                   "time": "2017-01-11T22:28:23.430Z"})
    values.append({"pressure": 384.5, "temperature": 88,
                   "time": "2017-01-11T22:26:23.430Z"})
    values.append({"pressure": 384.2, "temperature": 92.2,
                   "time": "2017-01-11T22:27:23.430Z"})
    values.append({"pressure": 390, "temperature": 87,
                   "time": "2017-01-11T22:28:29.430Z"})

    return values


def get_pressure_data():
    """Gets a set of pressure data"""

    vals = get_data()
    values = []
    for val in vals:
        values.append({"value": val["pressure"], "time": val["time"]})
    return values


def get_temperature_data():
    """Gets a set of temperature data"""

    vals = get_data()
    values = []
    for val in vals:
        values.append({"value": val["temperature"], "time": val["time"]})
    return values


def suppress_error(sds_call):
    """Suppress an error thrown by SDS"""
    try:
        sds_call()
    except Exception as error:
        print(f"Encountered Error: {error}")


def main(test=False):
    """This function is the main body of the SDS Time Series sample script"""
    exception = None
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        tenant_id = config.get('Access', 'Tenant')
        namespace_id = config.get('Configurations', 'Namespace')

        # step 1
        if tenant_id == 'default' and namespace_id == 'default':
            sds_client = EDSClient(
                config.get('Access', 'ApiVersion'),
                config.get('Access', 'Resource'))
        else:
            sds_client = OCSClient(
                config.get('Access', 'ApiVersion'),
                config.get('Access', 'Tenant'),
                config.get('Access', 'Resource'),
                config.get('Credentials', 'ClientId'),
                config.get('Credentials', 'ClientSecret'),
                False)

        # step 2
        print('Creating value and time type')
        time_value_type = get_type_value_time()
        time_value_type = sds_client.Types.getOrCreateType(
            namespace_id, time_value_type)

        # step 3
        print('Creating a stream for pressure and temperature')
        pressure_stream = SdsStream(
            id=STREAM_PRESSURE_NAME,
            typeId=time_value_type.Id,
            description="A stream for pressure data of tank1")
        sds_client.Streams.createOrUpdateStream(namespace_id, pressure_stream)
        temperature_stream = SdsStream(
            id=STREAM_TEMP_NAME,
            typeId=time_value_type.Id,
            description="A stream for temperature data of tank1")
        sds_client.Streams.createOrUpdateStream(
            namespace_id, temperature_stream)

        # step 4
        sds_client.Streams.insertValues(
            namespace_id,
            pressure_stream.Id,
            json.dumps((get_pressure_data())))
        sds_client.Streams.insertValues(
            namespace_id,
            temperature_stream.Id,
            json.dumps((get_temperature_data())))

        # step 5
        print('Creating a tank type that has both stream and temperature')
        tank_type = get_type_press_temp_time()
        tank_type = sds_client.Types.getOrCreateType(namespace_id, tank_type)

        # step 6
        print('Creating a tank stream')
        tank_stream = SdsStream(
            id=STREAM_TANK_1,
            typeId=tank_type.Id,
            description="A stream for data of tank1s")
        sds_client.Streams.createOrUpdateStream(namespace_id, tank_stream)

        # step 7
        sds_client.Streams.insertValues(namespace_id, STREAM_TANK_1,
                                        json.dumps(get_data()))

        print()
        print()
        print('Looking at the data in the system.  In this case we have some'
              'null values that are encoded as 0 for the value.')
        data = get_data()
        tank_1_sorted = sorted(data, key=lambda x: x['time'], reverse=False)
        print()
        print('Value we sent:')
        print(tank_1_sorted[1])
        first_time = tank_1_sorted[0]['time']
        last_time = tank_1_sorted[-1]['time']

        # step 8
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_PRESSURE_NAME, None, first_time, last_time)

        print()
        print('Value from pressure stream:')
        print((results)[1])

        print()
        print('Value from tank1 stream:')
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_TANK_1, None, first_time, last_time)
        print((results)[1])

        # step 9
        print()
        print()
        print("turning on verbosity")
        sds_client.acceptverbosity = True

        print("This means that will get default values back (in our case"
              " 0.0 since we are looking at doubles)")

        print()
        print('Value from pressure stream:')
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_PRESSURE_NAME, None, first_time, last_time)
        print((results)[1])
        print()
        print('Value from tank1 stream:')
        results = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_TANK_1, None, first_time, last_time)
        print((results)[1])

        # step 10

        print()
        print()
        print("Getting data summary")
        # the count of 1 refers to the number of intervals requested
        summary_results = sds_client.Streams.getSummaries(
            namespace_id, STREAM_TANK_1, None, first_time, last_time, 1)
        print(summary_results)

        print()
        print()
        print('Now we want to look at data across multiple tanks.')
        print('For that we can take advantage of bulk stream calls')
        print('Creating new tank streams')
        tank_stream = SdsStream(
            id=STREAM_TANK_2,
            typeId=tank_type.Id,
            description="A stream for data of tank2")
        sds_client.Streams.createOrUpdateStream(namespace_id, tank_stream)

        data_tank_2 = get_data_tank_2()
        sds_client.Streams.insertValues(
            namespace_id, STREAM_TANK_2, json.dumps(get_data_tank_2()))

        tank_2_sorted = sorted(
            data_tank_2, key=lambda x: x['time'], reverse=False)
        first_time_tank_2 = tank_2_sorted[0]['time']
        last_time_tank_2 = tank_2_sorted[-1]['time']

        tank_stream = SdsStream(
            id=STREAM_TANK_0, typeId=tank_type.Id, description="")
        sds_client.Streams.createOrUpdateStream(namespace_id, tank_stream)

        sds_client.Streams.insertValues(
            namespace_id, STREAM_TANK_0, json.dumps(get_data()))

        time.sleep(10)

        # step 11
        print('Getting bulk call results')
        results = sds_client.Streams.getStreamsWindow(
            namespace_id, [STREAM_TANK_0, STREAM_TANK_2], None,
            first_time_tank_2, last_time_tank_2)
        print(results)

    except Exception as ex:
        exception = ex
        print(f"Encountered Error: {ex}")
        print()

    finally:
        # step 12
        print()
        print()
        print()
        print("Cleaning up")
        print("Deleting the stream")
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_PRESSURE_NAME))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TEMP_NAME))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TANK_0))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TANK_1))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_TANK_2))

        print("Deleting the types")
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, TYPE_PRESSURE_TEMPERATURE_TIME_NAME))
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, TYPE_VALUE_TIME_NAME))

        if test and exception is not None:
            raise exception
    print('Complete!')


if __name__ == '__main__':
    main()
