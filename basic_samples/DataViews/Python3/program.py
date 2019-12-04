from ocs_sample_library_preview import (
    SdsTypeCode, SdsType, SdsTypeProperty, SdsStream, OCSClient, DataView,
    DataViewQuery, DataViewGroupRule, DataViewMappings, DataViewIndexConfig)
import configparser
import datetime
import time
import traceback

###############################################################################
# The following define the identifiers we'll use throughout
###############################################################################

sampleDataViewId = "DataView_Sample"
sampleDataViewName = "DataView_Sample_Name"
sampleDataViewDescription = "A Sample Description that describes that this "\
                            "DataView is just used for our sample."
sampleDataViewDescription_modified = "A longer sample description that "\
                                     "describes that this DataView is just "\
                                     "used for our sample and this part shows"\
                                     " a put."

samplePressureTypeId = "Time_Pressure_SampleType"
samplePressureStreamId = "Tank_Pressure_SampleStream"
samplePressureStreamName = "Tank Pressure SampleStream"

sampleTemperatureTypeId = "Time_Temperature_SampleType"
sampleTemperatureStreamId = "Tank_Temperature_SampleStream"
sampleTemperatureStreamName = "Tank Temperature SampleStream"

# In this example we will keep the SDS code in its own function.
# The variable needData is used in the main program to decide if we need to do
# this. In the rest of the code it is assumed this is used.
# The SDS code is not highlighted, but should be straightforward to follow.
# It creates enough Types, Streams and Data to see a result.
# For more details on the creating SDS objects see the SDS python example.

# This is kept seperate because chances are your data collection will occur at
# a different time then your creation of DataViews, but for a complete
# example we assume a blank start.

needData = True
namespaceId = ''
config = configparser.ConfigParser()
config.read('config.ini')
startTime = None


def suppressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))


def createData(ocsClient):
    import random
    global namespaceId, startTime

    doubleType = SdsType(id="doubleType", sdsTypeCode=SdsTypeCode.Double)
    dateTimeType = SdsType(id="dateTimeType", sdsTypeCode=SdsTypeCode.DateTime)

    pressureDoubleProperty = SdsTypeProperty(id="pressure", sdsType=doubleType)
    temperatureDoubleProperty = SdsTypeProperty(id="temperature",
                                                sdsType=doubleType)
    timeDateTimeProperty = SdsTypeProperty(id="time", sdsType=dateTimeType,
                                           isKey=True)

    pressure_SDSType = SdsType(
        id=samplePressureTypeId,
        description="This is a sample Sds type for storing Pressure type "
                    "events for DataViews",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty, timeDateTimeProperty])
    temperature_SDSType = SdsType(
        id=sampleTemperatureTypeId,
        description="This is a sample Sds type for storing Temperature type "
                    "events for DataViews",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[temperatureDoubleProperty, timeDateTimeProperty])

    print('Creating SDS Type')
    ocsClient.Types.getOrCreateType(namespaceId, pressure_SDSType)
    ocsClient.Types.getOrCreateType(namespaceId, temperature_SDSType)

    pressureStream = SdsStream(
        id=samplePressureStreamId,
        name=samplePressureStreamName,
        description="A Stream to store the sample Pressure events",
        typeId=samplePressureTypeId)

    temperatureStream = SdsStream(
        id=sampleTemperatureStreamId,
        name=sampleTemperatureStreamName,
        description="A Stream to store the sample Temperature events",
        typeId=sampleTemperatureTypeId)

    print('Creating SDS Streams')
    ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
    ocsClient.Streams.createOrUpdateStream(namespaceId, temperatureStream)

    start = datetime.datetime.now() - datetime.timedelta(hours=1)

    pressureValues = []
    temperatureValues = []

    def valueWithTime(timestamp, sensor, value):
        return f'{{"time": "{timestamp}", "{sensor}": {str(value)} }}'

    print('Generating Values')
    for i in range(1, 30, 1):
        pv = str(random.uniform(0, 100))
        tv = str(random.uniform(50, 70))
        timestamp = (start + datetime.timedelta(minutes=i * 2)
                     ).isoformat(timespec='seconds')
        pVal = valueWithTime(timestamp, "pressure", random.uniform(0, 100))
        tVAl = valueWithTime(timestamp, "temperature", random.uniform(50, 70))

        pressureValues.append(pVal)
        temperatureValues.append(tVAl)

    print('Sending Pressure Values')
    ocsClient.Streams.insertValues(
        namespaceId,
        samplePressureStreamId,
        str(pressureValues).replace("'", ""))
    print('Sending Temperature Values')
    ocsClient.Streams.insertValues(
        namespaceId,
        sampleTemperatureStreamId,
        str(temperatureValues).replace("'", ""))
    startTime = start


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
        ocsClient = OCSClient(config.get('Access', 'ApiVersion'),
                              config.get('Access', 'Tenant'),
                              config.get('Access', 'Resource'),
                              config.get('Credentials', 'ClientId'),
                              config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')

        print(namespaceId)
        print(ocsClient.uri)

        # Step 2
        if needData:
            createData(ocsClient)

        sampleStreamId = "SampleStream"

        #######################################################################
        # DataViews
        #######################################################################

        # We need to create the DataView.
        # For our DataView we are going to combine the two streams that were
        # created, using a search to find the streams,
        # using common part of their name.

        # We are using the default mappings.
        # This means our columns will keep their original names.
        # Another typical use of columns is to change what stream properties
        # get mapped to which column.

        # Mappings allow you to rename a column in the results to something
        # different.  So if we want to we could rename Pressure to press.

        # We then define the IndexDataType.  Currently only
        # datetime is supported.

        # Next we need to define IndexConfig.  It holds the default
        # startIndex and endIndex to define a time period, mode (interpolated),
        # and interpolation interval.

        # Our results when looking at it like a table looks like:
        #
        # time,pressure,temperature
        # 2019-06-27T12:23:00Z,36.3668286389033,60.614978497887
        # 2019-06-27T12:24:00Z,36.3668286389033,60.614978497887
        # 2019-06-27T12:25:00Z,36.3668286389033,60.614978497887
        # 2019-06-27T12:26:00Z,40.5653155047711,59.4181700259214
        # 2019-06-27T12:27:00Z,54.5602717243303,55.4288084527031
        # ...

        # Step 3
        queryObj = DataViewQuery(sampleDataViewId, f"name:*{sampleStreamId}*")
        if startTime:
            indexConfigObj = DataViewIndexConfig(startIndex=startTime.isoformat(timespec='minutes'),
                                                 endIndex=(
                                                     startTime + datetime.timedelta(minutes=40)).isoformat(timespec='minutes'),
                                                 mode="Interpolated",
                                                 interval="00:01:00")
        else:
            indexConfigObj = None
        dataView = DataView(id=sampleDataViewId, queries=queryObj,
                            indexDataType="datetime",
                            name=sampleDataViewName,
                            indexConfig=indexConfigObj,
                            description=sampleDataViewDescription)
        print
        print("Creating DataView")
        print(dataView.toJson())
        dataViews = ocsClient.DataViews.postDataView(namespaceId, dataView)

        # Step 4
        print
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        # assert is added to make sure we get back what we are expecting
        expectedJSON = '{"Id": "DataView_Sample", "Queries": [{"Id": "DataView_Sample", "Query": "name:*SampleStream*"}], "Name": "DataView_Sample_Name", "Description": "A Sample Description that describes that this DataView is just used for our sample.", "IndexConfig": {"StartIndex": "2019-09-03T14:10:00.0000000Z", "EndIndex": "2019-09-03T14:50:00.0000000Z", "Mode": "Interpolated", "Interval": "00:01:00"}, "IndexDataType": "DateTime", "GroupRules": []}'

        dv.Description = sampleDataViewDescription_modified

        # Step 5
        print
        print("Updating DataView")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        # Step 6
        # Getting the complete set of DataViews to make sure it is there
        print
        print("Getting DataViews")
        dataViews = ocsClient.DataViews.getDataViews(namespaceId)
        for dataView1 in dataViews:
            if hasattr(dataView1, "Id"):
                print(dataView1.toJson())

        # Getting the DataGroups of the defined DataView.
        # The datgroup lets you see what is returned by the DataView Query.
        print
        print("Getting DataGroups")

        # Step 7
        # This works for the automated test.  You can use this or the below.
        dataGroups = ocsClient.DataViews.getDataGroups(
            namespaceId, sampleDataViewId, 0, 100, True)
        print('DataGroups')
        print(dataGroups)

        # By default the preview get interpolated values every minute over the
        # last hour, which lines up with our data that we sent in.

        # Beyond the normal API options, this function does have the option
        # to return the data in a class if you have created a Type for the
        # data you are retrieving.

        # Step 8
        print
        print("Retrieving data preview from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId)
        print(str(dataViewDataPreview1[0]))

        # Step 9
        print()
        print("Getting data as a table, separated by commas, with headers")
        # Get the first 20 rows, keep token for next 20 rows
        dataViewDataTable1, token = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId, form="csvh", count=20)

        # Display received 20 lines showing:
        #   * First lines with extrapolation (first value replicated of each stream)
        #   * Interpolated values at 1 minute interval, stream recorded at 2 minutes interval
        print(dataViewDataTable1)
        print()

        # Get the last 20 rows using token, then display (without row header)
        dataViewDataTable2, token = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId, form="csv", count=20, continuationToken=token)
        print(dataViewDataTable2, "\n\n")

        # Now override startIndex/endIndex/interval of previous DataView
        # Ask for last 5 minutes of data, aligned on the seconds, interpolated at 30 seconds
        startIndex = (startTime + datetime.timedelta(minutes=55)
                      ).isoformat(timespec='seconds')
        endIndex = (startTime + datetime.timedelta(minutes=60)
                    ).isoformat(timespec='seconds')
        dataViewDataTable3, token2 = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId, form="csvh", count=11, continuationToken=None,
            startIndex=startIndex, endIndex=endIndex, interval="00:00:30")
        print(dataViewDataTable3)
        assert token2 is None, "Continuation token is not None"

    except Exception as ex:
        print((f"Encountered Error: {ex}"))
        print
        traceback.print_exc()
        print
        success = False
        exception = ex

    finally:
        #######################################################################
        # DataView deletion
        #######################################################################

        print
        print
        print("Deleting DataView")

        # Step 10
        suppressError(lambda: ocsClient.DataViews.deleteDataView(
            namespaceId, sampleDataViewId))

        # check, including assert is added to make sure we deleted it
        dv = None
        try:
            dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        except Exception as ex:
            # Exception is expected here since DataView has been deleted
            dv = None
        finally:
            assert dv is None, 'Delete failed'
            print("Verification OK: DataView deleted")

        if needData:
            print("Deleting added Streams")
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, samplePressureStreamId))
            suppressError(lambda: ocsClient.Streams.deleteStream(
                namespaceId, sampleTemperatureStreamId))

            print("Deleting added Types")
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, samplePressureTypeId))
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, sampleTemperatureTypeId))
        if test and not success:
            raise exception


main()
print("done")

# Straightforward test to make sure program is working using asserts in
# program.  Can run it yourself with pytest program.py


def test_main():
    main(True)
