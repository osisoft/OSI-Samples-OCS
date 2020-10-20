"""This sample script demonstrates how to invoke the Sequential Data Store REST API"""

import configparser
import inspect
import math
import traceback

from ocs_sample_library_preview import (SdsType, SdsTypeCode, SdsTypeProperty,
                                        EDSClient, OCSClient, SdsStream, SdsBoundaryType,
                                        SdsStreamPropertyOverride,
                                        SdsStreamViewProperty, SdsStreamView,
                                        SdsStreamViewMap, SdsStreamIndex)

from wave_data import (WaveData, WaveDataCompound, WaveDataInteger,
                       WaveDataTarget)


def get_wave_data_type(sample_type_id):
    """Creates an SDS type definition for WaveData"""
    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    int_type = SdsType()
    int_type.Id = "intType"
    int_type.SdsTypeCode = SdsTypeCode.Int32

    double_type = SdsType()
    double_type.Id = "doubleType"
    double_type.SdsTypeCode = SdsTypeCode.Double

    # note that the Order is the key (primary index)
    order_property = SdsTypeProperty()
    order_property.Id = "Order"
    order_property.SdsType = int_type
    order_property.IsKey = True

    tau_property = SdsTypeProperty()
    tau_property.Id = "Tau"
    tau_property.SdsType = double_type

    radians_property = SdsTypeProperty()
    radians_property.Id = "Radians"
    radians_property.SdsType = double_type

    sin_property = SdsTypeProperty()
    sin_property.Id = "Sin"
    sin_property.SdsType = double_type

    cos_property = SdsTypeProperty()
    cos_property.Id = "Cos"
    cos_property.SdsType = double_type

    tan_property = SdsTypeProperty()
    tan_property.Id = "Tan"
    tan_property.SdsType = double_type

    sinh_property = SdsTypeProperty()
    sinh_property.Id = "Sinh"
    sinh_property.SdsType = double_type

    cosh_property = SdsTypeProperty()
    cosh_property.Id = "Cosh"
    cosh_property.SdsType = double_type

    tanh_property = SdsTypeProperty()
    tanh_property.Id = "Tanh"
    tanh_property.SdsType = double_type

    # create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sample_type_id
    wave.Name = "WaveDataSample"
    wave.Description = "This is a sample Sds type for storing WaveData type "\
                       "events."
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [order_property, tau_property, radians_property,
                       sin_property, cos_property, tan_property,
                       sinh_property, cosh_property, tanh_property]

    return wave


def get_wave_compound_data_type(sample_type_id):
    """Creates a compound SDS type definition for WaveData"""
    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    int_type = SdsType()
    int_type.Id = "intType"
    int_type.SdsTypeCode = SdsTypeCode.Int32

    double_type = SdsType()
    double_type.Id = "doubleType"
    double_type.SdsTypeCode = SdsTypeCode.Double

    # note that the Order is the key (primary index)
    order_property = SdsTypeProperty()
    order_property.Id = "Order"
    order_property.SdsType = int_type
    order_property.IsKey = True
    order_property.Order = 1

    multiplier_property = SdsTypeProperty()
    multiplier_property.Id = "Multiplier"
    multiplier_property.SdsType = int_type
    multiplier_property.IsKey = True
    multiplier_property.Order = 2

    tau_property = SdsTypeProperty()
    tau_property.Id = "Tau"
    tau_property.SdsType = double_type

    radians_property = SdsTypeProperty()
    radians_property.Id = "Radians"
    radians_property.SdsType = double_type

    sin_property = SdsTypeProperty()
    sin_property.Id = "Sin"
    sin_property.SdsType = double_type

    cos_property = SdsTypeProperty()
    cos_property.Id = "Cos"
    cos_property.SdsType = double_type

    tan_property = SdsTypeProperty()
    tan_property.Id = "Tan"
    tan_property.SdsType = double_type

    sinh_property = SdsTypeProperty()
    sinh_property.Id = "Sinh"
    sinh_property.SdsType = double_type

    cosh_property = SdsTypeProperty()
    cosh_property.Id = "Cosh"
    cosh_property.SdsType = double_type

    tanh_property = SdsTypeProperty()
    tanh_property.Id = "Tanh"
    tanh_property.SdsType = double_type

    # create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = sample_type_id
    wave.Name = "WaveDataTypeCompound"
    wave.Description = "This is a sample Sds type for storing WaveData type "\
                       "events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [order_property, multiplier_property, tau_property,
                       radians_property, sin_property, cos_property, tan_property,
                       sinh_property, cosh_property, tanh_property]

    return wave


def get_wave_data_target_type(sample_type_id):
    """Creates an SDS type definition for WaveDataTarget"""
    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    int_type = SdsType()
    int_type.Id = "intType"
    int_type.SdsTypeCode = SdsTypeCode.Int32

    double_type = SdsType()
    double_type.Id = "doubleType"
    double_type.SdsTypeCode = SdsTypeCode.Double

    # note that the Order is the key (primary index)
    order_target_property = SdsTypeProperty()
    order_target_property.Id = "OrderTarget"
    order_target_property.SdsType = int_type
    order_target_property.IsKey = True

    tau_target_property = SdsTypeProperty()
    tau_target_property.Id = "TauTarget"
    tau_target_property.SdsType = double_type

    radians_target_property = SdsTypeProperty()
    radians_target_property.Id = "RadiansTarget"
    radians_target_property.SdsType = double_type

    sin_target_property = SdsTypeProperty()
    sin_target_property.Id = "SinTarget"
    sin_target_property.SdsType = double_type

    cos_target_property = SdsTypeProperty()
    cos_target_property.Id = "CosTarget"
    cos_target_property.SdsType = double_type

    tan_target_property = SdsTypeProperty()
    tan_target_property.Id = "TanTarget"
    tan_target_property.SdsType = double_type

    sinh_target_property = SdsTypeProperty()
    sinh_target_property.Id = "SinhTarget"
    sinh_target_property.SdsType = double_type

    cosh_target_property = SdsTypeProperty()
    cosh_target_property.Id = "CoshTarget"
    cosh_target_property.SdsType = double_type

    tanh_target_property = SdsTypeProperty()
    tanh_target_property.Id = "TanhTarget"
    tanh_target_property.SdsType = double_type

    # create an SdsType for WaveData Class
    wave = SdsType()
    wave.Id = SAMPLE_TARGET_TYPE_ID
    wave.Name = "WaveDataTargetSample"
    wave.Description = "This is a sample Sds type for storing WaveDataTarget"\
                       " type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [order_target_property, tau_target_property,
                       radians_target_property, sin_target_property,
                       cos_target_property, tan_target_property,
                       sinh_target_property, cosh_target_property,
                       tanh_target_property]

    return wave


def get_wave_data_integer_type(sample_type_id):
    """Creates an SDS type definition for WaveDataInteger"""
    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError("sampleTypeId is not an instantiated string")

    int_type = SdsType()
    int_type.Id = "intType"
    int_type.SdsTypeCode = SdsTypeCode.Int32

    # note that the Order is the key (primary index)
    order_target_property = SdsTypeProperty()
    order_target_property.Id = "OrderTarget"
    order_target_property.SdsType = int_type
    order_target_property.IsKey = True

    sin_int_property = SdsTypeProperty()
    sin_int_property.Id = "SinInt"
    sin_int_property.SdsType = int_type

    cos_int_property = SdsTypeProperty()
    cos_int_property.Id = "CosInt"
    cos_int_property.SdsType = int_type

    tan_int_property = SdsTypeProperty()
    tan_int_property.Id = "TanInt"
    tan_int_property.SdsType = int_type

    # create an SdsType for the WaveDataInteger Class
    wave = SdsType()
    wave.Id = SAMPLE_INTEGER_TYPE_ID
    wave.Name = "WaveDataIntegerSample"
    wave.Description = "This is a sample Sds type for storing WaveDataInteger"\
                       "type events"
    wave.SdsTypeCode = SdsTypeCode.Object
    wave.Properties = [order_target_property, sin_int_property,
                       cos_int_property, tan_int_property]

    return wave


def next_wave(order, multiplier):
    """Creates a new WaveData event"""
    radians = (order) * math.pi/32

    new_wave = WaveDataCompound()
    new_wave.order = order
    new_wave.multiplier = multiplier
    new_wave.radians = radians
    new_wave.tau = radians / (2 * math.pi)
    new_wave.sin = multiplier * math.sin(radians)
    new_wave.cos = multiplier * math.cos(radians)
    new_wave.tan = multiplier * math.tan(radians)
    new_wave.sinh = multiplier * math.sinh(radians)
    new_wave.cosh = multiplier * math.cosh(radians)
    new_wave.tanh = multiplier * math.tanh(radians)

    return new_wave


def suppress_error(sds_call):
    """Suppress an error thrown by SDS"""
    try:
        sds_call()
    except Exception as error:
        print(f"Encountered Error: {error}")


def is_prop(value):
    """Check whether a field is a property of an object"""
    return isinstance(value, property)


def to_string(event):
    """Converts an event into a string"""
    string = ""
    props = inspect.getmembers(type(event), is_prop)
    print_order = [2, 3, 4, 0, 6, 5, 1, 7, 8]
    ordered_props = [props[i] for i in print_order]
    for prop in ordered_props:
        value = prop[1].fget(event)
        if value is None:
            string += "{name}: , ".format(name=prop[0])
        else:
            string += "{name}: {value}, ".format(name=prop[0], value=value)
    return string[:-2]


def to_wave_data(json_obj):
    """"Converts JSON object into WaveData type"""
    # Many JSON implementations leave default values out.  We compensate for
    # WaveData, knowing  that all values should be filled in
    wave = WaveData()
    properties = inspect.getmembers(type(wave), is_prop)
    for prop in properties:
        # Pre-Assign the default
        prop[1].fset(wave, 0)

        if prop[0] in json_obj:
            value = json_obj[prop[0]]
            if value is not None:
                prop[1].fset(wave, value)
    return wave


# Sample Data Information
SAMPLE_TYPE_ID = "WaveData_SampleType"
SAMPLE_TARGET_TYPE_ID = "WaveDataTarget_SampleType"
SAMPLE_INTEGER_TYPE_ID = "WaveData_IntegerType"
SAMPLE_STREAM_ID = "WaveData_SampleStream"
SAMPLE_STREAM_VIEW_ID = "WaveData_SampleStreamView"
SAMPLE_STREAM_VIEW_INT_ID = "WaveData_SampleIntStreamView"
STREAM_ID_SECONDARY = "SampleStream_Secondary"
STREAM_ID_COMPOUND = "SampleStream_Compound"
COMPOUND_TYPE_ID = "SampleType_Compound"


def main(test=False):
    """This function is the main body of the SDS sample script"""
    exception = None
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Step 1
        tenant_id = config.get('Access', 'Tenant')
        namespace_id = config.get('Configurations', 'Namespace')

        if tenant_id == 'default':
            sds_client = EDSClient(
                config.get('Access', 'ApiVersion'),
                config.get('Access', 'Resource'))
        else:
            sds_client = OCSClient(
                config.get('Access', 'ApiVersion'),
                config.get('Access', 'Tenant'),
                config.get('Access', 'Resource'),
                config.get('Credentials', 'ClientId'),
                config.get('Credentials', 'ClientSecret'))

        namespace_id = config.get('Configurations', 'Namespace')

        print(r"------------------------------------------")
        print(r"  _________    .___     __________        ")
        print(r" /   _____/  __| _/_____\______   \___.__.")
        print(r" \_____  \  / __ |/  ___/|     ___<   |  |")
        print(r" /        \/ /_/ |\___ \ |    |    \___  |")
        print(r"/_______  /\____ /____  >|____|    / ____|")
        print(r"        \/      \/    \/           \/     ")
        print(r"------------------------------------------")
        print("Sds endpoint at {url}".format(url=sds_client.uri))
        print()

        # Step 2
        #######################################################################
        # SdsType get or creation
        #######################################################################
        print("Creating an SdsType")
        wave_type = get_wave_data_type(SAMPLE_TYPE_ID)
        wave_type = sds_client.Types.getOrCreateType(namespace_id, wave_type)
        assert wave_type.Id == SAMPLE_TYPE_ID, "Error getting back wave Type"

        # Step 3
        #######################################################################
        # Sds Stream creation
        #######################################################################
        print("Creating an SdsStream")
        stream = SdsStream()
        stream.Id = SAMPLE_STREAM_ID
        stream.Name = "WaveStreamPySample"
        stream.Description = "A Stream to store the WaveData events"
        stream.TypeId = wave_type.Id
        sds_client.Streams.createOrUpdateStream(namespace_id, stream)

        # Step 4
        #######################################################################
        # CRUD operations for events
        #######################################################################

        print("Inserting data")
        # Insert a single event
        event = next_wave(0, 2.0)
        sds_client.Streams.insertValues(namespace_id, stream.Id, [event])

        # Insert a list of events
        waves = []
        for error in range(2, 20, 2):
            waves.append(next_wave(error, 2.0))
        sds_client.Streams.insertValues(namespace_id, stream.Id, waves)

        # Step 5
        # Get the last inserted event in a stream
        print("Getting latest event")
        wave = sds_client.Streams.getLastValue(
            namespace_id, stream.Id, WaveData)
        print(to_string(wave))
        print()

        # Get all the events
        waves = sds_client.Streams.getWindowValues(
            namespace_id, stream.Id, WaveData, 0, 180)
        print("Getting all events")
        print("Total events found: " + str(len(waves)))
        for wave in waves:
            print(to_string(wave))
        print()

        # Step 6
        # get all values with headers
        waves = sds_client.Streams.getWindowValuesForm(
            namespace_id, stream.Id, None, 0, 180, "tableh")
        print("Getting all events in table format")
        print(waves)

        # Step 7
        print("Updating events")
        # Update the first event
        event = next_wave(0, 4.0)
        sds_client.Streams.updateValues(namespace_id, stream.Id, [event])

        # Update the rest of the events, adding events that have no prior
        # index entry
        updated_events = []
        for error in range(2, 40, 2):
            event = next_wave(error, 4.0)
            updated_events.append(event)
        sds_client.Streams.updateValues(
            namespace_id, stream.Id, updated_events)

        # Get all the events
        waves = sds_client.Streams.getWindowValues(namespace_id, stream.Id,
                                                   WaveData, 0, 40)
        print("Getting updated events")
        print("Total events found: " + str(len(waves)))
        for wave in waves:
            print(to_string(wave))
        print()

        # Step 8
        print("Replacing events")
        # replace one value
        event = next_wave(0, 5.0)
        sds_client.Streams.replaceValues(namespace_id, stream.Id, [event])

        # replace multiple values
        replaced_events = []
        for error in range(2, 40, 2):
            event = next_wave(error, 5.0)
            replaced_events.append(event)
        sds_client.Streams.replaceValues(
            namespace_id, stream.Id, replaced_events)

        # Step 9
        # Get all the events
        waves = sds_client.Streams.getWindowValues(namespace_id, stream.Id,
                                                   WaveData, 0, 180)
        print("Getting replaced events")
        print("Total events found: " + str(len(waves)))
        for wave in waves:
            print(to_string(wave))
        print()

        retrieved_interpolated = sds_client.Streams.getRangeValuesInterpolated(
            namespace_id, stream.Id, None, "5", "32", 4)
        print("Sds can interpolate or extrapolate data at an index location "
              "where data does not explicitly exist:")
        print(retrieved_interpolated)
        print()

        # Step 10
        # Filtering from all values
        print("Getting filtered events")
        filtered_events = sds_client.Streams.getWindowValues(
            namespace_id, SAMPLE_STREAM_ID, WaveData, 0, 50, 'Radians lt 3')

        print("Total events found: " + str(len(filtered_events)))
        for wave in filtered_events:
            print(to_string(wave))
        print()

        # Step 11
        # Sampling from all values
        print("Getting sampled values")
        sampled_waves = sds_client.Streams.getSampledValues(
            namespace_id, stream.Id, WaveData, 0, 40, "sin", 4)

        print("Total events found: " + str(len(sampled_waves)))
        for wave in sampled_waves:
            print(to_string(wave))
        print()

        # Step 12
        #######################################################################
        # Property Overrides
        #######################################################################

        print("Property Overrides")
        print("Sds can interpolate or extrapolate data at an index location "
              "where data does not explicitly exist:")
        print()

        # We will retrieve three events using the default behavior, Continuous
        waves = sds_client.Streams.getRangeValues(
            namespace_id, stream.Id, WaveData, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated)

        print("Default (Continuous) requesting data starting at index location"
              " '1', where we have not entered data, Sds will interpolate a "
              "value for each property:")

        for wave in waves:
            print(("Order: {order}: Radians: {radians} Cos: {cos}".format(
                order=wave.order, radians=wave.radians, cos=wave.cos)))

        # Create a Discrete stream PropertyOverride indicating that we do not
        #  want Sds to calculate a value for Radians and update our stream
        property_override = SdsStreamPropertyOverride()
        property_override.SdsTypePropertyId = 'Radians'
        property_override.InterpolationMode = 3

        # update the stream
        props = [property_override]
        stream.PropertyOverrides = props
        sds_client.Streams.createOrUpdateStream(namespace_id, stream)

        waves = sds_client.Streams.getRangeValues(
            namespace_id, stream.Id, WaveData, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated)
        print()
        print("We can override this read behavior on a property by property"
              "basis, here we override the Radians property instructing Sds"
              " not to interpolate.")
        print("Sds will now return the default value for the data type:")
        for wave in waves:
            print(("Order: {order}: Radians: {radians} Cos: {cos}".format(
                order=wave.order, radians=wave.radians, cos=wave.cos)))

        # Step 13
        #######################################################################
        # Stream Views
        #######################################################################

        # Create additional types to define our targets
        wave_target_type = get_wave_data_target_type(SAMPLE_TARGET_TYPE_ID)
        wave_target_type = sds_client.Types.getOrCreateType(namespace_id,
                                                            wave_target_type)

        wave_integer_type = get_wave_data_integer_type(SAMPLE_INTEGER_TYPE_ID)
        wave_integer_type = sds_client.Types.getOrCreateType(namespace_id,
                                                             wave_integer_type)

        # Create an SdsStreamViewProperty objects when we want to explicitly
        # map one property to another
        vp1 = SdsStreamViewProperty()
        vp1.SourceId = "Order"
        vp1.TargetId = "OrderTarget"

        vp2 = SdsStreamViewProperty()
        vp2.SourceId = "Sin"
        vp2.TargetId = "SinInt"

        vp3 = SdsStreamViewProperty()
        vp3.SourceId = "Cos"
        vp3.TargetId = "CosInt"

        vp4 = SdsStreamViewProperty()
        vp4.SourceId = "Tan"
        vp4.TargetId = "TanInt"

        # Create a streamView mapping our original type to our target type,
        # data shape is the same so let Sds handle the mapping
        stream_view = SdsStreamView()
        stream_view.Id = SAMPLE_STREAM_VIEW_ID
        stream_view.Name = "SampleStreamView"
        stream_view.TargetTypeId = wave_target_type.Id
        stream_view.SourceTypeId = wave_type.Id

        # Data shape and data types are different so include explicit mappings
        # between properties
        manual_stream_view = SdsStreamView()
        manual_stream_view.Id = SAMPLE_STREAM_VIEW_INT_ID
        manual_stream_view.Name = "SampleIntStreamView"
        manual_stream_view.TargetTypeId = wave_integer_type.Id
        manual_stream_view.SourceTypeId = wave_type.Id
        manual_stream_view.Properties = [vp1, vp2, vp3, vp4]

        automatic_stream_view = sds_client.Streams.getOrCreateStreamView(
            namespace_id, stream_view)
        manual_stream_view = sds_client.Streams.getOrCreateStreamView(
            namespace_id, manual_stream_view)

        stream_view_map_1 = SdsStreamViewMap()
        stream_view_map_1 = sds_client.Streams.getStreamViewMap(
            namespace_id, automatic_stream_view.Id)

        stream_view_map_2 = SdsStreamViewMap()
        stream_view_map_2 = sds_client.Streams.getStreamViewMap(
            namespace_id, manual_stream_view.Id)

        range_waves = sds_client.Streams.getRangeValues(
            namespace_id, stream.Id, WaveData, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated)
        print()
        print("SdsStreamViews")
        print("Here is some of our data as it is stored on the server:")
        for way in range_waves:
            print(("Sin: {sin}, Cos: {cos}, Tan: {tan}".format(
                sin=way.sin, cos=way.cos, tan=way.tan)))

        # StreamView data when retrieved with a streamView
        range_waves = sds_client.Streams.getRangeValues(
            namespace_id, stream.Id, WaveDataTarget, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated, automatic_stream_view.Id)
        print()
        print("Specifying a streamView with an SdsType of the same shape"
              "returns values that are automatically mapped to the target"
              " SdsType's properties:")
        for way in range_waves:
            print(("SinTarget: {sinTarget}, CosTarget: {cosTarget}, TanTarget:"
                   " {tanTarget}").format(sinTarget=way.sin_target,
                                          cosTarget=way.cos_target,
                                          tanTarget=way.tan_target))

        range_waves = sds_client.Streams.getRangeValues(
            namespace_id, stream.Id, WaveDataInteger, "1", 0, 3, False,
            SdsBoundaryType.ExactOrCalculated, manual_stream_view.Id)
        print()
        print("SdsStreamViews can also convert certain types of data, here we"
              " return integers where the original values were doubles:")
        for way in range_waves:
            print(("SinInt: {sinInt}, CosInt: {cosInt}, TanInt: {tanInt}")
                  .format(sinInt=way.sin_int, cosInt=way.cos_int,
                          tanInt=way.tan_int))

        print()
        print("We can query Sds to return the SdsStreamViewMap for our "
              "SdsStreamView, here is the one generated automatically:")
        for prop in stream_view_map_1.Properties:
            print(("{source} => {dest}".format(
                source=prop.SourceId, dest=prop.TargetId)))

        print()
        print("Here is our explicit mapping, note SdsStreamViewMap will return"
              " all properties of the Source Type, even those without a "
              "corresponding Target property:")
        for prop in stream_view_map_2.Properties:
            if hasattr(prop, 'TargetId'):
                print(("{source} => {dest}".format(source=prop.SourceId,
                                                   dest=prop.TargetId)))
            else:
                print(("{source} => {dest}".format(source=prop.SourceId,
                                                   dest='Not mapped')))

        # Step 14
        print("We will now update the stream type based on the streamview")

        first_val = sds_client.Streams.getFirstValue(namespace_id, stream.Id,
                                                     None)
        sds_client.Streams.updateStreamType(namespace_id, stream.Id,
                                            SAMPLE_STREAM_VIEW_ID)

        new_stream = sds_client.Streams.getStream(
            namespace_id, SAMPLE_STREAM_ID)
        first_val_updated = sds_client.Streams.getFirstValue(namespace_id,
                                                             SAMPLE_STREAM_ID, None)

        print("The new type id" + new_stream.TypeId + " compared to the "
              "original one " + stream.TypeId)
        print("The new type value " + str(first_val) + " compared to the "
              "original one " + str(first_val_updated))

        # Step 15
        types = sds_client.Types.getTypes(namespace_id, 0, 100)
        types_query = sds_client.Types.getTypes(
            namespace_id, 0, 100, "Id:*Target*")

        print()
        print("All Types: ")
        for type_i in types:
            print(type_i.Id)

        print("Types after Query: ")
        for type_i in types_query:
            print(type_i.Id)

        if tenant_id != 'default':
            # Step 16
            #######################################################################
            # Tags and Metadata (OCS ONLY)
            #######################################################################
            print()
            print("Let's add some Tags and Metadata to our stream:")

            tags = ["waves", "periodic", "2018", "validated"]
            metadata = {"Region": "North America", "Country": "Canada",
                        "Province": "Quebec"}

            sds_client.Streams.createOrUpdateTags(
                namespace_id, stream.Id, tags)
            sds_client.Streams.createOrUpdateMetadata(namespace_id, stream.Id,
                                                      metadata)

            print()
            print("Tags now associated with ", stream.Id)
            print(sds_client.Streams.getTags(namespace_id, stream.Id))

            region = sds_client.Streams.getMetadata(
                namespace_id, stream.Id, "Region")
            country = sds_client.Streams.getMetadata(
                namespace_id, stream.Id, "Country")
            province = sds_client.Streams.getMetadata(
                namespace_id, stream.Id, "Province")

            print()
            print("Metadata now associated with", stream.Id, ":")
            print("Metadata key Region: ", region)
            print("Metadata key Country: ", country)
            print("Metadata key Province: ", province)
            print()

            # Step 17
            #######################################################################
            # Update Metadata (OCS ONLY)
            #######################################################################
            print()
            print("Let's update the Metadata on our stream:")

            patch = [
                {"op": "remove", "path": "/Region"},
                {"op": "replace", "path": "/Province", "value": "Ontario"},
                {"op": "add", "path": "/City", "value": "Toronto"}
            ]

            sds_client.Streams.patchMetadata(namespace_id, stream.Id,
                                             patch)

            country = sds_client.Streams.getMetadata(
                namespace_id, stream.Id, "Country")
            province = sds_client.Streams.getMetadata(
                namespace_id, stream.Id, "Province")
            city = sds_client.Streams.getMetadata(
                namespace_id, stream.Id, "City")

            print()
            print("Metadata now associated with", stream.Id, ":")
            print("Metadata key Country: ", country)
            print("Metadata key Province: ", province)
            print("Metadata key City: ", city)
            print()

        # Step 17
        #######################################################################
        # Delete events
        #######################################################################
        print()
        print('Deleting values from the SdsStream')
        # remove a single value from the stream
        sds_client.Streams.removeValue(namespace_id, stream.Id, 0)

        # remove multiple values from the stream
        sds_client.Streams.removeWindowValues(namespace_id, stream.Id, 0, 40)
        try:
            event = sds_client.Streams.getLastValue(namespace_id, stream.Id,
                                                    WaveData)
            if event is not None:
                raise ValueError
        except TypeError:
            pass
        print("All values deleted successfully!")

        # Step 18
        print("Adding a stream with a secondary index.")
        index = SdsStreamIndex()
        index.SdsTypePropertyId = "Radians"

        secondary = SdsStream()
        secondary.Id = STREAM_ID_SECONDARY
        secondary.TypeId = SAMPLE_TYPE_ID
        secondary.Indexes = [index]

        secondary = sds_client.Streams.getOrCreateStream(
            namespace_id, secondary)
        count = 0
        if stream.Indexes:
            count = len(stream.Indexes)

        print("Secondary indexes on streams original:" + str(count) +
              ". New one:  " + str(len(secondary.Indexes)))
        print()

        # Modifying an existing stream with a secondary index.
        print("Modifying a stream to have a secondary index.")

        sample_stream = sds_client.Streams.getStream(
            namespace_id, SAMPLE_STREAM_ID)

        index = SdsStreamIndex()
        index.SdsTypePropertyId = "RadiansTarget"
        sample_stream.Indexws = [index]
        sds_client.Streams.createOrUpdateStream(namespace_id, sample_stream)

        sample_stream = sds_client.Streams.getStream(
            namespace_id, SAMPLE_STREAM_ID)
        # Modifying an existing stream to remove the secondary index
        print("Removing a secondary index from a stream.")

        secondary.Indexes = []

        sds_client.Streams.createOrUpdateStream(namespace_id, secondary)

        secondary = sds_client.Streams.getStream(namespace_id, secondary.Id)

        original_length = "0"
        if stream.Indexes:
            original_length = str(len(stream.Indexes))

        secondary_length = "0"
        if secondary.Indexes:
            secondary_length = str(len(secondary.Indexes))

        print("Secondary indexes on streams original:" + original_length +
              ". New one:  " + secondary_length)

        # Step 19
        # Adding Compound Index Type
        print("Creating an SdsType with a compound index")
        type_compound = get_wave_compound_data_type(COMPOUND_TYPE_ID)
        sds_client.Types.getOrCreateType(namespace_id, type_compound)

        # create an SdsStream
        print("Creating an SdsStream off of type with compound index")
        stream_compound = SdsStream()
        stream_compound.Id = STREAM_ID_COMPOUND
        stream_compound.TypeId = type_compound.Id
        sds_client.Streams.createOrUpdateStream(namespace_id, stream_compound)

        # Step 20
        print("Inserting data")
        waves = []
        waves.append(next_wave(1, 10))
        waves.append(next_wave(2, 2))
        waves.append(next_wave(3, 1))
        waves.append(next_wave(10, 3))
        waves.append(next_wave(10, 8))
        waves.append(next_wave(10, 10))
        sds_client.Streams.insertValues(
            namespace_id, STREAM_ID_COMPOUND, waves)

        latest_compound = sds_client.Streams.getLastValue(
            namespace_id, STREAM_ID_COMPOUND, None)
        first_compound = sds_client.Streams.getFirstValue(
            namespace_id, STREAM_ID_COMPOUND, None)

        window_val = sds_client.Streams.getWindowValues(
            namespace_id, STREAM_ID_COMPOUND, None, "2|1", "10|8")

        print("First data: " + str(first_compound) +
              " Latest data: " + str(latest_compound))
        print("Window Data:")
        print(str(window_val))

    except Exception as error:
        print((f'Encountered Error: {error}'))
        print()
        traceback.print_exc()
        print()
        exception = error

    finally:
        # Step 21

        #######################################################################
        # SdsType, SdsStream, and SdsStreamView deletion
        #######################################################################
        # Clean up the remaining artifacts
        print("Cleaning up")
        print("Deleting the stream")
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, SAMPLE_STREAM_ID))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_ID_SECONDARY))
        suppress_error(lambda: sds_client.Streams.deleteStream(
            namespace_id, STREAM_ID_COMPOUND))

        print("Deleting the streamViews")
        suppress_error(lambda: sds_client.Streams.deleteStreamView(
            namespace_id, SAMPLE_STREAM_VIEW_ID))
        suppress_error(lambda: sds_client.Streams.deleteStreamView(
            namespace_id, SAMPLE_STREAM_VIEW_INT_ID))

        print("Deleting the types")
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, SAMPLE_TYPE_ID))
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, SAMPLE_TARGET_TYPE_ID))
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, SAMPLE_INTEGER_TYPE_ID))
        suppress_error(lambda: sds_client.Types.deleteType(
            namespace_id, COMPOUND_TYPE_ID))

        if test and exception is not None:
            raise exception
    print('Complete!')


if __name__ == '__main__':
    main()
