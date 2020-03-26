
from ocs_sample_library_preview import DataView, Field, FieldSource, OCSClient, Query, SdsStream, SdsType, SdsTypeCode, SdsTypeProperty
import configparser
import datetime
import time
import math
import inspect
import collections
import traceback

# Sample Data Information
sampleTypeId1 = "Time_SampleType1"
sampleTypeId2 = "Time_SampleType2"
sampleStreamId1 = "dvTank2"
sampleStreamName1 = "Tank2"
sampleStreamId2 = "dvTank100"
sampleStreamName2 = "Tank100"
sampleFieldToConsolidateTo = "temperature"
sampleFieldToConsolidate = "ambient_temp"
sampleStartTime = None
sampleEndTime = None

# Data View Information
sampleDataViewId = "DataView_Sample"
sampleDataViewName = "DataView_Sample_Name"
sampleDataViewDescription = "A Sample Description that describes that this "\
                            "Data View is just used for our sample."
sampleQueryId = "stream"
sampleQueryString = "dvTank*"
sampleInterval = "00:20:00"

needData = True
namespaceId = ''
config = configparser.ConfigParser()
config.read('config.ini')


def suppressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))


def find_Field(fieldSetFields, fieldSource):
    for field in fieldSetFields:
        if field.Source == fieldSource:
            return field


def find_FieldSet(fieldSets, fieldSetQueryId):
    for fieldSet in fieldSets:
        if fieldSet.QueryId == fieldSetQueryId:
            return fieldSet


def find_Field_Key(fieldSetFields, fieldSource, key):
    for field in fieldSetFields:
        if field.Source == fieldSource and any(key in s for s in field.Keys):
            return field


def main(test=False):
    global namespaceId
    success = True
    exception = {}

    print("--------------------------------------------------------------------")
    print(" ######                      #    #                 ######  #     # ")
    print(" #     #   ##   #####   ##   #    # # ###### #    # #     #  #   #  ")
    print(" #     #  #  #    #    #  #  #    # # #      #    # #     #   # #   ")
    print(" #     # #    #   #   #    # #    # # #####  #    # ######     #    ")
    print(" #     # ######   #   ###### #    # # #      # ## # #          #    ")
    print(" #     # #    #   #   #    #  #  #  # #      ##  ## #          #    ")
    print(" ######  #    #   #   #    #   ##   # ###### #    # #          #    ")
    print("--------------------------------------------------------------------")

    # Step 1
    print()
    print("Step 1: Authenticate against OCS")
    ocsClient = OCSClient(config.get('Access', 'ApiVersion'),
                          config.get('Access', 'Tenant'),
                          config.get('Access', 'Resource'),
                          config.get('Credentials', 'ClientId'),
                          config.get('Credentials', 'ClientSecret'))

    namespaceId = config.get('Configurations', 'Namespace')

    print(namespaceId)
    print(ocsClient.uri)

    try:

        # Step 2
        print()
        print("Step 2: Create types, streams, and data")
        if needData:
            createData(ocsClient)

        # Step 3
        print()
        print("Step 3: Create a data view")
        dataView = DataView(id=sampleDataViewId, name=sampleDataViewName,
                            description=sampleDataViewDescription)
        ocsClient.DataViews.postDataView(namespaceId, dataView)

        # Step 4
        print()
        print("Step 4: Retrieve the data view")
        dataView = ocsClient.DataViews.getDataView(
            namespaceId, sampleDataViewId)
        print(dataView.toJson())

        # Step 5
        print()
        print("Step 5: Add a query for data items")
        query = Query(id=sampleQueryId, value=sampleQueryString)
        dataView.Queries.append(query)
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dataView)

        # Step 6
        print()
        print("Step 6: View items found by the query")
        print("List data items found by the query:")
        dataItems = ocsClient.DataViews.getResolvedDataItems(
            namespaceId, sampleDataViewId, sampleQueryId)
        print(dataItems.toJson())

        print("List ineligible data items found by the query:")
        dataItems = ocsClient.DataViews.getResolvedIneligibleDataItems(
            namespaceId, sampleDataViewId, sampleQueryId)
        print(dataItems.toJson())

        # Step 7
        print()
        print("Step 7: View fields available to include in the data view")
        availableFields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId)
        print(availableFields.toJson())

        # Step 8
        print()
        print("Step 8: Include some of the available fields")
        dataView.DataFieldSets = availableFields.Items
        ocsClient.DataViews.putDataView(namespaceId, dataView)

        print("List available field sets:")
        availableFields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId)
        print(availableFields.toJson())

        print("Retrieving data from the data view:")
        dataViewData = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=sampleStartTime,
            endIndex=sampleEndTime, interval=sampleInterval)
        print(str(dataViewData))
        print(len(dataViewData))
        assert len(dataViewData) > 0, "Error getting data view data"

        # Step 9
        print()
        print("Step 9: Group the data view")
        grouping = Field(source=FieldSource.Id,
                         label="{DistinguisherValue} {FirstKey}")
        dataView.GroupingFields.append(grouping)
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dataView)

        print("Retrieving data from the data view:")
        dataViewData = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=sampleStartTime,
            endIndex=sampleEndTime, interval=sampleInterval)
        print(str(dataViewData))
        assert len(dataViewData) > 0, "Error getting data view data"

        # Step 10
        print()
        print("Step 10: Identify data items")
        identify = dataView.GroupingFields.pop()
        dvDataItemFieldSet = find_FieldSet(
            dataView.DataFieldSets, sampleQueryId)
        dvDataItemFieldSet.IdentifyingField = identify
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dataView)

        print("Retrieving data from the data view:")
        dataViewData = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=sampleStartTime,
            endIndex=sampleEndTime, interval=sampleInterval)
        print(str(dataViewData))
        assert len(dataViewData) > 0, "Error getting data view data"

        # Step 11
        print()
        print("Step 11: Consolidate data fields")
        field1 = find_Field_Key(dvDataItemFieldSet.DataFields,
                                FieldSource.PropertyId, sampleFieldToConsolidateTo)
        field2 = find_Field_Key(dvDataItemFieldSet.DataFields,
                                FieldSource.PropertyId, sampleFieldToConsolidate)
        print(field1.toJson())
        print(field2.toJson())
        field1.Keys.append(sampleFieldToConsolidate)
        dvDataItemFieldSet.DataFields.remove(field2)
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dataView)

        print("Retrieving data from the data view:")
        dataViewData = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=sampleStartTime,
            endIndex=sampleEndTime, interval=sampleInterval)
        print(str(dataViewData))
        assert len(dataViewData) > 0, "Error getting data view data"

    except Exception as ex:
        print((f"Encountered Error: {ex}"))
        print
        traceback.print_exc()
        print
        success = False
        exception = ex

    finally:

        #######################################################################
        # Data View deletion
        #######################################################################

        # Step 12
        print()
        print("Step 12: Delete sample objects from OCS")
        print("Deleting data view...")

        suppressError(lambda: ocsClient.DataViews.deleteDataView(
            namespaceId, sampleDataViewId))

        # check, including assert is added to make sure we deleted it
        dataView = None
        try:
            dataView = ocsClient.DataViews.getDataView(
                namespaceId, sampleDataViewId)
        except Exception as ex:
            # Exception is expected here since Data View has been deleted
            dataView = None
        finally:
            assert dataView is None, 'Delete failed'
            print("Verification OK: Data View deleted")

        if needData:
            print("Deleting sample streams...")
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleStreamId1))
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleStreamId2))

            print("Deleting sample types...")
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, sampleTypeId1))
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, sampleTypeId2))
        if test and not success:
            raise exception


def createData(ocsClient):
    import random
    global namespaceId, sampleStartTime, sampleEndTime

    doubleType = SdsType(id="doubleType", sdsTypeCode=SdsTypeCode.Double)
    dateTimeType = SdsType(id="dateTimeType", sdsTypeCode=SdsTypeCode.DateTime)

    pressureDoubleProperty = SdsTypeProperty(id="pressure", sdsType=doubleType)
    temperatureDoubleProperty = SdsTypeProperty(id=sampleFieldToConsolidateTo,
                                                sdsType=doubleType)
    ambientTemperatureDoubleProperty = SdsTypeProperty(id=sampleFieldToConsolidate,
                                                       sdsType=doubleType)
    timeDateTimeProperty = SdsTypeProperty(id="time", sdsType=dateTimeType,
                                           isKey=True)

    sdsType1 = SdsType(
        id=sampleTypeId1,
        description="This is a sample Sds type for storing Pressure type "
                    "events for Data Views",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty, temperatureDoubleProperty, timeDateTimeProperty])

    sdsType2 = SdsType(
        id=sampleTypeId2,
        description="This is a new sample Sds type for storing Pressure type "
                    "events for Data Views",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty, ambientTemperatureDoubleProperty, timeDateTimeProperty])

    print('Creating SDS Types...')
    ocsClient.Types.getOrCreateType(namespaceId, sdsType1)
    ocsClient.Types.getOrCreateType(namespaceId, sdsType2)

    stream1 = SdsStream(
        id=sampleStreamId1,
        name=sampleStreamName1,
        description="A Stream to store the sample Pressure events",
        typeId=sampleTypeId1)

    stream2 = SdsStream(
        id=sampleStreamId2,
        name=sampleStreamName2,
        description="A Stream to store the sample Pressure events",
        typeId=sampleTypeId2)

    print('Creating SDS Streams...')
    ocsClient.Streams.createOrUpdateStream(namespaceId, stream1)
    ocsClient.Streams.createOrUpdateStream(namespaceId, stream2)

    start = datetime.datetime.now() - datetime.timedelta(hours=1)
    sampleEndTime = datetime.datetime.now()

    values1 = []
    values2 = []

    def valueWithTime(timestamp, value, fieldName, value2):
        return f'{{"time": "{timestamp}", "pressure": {str(value)}, "{fieldName}": {str(value2)}}}'

    print('Generating values...')
    for i in range(1, 30, 1):
        timestamp = (start + datetime.timedelta(minutes=i * 2)
                     ).isoformat(timespec='seconds')
        val1 = valueWithTime(timestamp, random.uniform(
            0, 100), sampleFieldToConsolidateTo, random.uniform(50, 70))
        val2 = valueWithTime(timestamp, random.uniform(
            0, 100), sampleFieldToConsolidate, random.uniform(50, 70))

        values1.append(val1)
        values2.append(val2)

    print('Sending values...')
    ocsClient.Streams.insertValues(
        namespaceId,
        sampleStreamId1,
        str(values1).replace("'", ""))
    ocsClient.Streams.insertValues(
        namespaceId,
        sampleStreamId2,
        str(values2).replace("'", ""))
    sampleStartTime = start


main()
print("Complete!")

# Straightforward test to make sure program is working using asserts in
# program.  Can run it yourself with pytest program.py


def test_main():
    main(True)
