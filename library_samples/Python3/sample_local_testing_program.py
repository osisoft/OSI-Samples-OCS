
from ocs_sample_library_preview import *
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
sampleDataViewDescription_modified = "A longer sample description that "\
                                     "describes that this Data View is just "\
                                     "used for our sample and this part shows"\
                                     " a put."

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
fieldSourceForSectioner = FieldSource.Id
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
        pv = str(random.uniform(0, 100))
        tv = str(random.uniform(50, 70))
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


def find_FieldSet(fieldSets, fieldSetSourceType):
    for fieldSet in fieldSets:
        if fieldSet.SourceType == fieldSetSourceType:
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

        # Step 0
        ocsClient = OCSClient(config.get('Access', 'ApiVersion'),
                              config.get('Access', 'Tenant'),
                              config.get('Access', 'Resource'),
                              config.get('Credentials', 'ClientId'),
                              config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')

        print(namespaceId)
        print(ocsClient.uri)

        # Step 0.5
        if needData:
            createData(ocsClient)

        # Step 1

        dataView = DataView(id=sampleDataViewId)
        print
        print("Creating Data View")
        dataViews = ocsClient.DataViews.postDataView(namespaceId, dataView)

        # Step 2
        print
        print("Getting Data View")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

        # Step 3
        print
        print("Updating Data View")

        dv.Description = sampleDataViewDescription_modified
        query = Query(id=queryID, value=queryString)
        dv.Queries.append(query)
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print("Getting updated Data View")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

        assert len(dv.Queries) > 0, "Error getting back Dataview with queries"

        # Step 4
        print
        print("Getting ResolvedDataItems")

        dataItems = ocsClient.DataViews.getResolvedDataItems(
            namespaceId, sampleDataViewId, queryID)
        print(dataItems.toJson())

        print
        print("Getting ResolvedIneligibleDataItems")
        dataItems = ocsClient.DataViews.getResolvedIneligibleDataItems(
            namespaceId, sampleDataViewId, queryID)
        print(dataItems.toJson())

        # Step 5
        print
        print("Getting AvailableFieldSets")

        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, queryID)
        print(availablefields.toJson())

        # Step 6
        fields = availablefields.Items

        dv.FieldSets = fields

        print("Updating Data View")
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print("Now AvailableFieldSets")
        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, queryID)
        print(availablefields.toJson())

        print
        print("Retrieving data from the Data View")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) == 0, "Error getting back data"

        # Step 7
        section = Field(source=fieldSourceForSectioner,
                        label="{DistinguisherValue} {FirstKey}")
        dv.Sectioners.append(section)

        print("Updating Data View with sectioner")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print
        print("Retrieving data from the Data View")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) == 0, "Error getting back data"

        # Step 8

        print
        print("Now AvailableFieldSets")
        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, queryID)
        print(availablefields.toJson())

        dvDataItemFieldSet = find_FieldSet(
            dv.FieldSets, FieldSetSourceType.DataItem)
        field = find_Field(dvDataItemFieldSet.Fields, fieldSourceForSectioner)
        dvDataItemFieldSet.Fields.remove(field)
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        # Step 9
        print("Setting up distinguisher")

        field = find_FieldSet(dv.FieldSets, FieldSetSourceType.DataItem)
        field.Distinguisher = dv.Sectioners[0]
        dv.Sectioners = []

        print("Updating Data View with distinguisher")
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print
        print("Retrieving data from the Data View")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) == 0, "Error getting back data"

        # Step 10
        print
        print("Consolidating data")

        field1 = find_Field_Key(dvDataItemFieldSet.Fields,
                                FieldSource.PropertyId, fieldToConsolidateTo)
        field2 = find_Field_Key(dvDataItemFieldSet.Fields,
                                FieldSource.PropertyId, fieldToConsolidate)
        print(field1.toJson())
        print(field2.toJson())
        field1.Keys.append(fieldToConsolidate)
        dvDataItemFieldSet.Fields.remove(field2)

        print("Updating Data View with consildation")
        # No Data View returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print
        print("Retrieving data from the Data View")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id=namespaceId, dataView_id=sampleDataViewId, startIndex=startTime,
            endIndex=endTime, interval=interval)
        print(str(dataViewDataPreview1))
        assert len(dataViewDataPreview1) == 0, "Error getting back data"

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

        print
        print
        print("Deleting Data View")

        # Step 11
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
            print("Deleting added Streams")
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleStreamId))
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleStreamId2))

            print("Deleting added Types")
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, sampleTypeId))
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, samplePressureId2))
        if test and not success:
            raise exception


main()
print("done")

# Straightforward test to make sure program is working using asserts in
# program.  Can run it yourself with pytest program.py


def test_main():
    main(True)
