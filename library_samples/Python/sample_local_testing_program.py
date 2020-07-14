
from ocs_sample_library_preview import DataView, Field, FieldSource, OCSClient, Query, SdsStream, SdsType, SdsTypeCode, SdsTypeProperty
import configparser
import datetime
import time
import math
import inspect
import collections
import traceback

###############################################################################
# The following define the identifiers we'll use throughout
###############################################################################

sampleDataViewId = "DataView_Sample"
sampleDataViewName = "DataView_Sample_Name"
sampleDataViewDescription = "A Sample Description that describes that this "\
                            "Data View is just used for our sample."
sampleTypeId = "Time_SampleType"
samplePressureId2 = "Time_SampleType_old"
sampleStreamId = "dvTank2"
sampleStreamName = "Tank2"
sampleStreamId2 = "dvTank100"
sampleStreamName2 = "Tank100"

# In this example we will keep the SDS code in its own function.
# The variable needData is used in the main program to decide if we need to do
# this. In the rest of the code it is assumed this is used.
# The SDS code is not highlighted, but should be straightforward to follow.
# It creates enough Types, Streams and Data to see a result.
# For more details on the creating SDS objects see the SDS python example.

# This is kept seperate because chances are your data collection will occur at
# a different time then your creation of Data Views, but for a complete
# example we assume a blank start.

needData = True
namespaceId = ''
config = configparser.ConfigParser()
config.read('config.ini')
startTime = None
endTime = None
interval = "00:20:00"
queryID = "stream"
fieldSourceForGrouping = FieldSource.Id
queryString = "dvTank*"
fieldToConsolidateTo = "temperature"
fieldToConsolidate = "ambient_temp"


def suppressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))


def createData(ocsClient):
    import random
    global namespaceId, startTime, endTime

    doubleType = SdsType(id="doubleType", sdsTypeCode=SdsTypeCode.Double)
    dateTimeType = SdsType(id="dateTimeType", sdsTypeCode=SdsTypeCode.DateTime)

    pressureDoubleProperty = SdsTypeProperty(id="pressure", sdsType=doubleType)
    temperatureDoubleProperty = SdsTypeProperty(id=fieldToConsolidateTo,
                                                sdsType=doubleType)
    ambientTemperatureDoubleProperty = SdsTypeProperty(id=fieldToConsolidate,
                                                       sdsType=doubleType)
    timeDateTimeProperty = SdsTypeProperty(id="time", sdsType=dateTimeType,
                                           isKey=True)

    sDSType1 = SdsType(
        id=sampleTypeId,
        description="This is a sample Sds type for storing Pressure type "
                    "events for Data Views",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty, temperatureDoubleProperty, timeDateTimeProperty])

    sDSType2 = SdsType(
        id=samplePressureId2,
        description="This is a new sample Sds type for storing Pressure type "
                    "events for Data Views",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty, ambientTemperatureDoubleProperty, timeDateTimeProperty])

    print('Creating SDS Type')
    ocsClient.Types.getOrCreateType(namespaceId, sDSType1)
    ocsClient.Types.getOrCreateType(namespaceId, sDSType2)

    stream1 = SdsStream(
        id=sampleStreamId,
        name=sampleStreamName,
        description="A Stream to store the sample Pressure events",
        typeId=sampleTypeId)

    stream2 = SdsStream(
        id=sampleStreamId2,
        name=sampleStreamName2,
        description="A Stream to store the sample Pressure events",
        typeId=samplePressureId2)

    print('Creating SDS Streams')
    ocsClient.Streams.createOrUpdateStream(namespaceId, stream1)
    ocsClient.Streams.createOrUpdateStream(namespaceId, stream2)

    start = datetime.datetime.now() - datetime.timedelta(hours=1)
    endTime = datetime.datetime.now()

    values = []
    values2 = []

    def valueWithTime(timestamp, value, fieldName, value2):
        return f'{{"time": "{timestamp}", "pressure": {str(value)}, "{fieldName}": {str(value2)}}}'

    print('Generating Values')
    for i in range(1, 30, 1):
        timestamp = (start + datetime.timedelta(minutes=i * 2)
                     ).isoformat(timespec='seconds')
        pVal = valueWithTime(timestamp, random.uniform(
            0, 100), fieldToConsolidateTo, random.uniform(50, 70))
        pVal2 = valueWithTime(timestamp, random.uniform(
            0, 100), fieldToConsolidate, random.uniform(50, 70))

        values.append(pVal)
        values2.append(pVal2)

    print('Sending Values')
    ocsClient.Streams.insertValues(
        namespaceId,
        sampleStreamId,
        str(values).replace("'", ""))
    ocsClient.Streams.insertValues(
        namespaceId,
        sampleStreamId2,
        str(values2).replace("'", ""))
    startTime = start


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

    try:
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

        # Step 2
        print()
        print ("Step 2: Create types, streams, and data")
        if needData:
            createData(ocsClient)

        # Step 3
        print()
        print("Step 3: Create a data view")
        dataView = DataView(id=sampleDataViewId,name=sampleDataViewName,description=sampleDataViewDescription)
        dataViews = ocsClient.DataViews.postDataView(namespaceId, dataView)

        # Step 4
        print()
        print("Step 4: Retrieve the data view")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

        # Step 5
        print()
        print("Step 5: Add a query for data items")
        query = Query(id=queryID, value=queryString)
        dv.Queries.append(query)
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        # Step 6
        print()
        print("Step 6: View items found by the query")
        print("List data items found by the query:")
        dataItems = ocsClient.DataViews.getResolvedDataItems(
            namespaceId, sampleDataViewId, queryID)
        print(dataItems.toJson())

        print("List ineligible data items found by the query:")
        dataItems = ocsClient.DataViews.getResolvedIneligibleDataItems(
            namespaceId, sampleDataViewId, queryID)
        print(dataItems.toJson())

        # Step 7
        print()
        print("Step 7: View fields available to include in the data view")
        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId)
        print(availablefields.toJson())

        # Step 8
        print()
        print("Step 8: Include some of the available fields")
        dv.DataFieldSets = availablefields.Items
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print("List available field sets:")
        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId)
        print(availablefields.toJson())

        print("Retrieving data from the data view:")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        print(len(dataViewDataPreview1))
        assert len(dataViewDataPreview1) > 0, "Error getting back data"

        # Step 9
        print()
        print("Step 9: Group the data view")
        grouping = Field(source=fieldSourceForGrouping,
                        label="{DistinguisherValue} {FirstKey}")
        dv.GroupingFields.append(grouping)
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print("Retrieving data from the data view:")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) > 0, "Error getting back data"

        # Step 10
        print()
        print("Step 10: Identify data items")
        identify = dv.GroupingFields.pop()
        dvDataItemFieldSet = find_FieldSet(dv.DataFieldSets, queryID)
        dvDataItemFieldSet.IdentifyingField = identify
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print("Retrieving data from the data view:")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) > 0, "Error getting back data"

        # Step 11
        print()
        print("Step 11: Consolidate data fields")
        field1 = find_Field_Key(dvDataItemFieldSet.DataFields,
                                FieldSource.PropertyId, fieldToConsolidateTo)
        field2 = find_Field_Key(dvDataItemFieldSet.DataFields,
                                FieldSource.PropertyId, fieldToConsolidate)
        print(field1.toJson())
        print(field2.toJson())
        field1.Keys.append(fieldToConsolidate)
        dvDataItemFieldSet.DataFields.remove(field2)
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print("Retrieving data from the data view:")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) > 0, "Error getting back data"

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
        dv = None
        try:
            dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        except Exception as ex:
            # Exception is expected here since Data View has been deleted
            dv = None
        finally:
            assert dv is None, 'Delete failed'
            print("Verification OK: Data View deleted")

        if needData:
            print("Deleting sample streams...")
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleStreamId))
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleStreamId2))

            print("Deleting sample types...")
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, sampleTypeId))
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, samplePressureId2))
        if test and not success:
            raise exception


main()
print("Complete!")

# Straightforward test to make sure program is working using asserts in
# program.  Can run it yourself with pytest program.py


def test_main():
    main(True)
