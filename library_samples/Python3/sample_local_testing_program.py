
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

needData = False
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

        # Step 3
        
        dataView = DataView(id=sampleDataViewId)
        print
        print("Creating DataView")
        print(dataView.toJson())
        dataViews = ocsClient.DataViews.postDataView(namespaceId, dataView)

        # Step 4
        print
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())
        
        dv.Description = sampleDataViewDescription_modified
        query =  Query(id = "stream",value ="stream*")
        dv.Queries.append(query)

        print("Updated")
        print(dv.toJson())
        # Step 5
        print
        print("Updating DataView")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)
        
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

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
        print("Getting ResolvedDataItems")

        # Step 7
        # This works for the automated test.  You can use this or the below.
        dataItems = ocsClient.DataViews.getResolvedDataItems(
            namespaceId, sampleDataViewId, "stream")
        print(dataItems.toJson())
        
        print
        print("Getting ResolvedIneligibleDataItems")

        # Step 7
        dataItems = ocsClient.DataViews.getResolvedIneligibleDataItems(
            namespaceId, sampleDataViewId, "stream")
        print(dataItems.toJson())
        
        print
        print("Getting AvailableFieldSets")

        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, "stream")
        print(availablefields.toJson())
        fields = availablefields.Items

        dv.FieldSets = fields
        print("New DV")
        
        print(dv.toJson())
        
        print("Updating DataView")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)
        
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

        # Step 8
        print
        print("Retrieving data from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id = namespaceId, dataView_id = sampleDataViewId, startIndex = "2017-01-11T22:21:23.43Z",
            endIndex = "2017-01-11T22:28:29.43Z", interval = "01:00:00")
        print(str(dataViewDataPreview1))

        
        # Step 7
        section = Field(source = "Id", label="{DistinguisherValue} {FirstKey}")
        dv.Sectioners.append(section)
        print("New DV")
        
        print(dv.toJson())
        
        print("Updating DataView")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)
        
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

        print
        print("Retrieving data from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id = namespaceId, dataView_id = sampleDataViewId, startIndex = "2017-01-11T22:21:23.43Z",
            endIndex = "2017-01-11T22:28:29.43Z", interval = "01:00:00")
        print(str(dataViewDataPreview1))


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
