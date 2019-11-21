from ocs_sample_library_preview import *
import configparser
import datetime
import time
import math
import inspect
import collections
import traceback

######################################################################################################
# The following define the identifiers we'll use throughout
######################################################################################################

sampleDataViewId = "DataView_Sample"
sampleDataViewName = "DataView_Sample_Name"
sampleDataViewDescription = "A Sample Description that describes that this DataView is just used for our sample."
sampleDataViewDescription_modified = "A longer sample description that describes that this DataView is just used for our sample and this part shows a put."

samplePressureTypeId = "Time_Pressure_SampleType"
samplePressureStreamId = "Tank_Pressure_SampleStream"
samplePressureStreamName = "Tank Pressure SampleStream"

sampleTemperatureTypeId = "Time_Temperature_SampleType"
sampleTemperatureStreamId = "Tank_Temperature_SampleStream"
sampleTemperatureStreamName = "Tank Temperature SampleStream"

# In this example we will keep the SDS code in its own function.
# The variable needData is used in the main program to decide if we need to do this.
# In the rest of the code it is assumed this is used.
# The SDS code is not highlighted, but should be straightforward to follow.
# It creates enough Types, Streams and Data to see a result.  For more details on the creating SDS objects see the SDS python example.
# This is kept separate because chances are your data collection will occur at a different time then your creation of DataViews, but for a complete example we assume a blank start.

needData = True
namespaceId = ''
firstData = {}
config = configparser.ConfigParser()
config.read('config.ini')


def suppressError(sdsCall):
    try:
        sdsCall()
    except Exception as e:
        print(("Encountered Error: {error}".format(error=e)))


def createData(ocsClient):
    import random
    global namespaceId, firstData

    doubleType = SdsType(id="doubleType", sdsTypeCode=SdsTypeCode.Double)
    dateTimeType = SdsType(id="dateTimeType", sdsTypeCode=SdsTypeCode.DateTime)

    pressureDoubleProperty = SdsTypeProperty(id="pressure", sdsType=doubleType)
    temperatureDoubleProperty = SdsTypeProperty(
        id="temperature", sdsType=doubleType)
    timeDateTimeProperty = SdsTypeProperty(
        id="time", sdsType=dateTimeType, isKey=True)

    pressure_SDSType = SdsType(id=samplePressureTypeId, description="This is a sample Sds type for storing Pressure type events for DataViews",
                               sdsTypeCode=SdsTypeCode.Object, properties=[pressureDoubleProperty, timeDateTimeProperty])
    temperature_SDSType = SdsType(id=sampleTemperatureTypeId, description="This is a sample Sds type for storing Temperature type events for DataViews",
                                  sdsTypeCode=SdsTypeCode.Object, properties=[temperatureDoubleProperty, timeDateTimeProperty])

    print('Creating SDS Type')
    ocsClient.Types.getOrCreateType(namespaceId, pressure_SDSType)
    ocsClient.Types.getOrCreateType(namespaceId, temperature_SDSType)

    pressureStream = SdsStream(id=samplePressureStreamId, name=samplePressureStreamName,
                               description="A Stream to store the sample Pressure events", typeId=samplePressureTypeId)
    temperatureStream = SdsStream(id=sampleTemperatureStreamId, name=sampleTemperatureStreamName,
                                  description="A Stream to store the sample Temperature events", typeId=sampleTemperatureTypeId)

    print('Creating SDS Streams')
    ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
    ocsClient.Streams.createOrUpdateStream(namespaceId, temperatureStream)

    start = datetime.datetime.now() - datetime.timedelta(hours=1)

    pressureValues = []
    temperatureValues = []
    print('Sending Values')
    for i in range(1, 60, 1):
        pv = str(random.uniform(0, 100))
        tv = str(random.uniform(50, 70))
        pVal = ('{"time" : "' + (start + datetime.timedelta(minutes=i * 1)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")+'", "pressure":' + str(random.uniform(0, 100)) + '}')
        tVAl = ('{"time" : "' + (start + datetime.timedelta(minutes=i * 1)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")+'", "temperature":' + str(random.uniform(50, 70)) + '}')
        if i == 1:
            firstData = ('{"time" : "' + (start + datetime.timedelta(minutes=i * 1)).strftime(
                "%Y-%m-%dT%H:%M:%SZ")+'", "pressure":' + pv + ', "temperature":' + tv + '}')

        pressureValues.append(pVal)
        temperatureValues.append(tVAl)

    print('Sending Pressure Values')
    ocsClient.Streams.insertValues(
        namespaceId, samplePressureStreamId, str(pressureValues).replace("'", ""))
    print('Sending Temperature Values')
    ocsClient.Streams.insertValues(namespaceId, sampleTemperatureStreamId, str(
        temperatureValues).replace("'", ""))


def main(test=False):
    global namespaceId, firstData
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

        ocsClient = OCSClient(config.get('Access', 'ApiVersion'), config.get('Access', 'Tenant'), config.get('Access', 'Resource'),
                              config.get('Credentials', 'ClientId'), config.get('Credentials', 'ClientSecret'))

        namespaceId = config.get('Configurations', 'Namespace')

        print(namespaceId)
        print(ocsClient.uri)

        if needData:
            createData(ocsClient)

        sampleStreamId = "SampleStream"

        ######################################################################################################
        # DataViews
        ######################################################################################################

        # We need to create the DataView. DataViews are complex objects so we write out each step in the long comment below.
        # For our DataView we are going to combine the two streams that were created, using a search to find the streams, using common part of their name.
        # We are using the default mappings.  This means our columns will keep their original names.  Another typical use of columns is to change what stream properties get mapped to which column.
        # Mappings allow you to rename a column in the results to something different.  So if we want to we could rename Pressure to press.
        # We then define the IndexDataType.  Currently only datetime is supported.
        # Next we need to define the grouping rules.  Grouping decides how each row in the result is filled in.
        # In this case we are grouping by tag, which effectively squashes are results together so that way Pressure and Temperature and Time all get results in a row.
        # If we grouped by StreamName, each row would be filled is as fully as it can by each Stream name.  Giving us results with Pressure and Time seperate from Pressure and Temperature
        # Our results when looking at it like a table looks like:
        # time,DefaultGroupRule_Tags,pressure,temperature
        # 2019-02-18T18:50:17.1084594Z,(NoTags),13.8038967965309,57.6749982613741
        # 2019-02-18T18:51:17.1084594Z,(NoTags),13.8038967965309,57.674998261374
        # ....

        queryObj = DataViewQuery(
            sampleDataViewId, 'streams', 'name', sampleStreamId, 'Contains')
        groupRuleObj = DataViewGroupRule("DefaultGroupRule", "StreamTag")
        mappingObj = DataViewMappings(isDefault=True)

        dataView = DataView(id=sampleDataViewId, queries=[queryObj], indexDataType="datetime", groupRules=[
                            groupRuleObj], mappings=mappingObj, name=sampleDataViewName, description=sampleDataViewDescription)

        print
        print("Creating DataView")
        print(dataView.toJson())
        dataViews = ocsClient.DataViews.postDataView(namespaceId, dataView)

        print
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)

        # assert is added to make sure we get back what we are expecting
        expectedJSON = '{"Id": "DataView_Sample", "Queries": [{"Id": "DataView_Sample", "Query": {"Resource": "Streams", "Field": "Name", "Value": "SampleStream", "Function": "Contains"}}], "Name": "DataView_Sample_Name", "Description": "A Sample Description that describes that this DataView is just used for our sample.", "Mappings": {"IsDefault": true, "Columns": [{"Name": "time", "IsKey": true, "DataType": "DateTime", "MappingRule": {"PropertyPaths": ["time"]}}, {"Name": "DefaultGroupRule_Tags", "IsKey": false, "DataType": "string", "MappingRule": {"GroupRuleId": "DefaultGroupRule", "GroupRuleToken": "Tags"}}, {"Name": "pressure", "IsKey": false, "DataType": "Double", "MappingRule": {"PropertyPaths": ["pressure"]}}, {"Name": "temperature", "IsKey": false, "DataType": "Double", "MappingRule": {"PropertyPaths": ["temperature"]}}]}, "IndexDataType": "datetime", "GroupRules": [{"Id": "DefaultGroupRule", "Type": "StreamTag", "TokenRules": null}]}'
        assert dv.toJson() == expectedJSON, 'DataView is different: ' + dv.toJson()

        dv.Description = sampleDataViewDescription_modified
        dv.Mappings.IsDefault = False  # for now we have to change this to post the DataView

        print
        print("Updating DataView")
        dv = ocsClient.DataViews.putDataView(namespaceId, dv)

        expectedJSON = '{"Id": "DataView_Sample", "Queries": [{"Id": "DataView_Sample", "Query": {"Resource": "Streams", "Field": "Name", "Value": "SampleStream", "Function": "Contains"}}], "Name": "DataView_Sample_Name", "Description": "A longer sample description that describes that this DataView is just used for our sample and this part shows a put.", "Mappings": {"IsDefault": true, "Columns": [{"Name": "time", "IsKey": true, "DataType": "DateTime", "MappingRule": {"PropertyPaths": ["time"]}}, {"Name": "DefaultGroupRule_Tags", "IsKey": false, "DataType": "string", "MappingRule": {"GroupRuleId": "DefaultGroupRule", "GroupRuleToken": "Tags"}}, {"Name": "pressure", "IsKey": false, "DataType": "Double", "MappingRule": {"PropertyPaths": ["pressure"]}}, {"Name": "temperature", "IsKey": false, "DataType": "Double", "MappingRule": {"PropertyPaths": ["temperature"]}}]}, "IndexDataType": "datetime", "GroupRules": [{"Id": "DefaultGroupRule", "Type": "StreamTag", "TokenRules": null}]}'
        assert dv.toJson() == expectedJSON, 'DataView is different ' + dv.toJson()

        # Getting the complete set of DataViews to make sure it is there
        print
        print("Getting DataViews")
        dataViews = ocsClient.DataViews.getDataViews(namespaceId)
        for dataView1 in dataViews:
            if hasattr(dataView1, "Id"):
                print(dataView1.toJson())

        # Getting the DataGroups of the defined DataView.  The datgroup lets you see what is returned by the DataView Query.
        print
        print("Getting DataGroups")
        time.sleep(2)  # a sleep to make sure that things are set

        # This works normally, but fails during automated tests for some reason

        dataGroups = ocsClient.DataViews.getDataGroups(
            namespaceId, sampleDataViewId)
        for key, dataGroup in dataGroups['DataGroups'].items():
            print('DataGroup')
            print(dataGroup.toJson())

        # By default the preview get interpolated values every minute over the last hour, which lines up with our data that we sent in.
        # Beyond the normal API optoins, this function does have the option to return the data in a class if you have created a Type for the data you are retreiving.

        print
        print("Retrieving data preview from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataViewPreview(
            namespaceId, sampleDataViewId)
        print(str(dataViewDataPreview1[0]))

        # Now we can get the data creating a session.  The session allows us to get pages of data ensuring that the underlying data won't change as we collect the pages.
        # There are apis to manage the sessions, but that is beyond the scope of this basic example.
        # To highlight the use of the sessions this we will access the data, add a stream that would be added to result.
        # It won't show up because of the session, but we will see it in the preview that doesn't use the session.

        print
        print("Retrieving data from the DataView using session")
        dataViewDataSession1 = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId)
        print(str(dataViewDataSession1[0]))

        print("Intentional waiting for 5 seconds to show a noticeable change in time.")
        # We wait for 5 seconds so the preview is different that before, but our session data should be the same
        time.sleep(5)

        dataViewDataPreview2 = ocsClient.DataViews.getDataViewPreview(
            namespaceId, sampleDataViewId)
        print(str(dataViewDataPreview2[0]))

        dataViewDataSession2 = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId)
        print(str(dataViewDataSession2[0]))

        assert (dataViewDataSession2[0] == dataViewDataSession1[0]
                ), "Returned values from DataView Data Sessions is different"

        print()
        print("Getting data as a table, seperated by commas, with headers")
        # Viewing the whole returned result as a table
        dataViewDataSession3 = ocsClient.DataViews.getDataInterpolated(
            namespaceId, sampleDataViewId, form="csvh")

        # I only want to print out the headers and 2 rows, otherwise it monpolizes the printed screen.
        print(dataViewDataSession3[:193])

    except Exception as ex:
        print(("Encountered Error: {error}".format(error=ex)))
        print
        traceback.print_exc()
        print
        success = False
        exception = ex

    finally:
        ######################################################################################################
        # DataView deletion
        ######################################################################################################

        print
        print
        print("Deleting DataView")

        suppressError(lambda: ocsClient.DataViews.deleteDataView(
            namespaceId, sampleDataViewId))

        # check, including assert is added to make sure we deleted it
        dv = None
        try:
            dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        except Exception as ex:
            dv = None
        finally:
            assert dv is None, 'Delete failed'

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

# Straightforward test to make sure program is working using asserts in program.  Can run it yourself with pytest program.py


def test_main():
    main(True)
