
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
samplePressureTypeId2 = "Time_Pressure_SampleType_old"
samplePressureStreamId = "dvTank2"
samplePressureStreamName = "Tank2"
samplePressureStreamId2 = "dvTank100"
samplePressureStreamName2 = "Tank100"

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
endTime = None
interval = "00:20:00"
queryID = "stream"
fieldSourceForSectioner = FieldSource.Id
queryString = "dvTank*"
fieldToConsildateTo = "temperature"
fieldToConsildate = "ambient_temp"


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
    temperatureDoubleProperty = SdsTypeProperty(id=fieldToConsildateTo,
                                                sdsType=doubleType)
    ambient_temperatureDoubleProperty = SdsTypeProperty(id=fieldToConsildate,
                                                sdsType=doubleType)
    timeDateTimeProperty = SdsTypeProperty(id="time", sdsType=dateTimeType,
                                           isKey=True)

    pressure_SDSType = SdsType(
        id=samplePressureTypeId,
        description="This is a sample Sds type for storing Pressure type "
                    "events for DataViews",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty,temperatureDoubleProperty, timeDateTimeProperty])
        

    pressure_SDSType2 = SdsType(
        id=samplePressureTypeId2,
        description="This is a new sample Sds type for storing Pressure type "
                    "events for DataViews",
        sdsTypeCode=SdsTypeCode.Object,
        properties=[pressureDoubleProperty,ambient_temperatureDoubleProperty, timeDateTimeProperty])

    print('Creating SDS Type')
    ocsClient.Types.getOrCreateType(namespaceId, pressure_SDSType)
    ocsClient.Types.getOrCreateType(namespaceId, pressure_SDSType2)

    pressureStream = SdsStream(
        id=samplePressureStreamId,
        name=samplePressureStreamName,
        description="A Stream to store the sample Pressure events",
        typeId=samplePressureTypeId)
        

    pressureStream2 = SdsStream(
        id=samplePressureStreamId2,
        name=samplePressureStreamName2,
        description="A Stream to store the sample Pressure events",
        typeId=samplePressureTypeId2)

    print('Creating SDS Streams')
    ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream)
    ocsClient.Streams.createOrUpdateStream(namespaceId, pressureStream2)

    start = datetime.datetime.now() - datetime.timedelta(hours=1)
    endTime = datetime.datetime.now()

    pressureValues = []
    pressureValues2 = []

    def valueWithTime(timestamp, value, fieldName, value2):
        return f'{{"time": "{timestamp}", "pressure": {str(value)}, "{fieldName}": {str(value2)}}}'

    print('Generating Values')
    for i in range(1, 30, 1):
        pv = str(random.uniform(0, 100))
        tv = str(random.uniform(50, 70))
        timestamp = (start + datetime.timedelta(minutes=i * 2)
                     ).isoformat(timespec='seconds')
        pVal = valueWithTime(timestamp, random.uniform(0, 100),fieldToConsildateTo, random.uniform(50, 70))
        pVal2 = valueWithTime(timestamp, random.uniform(0, 100),fieldToConsildate, random.uniform(50, 70))

        pressureValues.append(pVal)
        pressureValues2.append(pVal2)

    print('Sending Values')
    ocsClient.Streams.insertValues(
        namespaceId,
        samplePressureStreamId,
        str(pressureValues).replace("'", ""))
    ocsClient.Streams.insertValues(
        namespaceId,
        samplePressureStreamId2,
        str(pressureValues2).replace("'", ""))
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
        print("Creating DataView")
        dataViews = ocsClient.DataViews.postDataView(namespaceId, dataView)

        # Step 2
        print
        print("Getting DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())

        
        # Step 3
        print
        print("Updating DataView")

        dv.Description = sampleDataViewDescription_modified
        query =  Query(id = queryID,value =queryString)
        dv.Queries.append(query)
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)
        
        print("Getting updated DataView")
        dv = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId)
        print(dv.toJson())
        
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
        
        #Step 5
        print
        print("Getting AvailableFieldSets")

        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, queryID)
        print(availablefields.toJson())

        #Step 6
        fields = availablefields.Items

        dv.FieldSets = fields
        
        print("Updating DataView")
        ocsClient.DataViews.putDataView(namespaceId, dv)
        
        print("Now AvailableFieldSets")
        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, queryID)
        print(availablefields.toJson())

        print
        print("Retrieving data from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id = namespaceId, dataView_id = sampleDataViewId, startIndex = startTime,
            endIndex = endTime, interval = interval)
        print(str(dataViewDataPreview1))

        
        # Step 7
        section = Field(source = fieldSourceForSectioner, label="{DistinguisherValue} {FirstKey}")
        dv.Sectioners.append(section)
        
        print("Updating DataView with sectioner")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print
        print("Retrieving data from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id = namespaceId, dataView_id = sampleDataViewId, startIndex = startTime,
            endIndex = endTime, interval = interval)
        print(str(dataViewDataPreview1))

        # Step 8
        
        print
        print("Now AvailableFieldSets")
        availablefields = ocsClient.DataViews.getResolvedAvailableFieldSets(
            namespaceId, sampleDataViewId, queryID)
        print(availablefields.toJson())

        dvDataItemFieldSet = find_FieldSet(dv.FieldSets, FieldSetSourceType.DataItem)
        field = find_Field(dvDataItemFieldSet.Fields,fieldSourceForSectioner)
        dvDataItemFieldSet.Fields.remove(field)
        ocsClient.DataViews.putDataView(namespaceId, dv)


        # Step 9
        print("Setting up distinquisher")

        field = find_FieldSet(dv.FieldSets, FieldSetSourceType.DataItem)
        field.Distinguisher = dv.Sectioners[0]
        dv.Sectioners = []
        
        print("Updating DataView with distinquisher")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)

        print
        print("Retrieving data from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id = namespaceId, dataView_id = sampleDataViewId, startIndex = startTime,
            endIndex = endTime, interval = interval)
        print(str(dataViewDataPreview1))

        # Step 10
        print
        print("Consolidating data")

        field1 = find_Field_Key(dvDataItemFieldSet.Fields,FieldSource.PropertyId, fieldToConsildateTo)
        field2 = find_Field_Key(dvDataItemFieldSet.Fields,FieldSource.PropertyId, fieldToConsildate)
        print(field1.toJson())
        print(field2.toJson())
        field1.Keys.append(fieldToConsildate)
        dvDataItemFieldSet.Fields.remove(field2)

        print("Updating DataView with consildation")
        # No DataView returned, success is 204
        ocsClient.DataViews.putDataView(namespaceId, dv)
        
        print
        print("Retrieving data from the DataView")
        dataViewDataPreview1 = ocsClient.DataViews.getDataInterpolated(
            namespace_id = namespaceId, dataView_id = sampleDataViewId, startIndex = startTime,
            endIndex = endTime, interval = interval)
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

        # Step 11
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
                namespaceId, samplePressureStreamId2))

            print("Deleting added Types")
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, samplePressureTypeId))
            suppressError(lambda: ocsClient.Types.deleteType(
                namespaceId, samplePressureTypeId2))
        if test and not success:
            raise exception


main()
print("done")

# Straightforward test to make sure program is working using asserts in
# program.  Can run it yourself with pytest program.py


def test_main():
    main(True)
