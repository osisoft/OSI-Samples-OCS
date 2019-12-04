package com.github.osisoft.ocs_sample_library_preview.dataviews;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

import com.github.osisoft.ocs_sample_library_preview.*;

/**
 * This client helps with all calls against the DataViews service on OCS
 */
public class DataViewClient {
    private String baseUrl = null;
    private String apiVersion = null;
    private Gson mGson = null;
    private BaseClient baseClient;
    // REST API url strings
    // base of all requests
    private String requestBase = "api/{apiVersion}/Tenants/{tenantId}/Namespaces/{namespaceId}";

    // DataView path
    private String dataViewBase = requestBase + "/DataViews";
    private String dataViewPath = dataViewBase + "/{dataViewId}";
    private String getDataViewInterpolated = dataViewPath
            + "/data/interpolated?startIndex={startIndex}&endIndex={endIndex}&interval={interval}&form={form}&count={count}";

    private String dataGroupPath = dataViewPath + "/DataGroups";
    private String getDataGroups = dataGroupPath + "?skip={skip}&count={count}";

    /**
     * Constructor
     * 
     * @param base baseclient handles some of the base information needed during
     *             calling ocs
     */
    public DataViewClient(BaseClient base) {
        baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
    }

    /**
     * Creates the DataView
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namespace to go against
     * @param dataViewDef DataView definition
     * @return the created DataView
     * @throws SdsError any error that occurs
     */
    public DataView postDataView(String tenantId, String namespaceId, DataView dataViewDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";
        String dataViewId = dataViewDef.getId();

        try {
            url = new URL(baseUrl + dataViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId));
            urlConnection = baseClient.getConnection(url, "POST");

            String body = mGson.toJson(dataViewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "create DataView request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        DataView results = mGson.fromJson(response, new TypeToken<DataView>() {
        }.getType());
        return results;
    }

    /**
     * Updates a DataView
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namespace to go against
     * @param DataViewDef DataView definiton to update to
     * @return updated DataView
     * @throws SdsErrorany error that occurs
     */
    public void putDataView(String tenantId, String namespaceId, DataView DataViewDef) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String DataViewId = DataViewDef.getId();

        try {
            url = new URL(baseUrl + dataViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{dataViewId}", DataViewId));
            urlConnection = baseClient.getConnection(url, "PUT");

            String body = mGson.toJson(DataViewDef);
            OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
            OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8);
            writer.write(body);
            writer.close();

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED
                    || httpResult == HttpURLConnection.HTTP_NO_CONTENT) {
            } else {
                throw new SdsError(urlConnection, "update DataView request failed");
            }
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Deletes the specified DataView
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namespace to go against
     * @param dataViewId  DataView to delete
     * @return response (should be empty)
     * @throws SdsError any error that occurs
     */
    public String deleteDataView(String tenantId, String namespaceId, String dataViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            url = new URL(baseUrl + dataViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId));
            urlConnection = baseClient.getConnection(url, "DELETE");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED
                    || httpResult == HttpURLConnection.HTTP_NO_CONTENT) {
            } else {
                throw new SdsError(urlConnection, "delete DataView request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }

    /**
     * Gets the specified DataView
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namepsace to go against
     * @param dataViewId  DataView to get
     * @return the DataView
     * @throws SdsError any error that occurs
     */
    public DataView getDataView(String tenantId, String namespaceId, String dataViewId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            url = new URL(baseUrl + dataViewPath.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get DataView request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        DataView results = mGson.fromJson(response, new TypeToken<DataView>() {
        }.getType());
        return results;
    }

    /**
     * Retrieves all of the DataViews
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namespace to go against
     * @return arraylist of DataViews
     * @throws SdsError any error that occurs
     */
    public ArrayList<DataView> getDataViews(String tenantId, String namespaceId) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            url = new URL(baseUrl + dataViewBase.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get DataViews request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        ArrayList<DataView> results = mGson.fromJson(response, new TypeToken<ArrayList<DataView>>() {
        }.getType());
        return results;
    }

    /**
     * Gets the DataGroups of the specified DataView
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namespace to go against
     * @param dataViewId  the DataView to get DataGroups from
     * @param skip        number of DataGroups to skip, used in paging
     * @param count       nubmer of DataGroups to get
     * @return DataGroups
     * @throws SdsError any error that occurs
     */
    public DataGroups getDataGroups(String tenantId, String namespaceId, String dataViewId, Integer skip, Integer count)
            throws SdsError {
        String response = getDataGroupsString(tenantId, namespaceId, dataViewId, skip, count);

        DataGroups results = mGson.fromJson(response.toString(), new TypeToken<DataGroups>() {
        }.getType());
        return results;
    }

    /**
     * Returns the DataGroups of a DataView as a string rather than casting it int a
     * DataGroups
     * 
     * @param tenantId    tenant to go against
     * @param namespaceId namespace to go against
     * @param dataViewId  the DataView to get DataGroups from
     * @param skip        number of DataGroups to skip, used in paging
     * @param count       nubmer of DataGroups to get
     * @return DataGroups as a JSON string
     * @throws SdsError any error that occurs
     */
    public String getDataGroupsString(String tenantId, String namespaceId, String dataViewId, Integer skip,
            Integer count) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            url = new URL(baseUrl + getDataGroups.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId)
                    .replace("{skip}", skip.toString()).replace("{count}", count.toString()));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get DataView DataGroups request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }

    /**
     * Get a single DataGroup
     * 
     * @param tenantId    tenant to work against
     * @param namespaceId namespace to work against
     * @param dataViewId  DataView to get the DataGroup from
     * @param dataGroupId specific DataGroup from the DataView to get
     * @return DataGroup
     * @throws SdsError any error that occurs
     */
    public DataGroup getDataGroup(String tenantId, String namespaceId, String dataViewId, String dataGroupId)
            throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            url = new URL(baseUrl + getDataGroups.replace("{apiVersion}", apiVersion).replace("{tenantId}", tenantId)
                    .replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId)
                    .replace("{dataGroupId}", dataGroupId.toString()));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get DataView DataGroup request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        DataGroup results = mGson.fromJson(response, new TypeToken<DataGroup>() {
        }.getType());
        return results;
    }

    /**
     * Gets interpolated values for the DataView
     * 
     * @param tenantId    tenant to work against
     * @param namespaceId namespace to work against
     * @param dataViewId  the DataView to get data from
     * @return the values to return as string
     * @throws SdsError any error that occurs
     */
    public String getDataViewInterpolated(String tenantId, String namespaceId, String dataViewId) throws SdsError {
        return getDataViewInterpolated(tenantId, namespaceId, dataViewId, "", "", "", "", 0);
    }

    /**
     * Gets interpolated values for the DataView
     * 
     * @param tenantId    tenant to work against
     * @param namespaceId namespace to work against
     * @param dataViewId  the DataView to get data from
     * @param startIndex  the start index
     * @param endIndex    the end index
     * @param interval    the interval between return points
     * @param form        the way the returned data is present
     * @param count       the number of returned points
     * @return string of the values asked for
     * @throws SdsError any error that occurs
     */
    public String getDataViewInterpolated(String tenantId, String namespaceId, String dataViewId, String startIndex,
            String endIndex, String interval, String form, Integer count) throws SdsError {
        URL url = null;
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            url = new URL(baseUrl + getDataViewInterpolated.replace("{apiVersion}", apiVersion)
                    .replace("{tenantId}", tenantId).replace("{namespaceId}", namespaceId)
                    .replace("{dataViewId}", dataViewId).replace("{startIndex}", startIndex.toString())
                    .replace("{endIndex}", endIndex.toString()).replace("{interval}", interval.toString())
                    .replace("{form}", form.toString()).replace("{count}", count.toString()));
            urlConnection = baseClient.getConnection(url, "GET");

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_OK || httpResult == HttpURLConnection.HTTP_CREATED) {
            } else {
                throw new SdsError(urlConnection, "get DataView data interpolated request failed");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (MalformedURLException mal) {
            System.out.println("MalformedURLException");
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }
}
