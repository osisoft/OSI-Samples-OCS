"""This sample script demonstrates how to invoke the Data View REST API"""

# Disable pylint warnings:
# Allow catching general exception Exception (broad-except)
# pylint: disable=W0703
# Allow more than 15 local variables (too-many-locals)
# pylint: disable=R0914
# Allow more than 50 statements (too-many-statements)
# pylint: disable=R0915

import configparser
import datetime
import random
import traceback
from ocs_sample_library_preview import (DataView, Field, FieldSource, OCSClient, Query, SdsStream,
                                        SdsType, SdsTypeCode, SdsTypeProperty)

# Sample Data Information
SAMPLE_TYPE_ID_1 = 'Time_SampleType1'
SAMPLE_TYPE_ID_2 = 'Time_SampleType2'
SAMPLE_STREAM_ID_1 = 'dvTank2'
SAMPLE_STREAM_NAME_1 = 'Tank2'
SAMPLE_STREAM_ID_2 = 'dvTank100'
SAMPLE_STREAM_NAME_2 = 'Tank100'
SAMPLE_FIELD_TO_CONSOLIDATE_TO = 'temperature'
SAMPLE_FIELD_TO_CONSOLIDATE = 'ambient_temp'

# Data View Information
SAMPLE_DATAVIEW_ID = 'DataView_Sample'
SAMPLE_DATAVIEW_NAME = 'DataView_Sample_Name'
SAMPLE_DATAVIEW_DESCRIPTION = 'A Sample Description that describes that this '\
    'Data View is just used for our sample.'
SAMPLE_QUERY_ID = 'stream'
SAMPLE_QUERY_STRING = 'dvTank*'
SAMPLE_INTERVAL = '00:20:00'


def suppress_error(sds_call):
    """Suppresses an error thrown by SDS"""
    try:
        sds_call()
    except Exception as error:
        print(('Encountered Error: {error}'.format(error=error)))


def find_field(fieldset_fields, field_source):
    """Find a field by field source"""
    for field in fieldset_fields:
        if field.Source == field_source:
            return field
    return None


def find_fieldset(fieldsets, fieldset_query_id):
    """Find a fieldset by query id"""
    for fieldset in fieldsets:
        if fieldset.QueryId == fieldset_query_id:
            return fieldset
    return None


def find_field_key(fieldset_fields, field_source, key):
    """Find a field by source and key"""
    for field in fieldset_fields:
        if field.Source == field_source and any(key in s for s in field.Keys):
            return field
    return None


def main(test=False):
    """This function is the main body of the Data View sample script"""
    exception = None

    config = configparser.ConfigParser()
    config.read('config.ini')

    print('--------------------------------------------------------------------')
    print(' ######                      #    #                 ######  #     # ')
    print(' #     #   ##   #####   ##   #    # # ###### #    # #     #  #   #  ')
    print(' #     #  #  #    #    #  #  #    # # #      #    # #     #   # #   ')
    print(' #     # #    #   #   #    # #    # # #####  #    # ######     #    ')
    print(' #     # ######   #   ###### #    # # #      # ## # #          #    ')
    print(' #     # #    #   #   #    #  #  #  # #      ##  ## #          #    ')
    print(' ######  #    #   #   #    #   ##   # ###### #    # #          #    ')
    print('--------------------------------------------------------------------')

    # Step 1
    print()
    print('Step 1: Authenticate against OCS')
    ocs_client = OCSClient(config.get('Access', 'ApiVersion'),
                           config.get('Access', 'Tenant'),
                           config.get('Access', 'Resource'),
                           config.get('Credentials', 'ClientId'),
                           config.get('Credentials', 'ClientSecret'))

    namespace_id = config.get('Configurations', 'Namespace')

    print(namespace_id)
    print(ocs_client.uri)

    try:

        # Step 2
        print()
        print('Step 2: Create types, streams, and data')
        times = create_data(namespace_id, ocs_client)
        sample_start_time = times[0]
        sample_end_time = times[1]

        # Step 3
        print()
        print('Step 3: Create a data view')
        dataview = DataView(id=SAMPLE_DATAVIEW_ID, name=SAMPLE_DATAVIEW_NAME,
                            description=SAMPLE_DATAVIEW_DESCRIPTION)
        ocs_client.DataViews.postDataView(namespace_id, dataview)

        # Step 4
        print()
        print('Step 4: Retrieve the data view')
        dataview = ocs_client.DataViews.getDataView(
            namespace_id, SAMPLE_DATAVIEW_ID)
        print(dataview.toJson())

        # Step 5
        print()
        print('Step 5: Add a query for data items')
        query = Query(id=SAMPLE_QUERY_ID, value=SAMPLE_QUERY_STRING)
        dataview.Queries.append(query)
        # No Data View returned, success is 204
        ocs_client.DataViews.putDataView(namespace_id, dataview)

        # Step 6
        print()
        print('Step 6: View items found by the query')
        print('List data items found by the query:')
        data_items = ocs_client.DataViews.getResolvedDataItems(
            namespace_id, SAMPLE_DATAVIEW_ID, SAMPLE_QUERY_ID)
        print(data_items.toJson())

        print('List ineligible data items found by the query:')
        data_items = ocs_client.DataViews.getResolvedIneligibleDataItems(
            namespace_id, SAMPLE_DATAVIEW_ID, SAMPLE_QUERY_ID)
        print(data_items.toJson())

        # Step 7
        print()
        print('Step 7: View fields available to include in the data view')
        available_fields = ocs_client.DataViews.getResolvedAvailableFieldSets(
            namespace_id, SAMPLE_DATAVIEW_ID)
        print(available_fields.toJson())

        # Step 8
        print()
        print('Step 8: Include some of the available fields')
        dataview.DataFieldSets = available_fields.Items
        ocs_client.DataViews.putDataView(namespace_id, dataview)

        print('List available field sets:')
        available_fields = ocs_client.DataViews.getResolvedAvailableFieldSets(
            namespace_id, SAMPLE_DATAVIEW_ID)
        print(available_fields.toJson())

        print('Retrieving data from the data view:')
        dataview_data = ocs_client.DataViews.getDataInterpolated(
            namespace_id=namespace_id, dataView_id=SAMPLE_DATAVIEW_ID, startIndex=sample_start_time,
            endIndex=sample_end_time, interval=SAMPLE_INTERVAL)
        print(str(dataview_data))
        print(len(dataview_data))
        assert len(dataview_data) > 0, 'Error getting data view data'

        # Step 9
        print()
        print('Step 9: Group the data view')
        grouping = Field(source=FieldSource.Id,
                         label='{DistinguisherValue} {FirstKey}')
        dataview.GroupingFields.append(grouping)
        # No DataView returned, success is 204
        ocs_client.DataViews.putDataView(namespace_id, dataview)

        print('Retrieving data from the data view:')
        dataview_data = ocs_client.DataViews.getDataInterpolated(
            namespace_id=namespace_id, dataView_id=SAMPLE_DATAVIEW_ID, startIndex=sample_start_time,
            endIndex=sample_end_time, interval=SAMPLE_INTERVAL)
        print(str(dataview_data))
        assert len(dataview_data) > 0, 'Error getting data view data'

        # Step 10
        print()
        print('Step 10: Identify data items')
        identify = dataview.GroupingFields.pop()
        dataview_dataitem_fieldset = find_fieldset(
            dataview.DataFieldSets, SAMPLE_QUERY_ID)
        dataview_dataitem_fieldset.IdentifyingField = identify
        # No Data View returned, success is 204
        ocs_client.DataViews.putDataView(namespace_id, dataview)

        print('Retrieving data from the data view:')
        dataview_data = ocs_client.DataViews.getDataInterpolated(
            namespace_id=namespace_id, dataView_id=SAMPLE_DATAVIEW_ID, startIndex=sample_start_time,
            endIndex=sample_end_time, interval=SAMPLE_INTERVAL)
        print(str(dataview_data))
        assert len(dataview_data) > 0, 'Error getting data view data'

        # Step 11
        print()
        print('Step 11: Consolidate data fields')
        field1 = find_field_key(dataview_dataitem_fieldset.DataFields,
                                FieldSource.PropertyId, SAMPLE_FIELD_TO_CONSOLIDATE_TO)
        field2 = find_field_key(dataview_dataitem_fieldset.DataFields,
                                FieldSource.PropertyId, SAMPLE_FIELD_TO_CONSOLIDATE)
        print(field1.toJson())
        print(field2.toJson())
        field1.Keys.append(SAMPLE_FIELD_TO_CONSOLIDATE)
        dataview_dataitem_fieldset.DataFields.remove(field2)
        # No Data View returned, success is 204
        ocs_client.DataViews.putDataView(namespace_id, dataview)

        print('Retrieving data from the data view:')
        dataview_data = ocs_client.DataViews.getDataInterpolated(
            namespace_id=namespace_id, dataView_id=SAMPLE_DATAVIEW_ID, startIndex=sample_start_time,
            endIndex=sample_end_time, interval=SAMPLE_INTERVAL)
        print(str(dataview_data))
        assert len(dataview_data) > 0, 'Error getting data view data'

    except Exception as error:
        print((f'Encountered Error: {error}'))
        print()
        traceback.print_exc()
        print()
        exception = error

    finally:

        #######################################################################
        # Data View deletion
        #######################################################################

        # Step 12
        print()
        print('Step 12: Delete sample objects from OCS')
        print('Deleting data view...')

        suppress_error(lambda: ocs_client.DataViews.deleteDataView(
            namespace_id, SAMPLE_DATAVIEW_ID))

        # check, including assert is added to make sure we deleted it
        dataview = None
        try:
            dataview = ocs_client.DataViews.getDataView(
                namespace_id, SAMPLE_DATAVIEW_ID)
        except Exception as error:
            # Exception is expected here since Data View has been deleted
            dataview = None
        finally:
            assert dataview is None, 'Delete failed'
            print('Verification OK: Data View deleted')

        print('Deleting sample streams...')
        suppress_error(lambda: ocs_client.Streams.deleteStream(
            namespace_id, SAMPLE_STREAM_ID_1))
        suppress_error(lambda: ocs_client.Streams.deleteStream(
            namespace_id, SAMPLE_STREAM_ID_2))

        print('Deleting sample types...')
        suppress_error(lambda: ocs_client.Types.deleteType(
            namespace_id, SAMPLE_TYPE_ID_1))
        suppress_error(lambda: ocs_client.Types.deleteType(
            namespace_id, SAMPLE_TYPE_ID_2))

        if test and exception is not None:
            raise exception
    print('Complete!')


def create_data(namespace_id, ocs_client):
    """Creates sample data for the script to use"""

    double_type = SdsType(id='doubleType', sdsTypeCode=SdsTypeCode.Double)
    datetime_type = SdsType(
        id='dateTimeType', sdsTypeCode=SdsTypeCode.DateTime)

    pressure_property = SdsTypeProperty(id='pressure', sdsType=double_type)
    temperature_property = SdsTypeProperty(id=SAMPLE_FIELD_TO_CONSOLIDATE_TO,
                                           sdsType=double_type)
    ambient_temperature_property = SdsTypeProperty(id=SAMPLE_FIELD_TO_CONSOLIDATE,
                                                   sdsType=double_type)
    time_property = SdsTypeProperty(id='time', sdsType=datetime_type,
                                    isKey=True)

    sds_type_1 = SdsType(
        id=SAMPLE_TYPE_ID_1,
        description='This is a sample Sds type for storing Pressure type '
                    'events for Data Views',
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressure_property, temperature_property, time_property])

    sds_type_2 = SdsType(
        id=SAMPLE_TYPE_ID_2,
        description='This is a new sample Sds type for storing Pressure type '
                    'events for Data Views',
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressure_property, ambient_temperature_property, time_property])

    print('Creating SDS Types...')
    ocs_client.Types.getOrCreateType(namespace_id, sds_type_1)
    ocs_client.Types.getOrCreateType(namespace_id, sds_type_2)

    stream1 = SdsStream(
        id=SAMPLE_STREAM_ID_1,
        name=SAMPLE_STREAM_NAME_1,
        description='A Stream to store the sample Pressure events',
        typeId=SAMPLE_TYPE_ID_1)

    stream2 = SdsStream(
        id=SAMPLE_STREAM_ID_2,
        name=SAMPLE_STREAM_NAME_2,
        description='A Stream to store the sample Pressure events',
        typeId=SAMPLE_TYPE_ID_2)

    print('Creating SDS Streams...')
    ocs_client.Streams.createOrUpdateStream(namespace_id, stream1)
    ocs_client.Streams.createOrUpdateStream(namespace_id, stream2)

    sample_start_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    sample_end_time = datetime.datetime.now()

    values1 = []
    values2 = []

    def value_with_time(timestamp, value, field_name, value2):
        """Formats a JSON data object"""
        return f'{{"time": "{timestamp}", "pressure": {str(value)}, "{field_name}": {str(value2)}}}'

    print('Generating values...')
    for i in range(1, 30, 1):
        timestamp = (sample_start_time + datetime.timedelta(minutes=i * 2)
                     ).isoformat(timespec='seconds')
        val1 = value_with_time(timestamp, random.uniform(
            0, 100), SAMPLE_FIELD_TO_CONSOLIDATE_TO, random.uniform(50, 70))
        val2 = value_with_time(timestamp, random.uniform(
            0, 100), SAMPLE_FIELD_TO_CONSOLIDATE, random.uniform(50, 70))

        values1.append(val1)
        values2.append(val2)

    print('Sending values...')
    ocs_client.Streams.insertValues(
        namespace_id,
        SAMPLE_STREAM_ID_1,
        str(values1).replace("'", ""))
    ocs_client.Streams.insertValues(
        namespace_id,
        SAMPLE_STREAM_ID_2,
        str(values2).replace("'", ""))

    return (sample_start_time, sample_end_time)


if __name__ == '__main__':
    main()
