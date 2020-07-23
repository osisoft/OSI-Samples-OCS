package com.github.osisoft.dataviewsample;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Properties;
import java.time.*;

import com.github.osisoft.ocs_sample_library_preview.*;
import com.github.osisoft.ocs_sample_library_preview.sds.*;
import com.github.osisoft.ocs_sample_library_preview.dataviews.*;

public class App {
    // Get Configuration
    static String tenantId = getConfiguration("tenantId");
    static String namespaceId = getConfiguration("namespaceId");
    static String ocsServerUrl = getConfiguration("ocsServerUrl");

    // Sample Data Information
    static String sampleTypeId1 = "Time_SampleType1";
    static String sampleTypeId2 = "Time_SampleType2";
    static String sampleStreamId1 = "dvTank2";
    static String sampleStreamName1 = "Tank2";
    static String sampleStreamId2 = "dvTank100";
    static String sampleStreamName2 = "Tank100";
    static String sampleFieldToConsolidateTo = "temperature";
    static String sampleFieldToConsolidate = "ambient_temp";
    static Instant sampleStartTime = null;
    static Instant sampleEndTime = null;

    // Data View Information
    static String sampleDataViewId = "DataView_Sample";
    static String sampleDataViewName = "DataView_Sample_Name";
    static String sampleDataViewDescription = "A Sample Description that describes that this DataView is just used for our sample.";
    static String sampleQueryId = "stream";
    static String sampleQueryString = "dvTank*";
    static String sampleInterval = "00:20:00";

    static boolean needData = true;

    private static FieldSet findFieldSet(FieldSet[] fieldSets, String queryId) {
        for (FieldSet fieldSet : fieldSets) {
            if (fieldSet.getQueryId().equals(queryId)) {
                return fieldSet;
            }
        }
        return null;
    }

    private static Field findField(Field[] fields, FieldSource fieldSource, String fieldId) {
        for (Field field : fields) {
            if (field.getSource() == fieldSource) {
                for (String key : field.getKeys()) {
                    if (key.equals(fieldId)) {
                        return field;
                    }
                }
            }
        }
        return null;
    }

    public static void main(String[] args) throws InterruptedException {
        toRun();
        System.out.println("Complete!");
    }

    public static Boolean toRun() {
        Boolean success = true;

        System.out.println("------------------------------------------------------------------------------------");
        System.out.println(" ######                      #    #                       #    #    #     #    #    ");
        System.out.println(" #     #   ##   #####   ##   #    # # ###### #    #       #   # #   #     #   # #   ");
        System.out.println(" #     #  #  #    #    #  #  #    # # #      #    #       #  #   #  #     #  #   #  ");
        System.out.println(" #     # #    #   #   #    # #    # # #####  #    #       # #     # #     # #     # ");
        System.out.println(" #     # ######   #   ###### #    # # #      # ## # #     # #######  #   #  ####### ");
        System.out.println(" #     # #    #   #   #    #  #  #  # #      ##  ## #     # #     #   # #   #     # ");
        System.out.println(" ######  #    #   #   #    #   ##   # ###### #    #  #####  #     #    #    #     # ");
        System.out.println("------------------------------------------------------------------------------------");

        // Step 1
        System.out.println();
        System.out.println("Step 1: Authenticate against OCS");
        OCSClient ocsClient = new OCSClient();

        try {
            // Step 2
            System.out.println();
            System.out.println("Step 2: Create types, streams, and data");
            if (needData) {
                createData(ocsClient);
            }

            // Step 3
            System.out.println();
            System.out.println("Step 3: Create a data view");
            DataView dataView = new DataView(sampleDataViewId, sampleDataViewName, sampleDataViewDescription);
            ocsClient.DataViews.createOrUpdateDataView(namespaceId, dataView);

            // Step 4
            System.out.println();
            System.out.println("Step 4: Retrieve the data view");
            dataView = ocsClient.DataViews.getDataView(namespaceId, sampleDataViewId);
            System.out.println(ocsClient.mGson.toJson(dataView));

            // Step 5
            System.out.println();
            System.out.println("Step 5: Add a query for data items");
            Query query = new Query(sampleQueryId, sampleQueryString);
            dataView.setQueries(new Query[] { query });
            ocsClient.DataViews.createOrUpdateDataView(namespaceId, dataView);

            // Step 6
            System.out.println();
            System.out.println("Step 6: View items found by the query");
            System.out.println("List data items found by the query:");
            ResolvedItems<DataItem> dataItems = ocsClient.DataViews.getDataItemsByQuery(namespaceId, sampleDataViewId,
                    sampleQueryId);
            System.out.println(ocsClient.mGson.toJson(dataItems));

            System.out.println("List ineligible data items found by the query:");
            dataItems = ocsClient.DataViews.getIneligibleDataItemsByQuery(namespaceId, sampleDataViewId, sampleQueryId);
            System.out.println(ocsClient.mGson.toJson(dataItems));

            // Step 7
            System.out.println();
            System.out.println("Step 7: View fields available to include in the data view");
            ResolvedItems<FieldSet> availableFields = ocsClient.DataViews.getAvailableFieldSets(namespaceId,
                    sampleDataViewId);
            System.out.println(ocsClient.mGson.toJson(availableFields));

            // Step 8
            System.out.println();
            System.out.println("Step 8: Include some of the available fields");
            dataView.setDataFieldSets(availableFields.getItems());
            ocsClient.DataViews.createOrUpdateDataView(namespaceId, dataView);

            System.out.println("List available field sets:");
            availableFields = ocsClient.DataViews.getAvailableFieldSets(namespaceId, sampleDataViewId);
            System.out.println(ocsClient.mGson.toJson(availableFields));

            System.out.println("Retrieving data from the data view:");
            String dataViewData = ocsClient.DataViews.getDataViewData(namespaceId, sampleDataViewId,
                    sampleStartTime.toString(), sampleEndTime.toString(), sampleInterval).getResponse();
            System.out.println(dataViewData);
            assert dataViewData.length() > 0 : "Error getting data view data";

            // Step 9
            System.out.println();
            System.out.println("Step 9: Group the data view");
            Field grouping = new Field(FieldSource.Id, null, "{DistinguisherValue} {FirstKey}");
            dataView.setGroupingFields(new Field[] { grouping });
            ocsClient.DataViews.createOrUpdateDataView(namespaceId, dataView);

            System.out.println("Retrieving data from the data view:");
            dataViewData = ocsClient.DataViews.getDataViewData(namespaceId, sampleDataViewId,
                    sampleStartTime.toString(), sampleEndTime.toString(), sampleInterval).getResponse();
            System.out.println(dataViewData);
            assert dataViewData.length() > 0 : "Error getting data view data";

            // Step 10
            System.out.println();
            System.out.println("Step 10: Identify data items");
            FieldSet dvDataItemFieldSet = findFieldSet(dataView.getDataFieldSets(), sampleQueryId);
            assert dvDataItemFieldSet != null : "Error finding field set";
            dvDataItemFieldSet.setIdentifyingField(dataView.getGroupingFields()[0]);
            dataView.setGroupingFields(new Field[0]);
            ocsClient.DataViews.createOrUpdateDataView(namespaceId, dataView);

            System.out.println("Retrieving data from the data view:");
            dataViewData = ocsClient.DataViews.getDataViewData(namespaceId, sampleDataViewId,
                    sampleStartTime.toString(), sampleEndTime.toString(), sampleInterval).getResponse();
            System.out.println(dataViewData);
            assert dataViewData.length() > 0 : "Error getting data view data";

            // Step 11
            System.out.println();
            System.out.println("Step 11: Consolidate data fields");
            Field field1 = findField(dvDataItemFieldSet.getDataFields(), FieldSource.PropertyId,
                    sampleFieldToConsolidateTo);
            Field field2 = findField(dvDataItemFieldSet.getDataFields(), FieldSource.PropertyId,
                    sampleFieldToConsolidate);
            assert field1 != null : "Error finding data field";
            assert field2 != null : "Error finding data field";
            System.out.println(ocsClient.mGson.toJson(field1));
            System.out.println(ocsClient.mGson.toJson(field2));
            ArrayList<String> keys = new ArrayList<String>(Arrays.asList(field1.getKeys()));
            keys.add(sampleFieldToConsolidate);
            field1.setKeys(Arrays.copyOf(keys.toArray(), keys.size(), String[].class));
            ArrayList<Field> fields = new ArrayList<Field>(Arrays.asList(dvDataItemFieldSet.getDataFields()));
            fields.remove(field2);
            dvDataItemFieldSet.setDataFields(Arrays.copyOf(fields.toArray(), fields.size(), Field[].class));
            ocsClient.DataViews.createOrUpdateDataView(namespaceId, dataView);

            System.out.println("Retrieving data from the data view:");
            dataViewData = ocsClient.DataViews.getDataViewData(namespaceId, sampleDataViewId,
                    sampleStartTime.toString(), sampleEndTime.toString(), sampleInterval).getResponse();
            System.out.println(dataViewData);
            assert dataViewData.length() > 0 : "Error getting data view data";
        } catch (Exception e) {
            e.printStackTrace();
            success = false;
        } finally {
            // Step 12
            System.out.println();
            System.out.println("Step 12: Delete sample objects from OCS");
            try {
                System.out.println("Deleting data view...");
                ocsClient.DataViews.deleteDataView(namespaceId, sampleDataViewId);
            } catch (Exception e) {
                e.printStackTrace();
                success = false;
            }
            if (needData) {
                cleanUp(ocsClient);
            }
        }
        return success;
    }

    private static void createData(OCSClient ocsClient) throws Exception {
        try {
            SdsType doubleType = new SdsType("doubleType", "", "", SdsTypeCode.Double);
            SdsType dateTimeType = new SdsType("dateTimeType", "", "", SdsTypeCode.DateTime);

            SdsTypeProperty pressureDoubleProperty = new SdsTypeProperty("pressure", "", "", doubleType, false);
            SdsTypeProperty temperatureDoubleProperty = new SdsTypeProperty(sampleFieldToConsolidateTo, "", "",
                    doubleType, false);
            SdsTypeProperty ambientTemperatureDoubleProperty = new SdsTypeProperty(sampleFieldToConsolidate, "", "",
                    doubleType, false);
            SdsTypeProperty timeDateTimeProperty = new SdsTypeProperty("time", "", "", dateTimeType, true);

            SdsType sdsType1 = new SdsType(sampleTypeId1, "", "", SdsTypeCode.Object,
                    new SdsTypeProperty[] { pressureDoubleProperty, temperatureDoubleProperty, timeDateTimeProperty });
            SdsType sdsType2 = new SdsType(sampleTypeId2, "", "", SdsTypeCode.Object, new SdsTypeProperty[] {
                    pressureDoubleProperty, ambientTemperatureDoubleProperty, timeDateTimeProperty });

            System.out.println("Creating SDS Types...");
            ocsClient.Types.createType(tenantId, namespaceId, sdsType1);
            ocsClient.Types.createType(tenantId, namespaceId, sdsType2);

            SdsStream stream1 = new SdsStream(sampleStreamId1, sampleTypeId1, "", sampleStreamName1);
            SdsStream stream2 = new SdsStream(sampleStreamId2, sampleTypeId2, "", sampleStreamName2);

            System.out.println("Creating SDS Streams...");
            ocsClient.Streams.createStream(tenantId, namespaceId, stream1);
            ocsClient.Streams.createStream(tenantId, namespaceId, stream2);

            sampleStartTime = Instant.now().minus(Duration.ofHours(1));
            sampleEndTime = Instant.now();

            ArrayList<String> values1 = new ArrayList<String>();
            ArrayList<String> values2 = new ArrayList<String>();

            System.out.println("Generating values...");
            for (int i = 1; i < 30; i += 1) {
                String val1 = ("{\"time\" : \"" + sampleStartTime.plus(Duration.ofMinutes(i * 2)) + "\", \"pressure\":"
                        + Math.random() * 100 + ", \"" + sampleFieldToConsolidateTo + "\":" + (Math.random() * 20) + 50
                        + "}");
                String val2 = ("{\"time\" : \"" + sampleStartTime.plus(Duration.ofMinutes(i * 2)) + "\", \"pressure\":"
                        + Math.random() * 100 + ", \"" + sampleFieldToConsolidate + "\":" + (Math.random() * 20) + 50
                        + "}");
                values1.add(val1);
                values2.add(val2);
            }

            String pVals = "[" + String.join(",", values1) + "]";
            String tVals = "[" + String.join(",", values2) + "]";

            System.out.println("Sending values...");
            ocsClient.Streams.updateValues(tenantId, namespaceId, sampleStreamId1, pVals);
            ocsClient.Streams.updateValues(tenantId, namespaceId, sampleStreamId2, tVals);
        } catch (Exception e) {
            printError("Error creating Sds Objects", e);
            throw e;
        }
    }

    /**
     * Prints out a formated error string
     *
     * @param exceptionDescription - the description of what the error is
     * @param exception            - the exception thrown
     */
    private static void printError(String exceptionDescription, Exception exception) {
        System.out.println("\n\n======= " + exceptionDescription + " =======");
        System.out.println(exception.toString());
        System.out.println("======= End of " + exceptionDescription + " =======");
    }

    private static String getConfiguration(String propertyId) {
        String property = "";
        Properties props = new Properties();

        try (InputStream inputStream = new FileInputStream("config.properties")) {
            // if launching from git folder use this:
            // "\\basic_samples\\DataViews\\JAVA\\config.properties");
            props.load(inputStream);
            property = props.getProperty(propertyId);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return property;
    }

    public static void cleanUp(OCSClient ocsClient) {
        System.out.println("Deleting sample streams...");
        try {
            ocsClient.Streams.deleteStream(tenantId, namespaceId, sampleStreamId1);
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            ocsClient.Streams.deleteStream(tenantId, namespaceId, sampleStreamId2);
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("Deleting sample types...");
        try {
            ocsClient.Types.deleteType(tenantId, namespaceId, sampleTypeId1);
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            ocsClient.Types.deleteType(tenantId, namespaceId, sampleTypeId2);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
