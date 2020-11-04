package com.github.osisoft.ocs_sample_library_preview.dataviews;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.regex.*;

import com.github.osisoft.ocs_sample_library_preview.*;

/**
 * This client handles calls against the Data View API on OCS
 */
public class DataViewClient {
    private String TenantId;
    private String baseUrl = null;
    private String apiVersion = null;
    private Gson mGson = null;
    private BaseClient baseClient;
    // REST API url strings
    // base of all requests
    private String requestBase;

    // Data View paths
    private String dataViewBase;
    private String dataViewPath;
    private String getDataViews;
    private String resolvedPath;
    private String getDataItems;
    private String getIneligibleDataItems;
    private String getGroups;
    private String getAvailableFieldSets;
    private String getFieldMappings;
    private String getStatistics;
    private String dataInterpolatedPath;
    private String getDataInterpolated;

    private Pattern urlLinks = Pattern.compile("<(\\S+)>; rel=\"(\\S+)\"");

    /**
     * Constructor
     * 
     * @param base BaseClient that handles some base information needed to call OCS
     */
    public DataViewClient(BaseClient base) {
        this.baseClient = base;
        this.baseUrl = base.baseUrl;
        this.apiVersion = base.apiVersion;
        this.mGson = base.mGson;
        this.TenantId = base.getTenantId();
        this.requestBase = "api/" + apiVersion + "-preview/Tenants/" + TenantId + "/Namespaces/{namespaceId}";
        this.dataViewBase = requestBase + "/DataViews";
        this.dataViewPath = dataViewBase + "/{dataViewId}";
        this.getDataViews = dataViewBase + "?skip={skip}&count={count}";
        this.resolvedPath = dataViewPath + "/Resolved";
        this.getDataItems = resolvedPath + "/DataItems/{queryId}?cache={cache}&skip={skip}&count={count}";
        this.getIneligibleDataItems = resolvedPath
                + "/IneligibleDataItems/{queryId}?cache={cache}&skip={skip}&count={count}";
        this.getGroups = resolvedPath + "/Groups?cache={cache}&skip={skip}&count={count}";
        this.getAvailableFieldSets = resolvedPath + "/AvailableFieldSets?cache={cache}";
        this.getFieldMappings = resolvedPath + "/FieldMappings?cache={cache}";
        this.getStatistics = resolvedPath + "/Statistics?cache={cache}";
        this.dataInterpolatedPath = dataViewPath + "/Data/Interpolated";
        this.getDataInterpolated = dataInterpolatedPath
                + "?startIndex={startIndex}&endIndex={endIndex}&interval={interval}&form={form}&cache={cache}&count={count}";
    }

    private String getRequestResponse(URL url, String method, String body) throws SdsError {
        HttpURLConnection urlConnection = null;
        String response = "";

        try {
            urlConnection = baseClient.getConnection(url, method);

            if (body != null) {
                try (OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream())) {
                    try (OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8)) {
                        writer.write(body);
                    }
                }
            }

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_NO_CONTENT) {
                return null;
            } else if (httpResult != HttpURLConnection.HTTP_OK && httpResult != HttpURLConnection.HTTP_CREATED) {
                throw new SdsError(urlConnection, "Request failed.");
            }

            response = baseClient.getResponse(urlConnection);
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }

    private ResponseWithLinks getRequestResponseWithLinks(URL url, String method, String body) throws SdsError {
        HttpURLConnection urlConnection = null;
        ResponseWithLinks response = new ResponseWithLinks();

        try {
            urlConnection = baseClient.getConnection(url, method);

            if (body != null) {
                try (OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream())) {
                    try (OutputStreamWriter writer = new OutputStreamWriter(out, StandardCharsets.UTF_8)) {
                        writer.write(body);
                    }
                }
            }

            int httpResult = urlConnection.getResponseCode();
            if (httpResult == HttpURLConnection.HTTP_NO_CONTENT) {
                return null;
            } else if (httpResult != HttpURLConnection.HTTP_OK && httpResult != HttpURLConnection.HTTP_CREATED) {
                throw new SdsError(urlConnection, "Request failed.");
            }

            String link = urlConnection.getHeaderField("Link");
            if (link != null) {
                Matcher matcher = urlLinks.matcher(link);
                while (matcher.find()) {
                    String name = matcher.group(2);
                    String linkUrl = matcher.group(1);
                    if (name.equals("first")) {
                        response.setFirst(linkUrl);
                    } else if (name.equals("next")) {
                        response.setNext(linkUrl);
                    }
                }
            }

            response.setResponse(baseClient.getResponse(urlConnection));
        } catch (SdsError sdsError) {
            sdsError.print();
            throw sdsError;
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return response;
    }

    /**
     * Returns the specified data view.
     * 
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @return The requested data view
     * @throws SdsError Error response
     */
    public DataView getDataView(String namespaceId, String dataViewId) throws SdsError, MalformedURLException {
        URL url = new URL(
                baseUrl + dataViewPath.replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<DataView>() {
        }.getType());
    }

    /**
     * Returns a list of data views.
     * 
     * @param namespaceId The namespace identifier
     * @return A page of data views. A response header, Total-Count, indicates the
     *         total size of the collection.
     * @throws SdsError Error response
     */
    public ArrayList<DataView> getDataViews(String namespaceId) throws SdsError, MalformedURLException {
        return getDataViews(namespaceId, 0, 100);
    }

    /**
     * Returns a list of data views.
     * 
     * @param namespaceId The namespace identifier
     * @param skip        An optional parameter representing the zero-based offset
     *                    of the first data view to retrieve. If not specified, a
     *                    default value of 0 is used.
     * @param count       An optional parameter representing the maximum number of
     *                    data views to retrieve. If not specified, a default value
     *                    of 100 is used.
     * @return arraylist of DataViews
     * @throws SdsError any error that occurs
     */
    public ArrayList<DataView> getDataViews(String namespaceId, Integer skip, Integer count)
            throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getDataViews.replace("{namespaceId}", namespaceId)
                .replace("{skip}", skip.toString()).replace("{count}", count.toString()));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ArrayList<DataView>>() {
        }.getType());
    }

    /**
     * Create a new data view with a system-generated identifier.
     * 
     * @param namespaceId The namespace identifier
     * @param dataView    A DataView object whose Id is null or unspecified
     * @return The data view as persisted, including values for optional parameters
     *         that were omitted in the request.
     * @throws SdsError Error response
     */
    public DataView createDataView(String namespaceId, DataView dataView) throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + dataViewBase.replace("{namespaceId}", namespaceId));
        String body = mGson.toJson(dataView);
        String response = getRequestResponse(url, "POST", body);
        return mGson.fromJson(response, new TypeToken<DataView>() {
        }.getType());
    }

    /**
     * This call creates the specified data view. If a data view with the same id
     * already exists, the existing data view is compared with the specified data
     * view. If they are identical, a redirect (302 Found) is returned with the
     * Location response header indicating the URL where the stream may be retrieved
     * using a Get function. If the data views do not match, the request fails with
     * 409 Conflict.
     * 
     * @param namespaceId The namespace identifier
     * @param dataView    A DataView object whose Id will be used in the URL path
     * @return The data view as persisted, including values for optional parameters
     *         that were omitted in the request.
     * @throws SdsError Error response
     */
    public DataView getOrCreateDataView(String namespaceId, DataView dataView) throws SdsError, MalformedURLException {
        URL url = new URL(
                baseUrl + dataViewPath.replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataView.getId()));
        String body = mGson.toJson(dataView);
        String response = getRequestResponse(url, "POST", body);
        return mGson.fromJson(response, new TypeToken<DataView>() {
        }.getType());
    }

    /**
     * If a data view with the same id already exists, it is updated to the
     * specified value. Otherwise, a new data view is created.
     * 
     * @param namespaceId The namespace identifier
     * @param dataView    A DataView object whose Id will be used in the URL path
     * @return If data view with the same id exists, null. Otherwise, the data view
     *         as persisted, including values for optional parameters that were
     *         omitted in the request.
     * @throws SdsError Error response
     */
    public DataView createOrUpdateDataView(String namespaceId, DataView dataView)
            throws SdsError, MalformedURLException {
        URL url = new URL(
                baseUrl + dataViewPath.replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataView.getId()));
        String body = mGson.toJson(dataView);
        String response = getRequestResponse(url, "PUT", body);
        return mGson.fromJson(response, new TypeToken<DataView>() {
        }.getType());
    }

    /**
     * Delete the data view with the specified id.
     * 
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @throws SdsError Error response
     */
    public void deleteDataView(String namespaceId, String dataViewId) throws SdsError, MalformedURLException {
        URL url = new URL(
                baseUrl + dataViewPath.replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId));
        getRequestResponse(url, "DELETE", null);
    }

    /**
     * Gets the paged collection of data items that are the results of an individual
     * query, and which are eligible for use in the current data view. A data view
     * has a collection of zero or more queries. Each query has an identifier. Those
     * identifiers are used here as part of the request path.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param queryId     The Query identifier
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         DataItems that resolved.
     * @throws SdsError Error response
     */
    public ResolvedItems<DataItem> getDataItemsByQuery(String namespaceId, String dataViewId, String queryId)
            throws SdsError, MalformedURLException {
        return getDataItemsByQuery(namespaceId, dataViewId, queryId, "Preserve", 0, 100);
    }

    /**
     * Gets the paged collection of data items that are the results of an individual
     * query, and which are eligible for use in the current data view. A data view
     * has a collection of zero or more queries. Each query has an identifier. Those
     * identifiers are used here as part of the request path.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param queryId     The Query identifier
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Preserve" is the
     *                    default value.
     * @param skip        An optional parameter representing the zero-based offset
     *                    of the first data item to retrieve. If not specified, a
     *                    default value of 0 is used.
     * @param count       An optional parameter representing the maximum number of
     *                    data items to retrieve. If not specified, a default value
     *                    of 100 is used.
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         DataItems that resolved.
     * @throws SdsError Error response
     */
    public ResolvedItems<DataItem> getDataItemsByQuery(String namespaceId, String dataViewId, String queryId,
            String cache, Integer skip, Integer count) throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getDataItems.replace("{namespaceId}", namespaceId)
                .replace("{dataViewId}", dataViewId).replace("{queryId}", queryId).replace("{cache}", cache)
                .replace("{skip}", skip.toString()).replace("{count}", count.toString()));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ResolvedItems<DataItem>>() {
        }.getType());
    }

    /**
     * Gets the paged collection of data items that are the results of an individual
     * query, but which are not eligible for use in the current data view. A common
     * reason for ineligibility is that the item's index property is of a different
     * type than the data view expects. A data view has a collection of zero or more
     * queries. Each query has an identifier. Those identifiers are used here as
     * part of the request path.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param queryId     The Query identifier
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         DataItems that resolved.
     * @throws SdsError Error response
     */
    public ResolvedItems<DataItem> getIneligibleDataItemsByQuery(String namespaceId, String dataViewId, String queryId)
            throws SdsError, MalformedURLException {
        return getIneligibleDataItemsByQuery(namespaceId, dataViewId, queryId, "Preserve", 0, 100);
    }

    /**
     * Gets the paged collection of data items that are the results of an individual
     * query, but which are not eligible for use in the current data view. A common
     * reason for ineligibility is that the item's index property is of a different
     * type than the data view expects. A data view has a collection of zero or more
     * queries. Each query has an identifier. Those identifiers are used here as
     * part of the request path.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param queryId     The Query identifier
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Preserve" is the
     *                    default value.
     * @param skip        An optional parameter representing the zero-based offset
     *                    of the first data item to retrieve. If not specified, a
     *                    default value of 0 is used.
     * @param count       An optional parameter representing the maximum number of
     *                    data items to retrieve. If not specified, a default value
     *                    of 100 is used.
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         DataItems that resolved.
     * @throws SdsError Error response
     */
    public ResolvedItems<DataItem> getIneligibleDataItemsByQuery(String namespaceId, String dataViewId, String queryId,
            String cache, Integer skip, Integer count) throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getIneligibleDataItems.replace("{namespaceId}", namespaceId)
                .replace("{dataViewId}", dataViewId).replace("{queryId}", queryId).replace("{cache}", cache)
                .replace("{skip}", skip.toString()).replace("{count}", count.toString()));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ResolvedItems<DataItem>>() {
        }.getType());
    }

    /**
     * Gets the collection of Groups that resolved for a data view.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         Groups that resolved.
     * @throws SdsError Error response
     */
    public ResolvedItems<Group> getGroups(String namespaceId, String dataViewId)
            throws SdsError, MalformedURLException {
        return getGroups(namespaceId, dataViewId, "Preserve", 0, 100);
    }

    /**
     * Gets the collection of Groups that resolved for a data view.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Preserve" is the
     *                    default value.
     * @param skip        An optional parameter representing the zero-based offset
     *                    of the first data item to retrieve. If not specified, a
     *                    default value of 0 is used.
     * @param count       An optional parameter representing the maximum number of
     *                    data items to retrieve. If not specified, a default value
     *                    of 100 is used.
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         Groups that resolved.
     * @throws SdsError Error response
     */
    public ResolvedItems<Group> getGroups(String namespaceId, String dataViewId, String cache, Integer skip,
            Integer count) throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getGroups.replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId)
                .replace("{cache}", cache).replace("{skip}", skip.toString()).replace("{count}", count.toString()));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ResolvedItems<Group>>() {
        }.getType());
    }

    /**
     * Gets the collection of field sets that are available for use in the data
     * view, and which are not already included in the data view.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         FieldSets that resolved and which are still available
     * @throws SdsError Error response
     */
    public ResolvedItems<FieldSet> getAvailableFieldSets(String namespaceId, String dataViewId)
            throws SdsError, MalformedURLException {
        return getAvailableFieldSets(namespaceId, dataViewId, "Preserve");
    }

    /**
     * Gets the collection of field sets that are available for use in the data
     * view, and which are not already included in the data view.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Preserve" is the
     *                    default value.
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         FieldSets that resolved and which are still available
     * @throws SdsError Error response
     */
    public ResolvedItems<FieldSet> getAvailableFieldSets(String namespaceId, String dataViewId, String cache)
            throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getAvailableFieldSets.replace("{namespaceId}", namespaceId)
                .replace("{dataViewId}", dataViewId).replace("{cache}", cache));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ResolvedItems<FieldSet>>() {
        }.getType());
    }

    /**
     * Gets the collection of field mappings resolved for the data view. These show
     * the exact data behind every field, for each data item, for each group.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         FieldMappings that resolved and which are still available
     * @throws SdsError Error response
     */
    public ResolvedItems<FieldMapping> getFieldMappings(String namespaceId, String dataViewId)
            throws SdsError, MalformedURLException {
        return getFieldMappings(namespaceId, dataViewId, "Preserve");
    }

    /**
     * Gets the collection of field mappings resolved for the data view. These show
     * the exact data behind every field, for each data item, for each group.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Preserve" is the
     *                    default value.
     * @return An object with a "TimeOfResolution" and a collection of "Items", the
     *         FieldMappings that resolved and which are still available
     * @throws SdsError Error response
     */
    public ResolvedItems<FieldMapping> getFieldMappings(String namespaceId, String dataViewId, String cache)
            throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getFieldMappings.replace("{namespaceId}", namespaceId)
                .replace("{dataViewId}", dataViewId).replace("{cache}", cache));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ResolvedItems<FieldMapping>>() {
        }.getType());
    }

    /**
     * Gets statistics about the size and shape on how the data view resolved.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @return An object with a "TimeOfResolution" and an "Item", the Statistics
     *         that were retrieved
     * @throws SdsError Error response
     */
    public ResolvedItem<Statistics> getStatistics(String namespaceId, String dataViewId)
            throws SdsError, MalformedURLException {
        return getStatistics(namespaceId, dataViewId, "Preserve");
    }

    /**
     * Gets statistics about the size and shape on how the data view resolved.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Preserve" is the
     *                    default value.
     * @return An object with a "TimeOfResolution" and an "Item", the Statistics
     *         that were retrieved
     * @throws SdsError Error response
     */
    public ResolvedItem<Statistics> getStatistics(String namespaceId, String dataViewId, String cache)
            throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getStatistics.replace("{namespaceId}", namespaceId)
                .replace("{dataViewId}", dataViewId).replace("{cache}", cache));
        String response = getRequestResponse(url, "GET", null);
        return mGson.fromJson(response, new TypeToken<ResolvedItem<Statistics>>() {
        }.getType());
    }

    /**
     * Get data for the provided index parameters with paging. See documentation on
     * paging for further information.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @return ResponseWithLinks, an object containing the String Response in the
     *         requested format, and if returned by the server, also includes links
     *         to the Next and First pages of data.
     * @throws SdsError Error response
     */
    public ResponseWithLinks getDataViewData(String namespaceId, String dataViewId)
            throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl
                + dataInterpolatedPath.replace("{namespaceId}", namespaceId).replace("{dataViewId}", dataViewId));
        return getRequestResponseWithLinks(url, "GET", null);
    }

    /**
     * Get data for the provided index parameters with paging. See documentation on
     * paging for further information.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param startIndex  The requested start index, inclusive. The default value is
     *                    the .DefaultStartIndex of the data view. Optional if a
     *                    default value is specified.
     * @param endIndex    The requested end index, inclusive. The default value is
     *                    the .DefaultEndIndex of the data view. Optional if a
     *                    default value is specified.
     * @param interval    The requested interval between index values. The default
     *                    value is the .DefaultInterval of the data view. Optional
     *                    if a default is specified.
     * @return ResponseWithLinks, an object containing the String Response in the
     *         requested format, and if returned by the server, also includes links
     *         to the Next and First pages of data.
     * @throws SdsError Error response
     */
    public ResponseWithLinks getDataViewData(String namespaceId, String dataViewId, String startIndex, String endIndex,
            String interval) throws SdsError, MalformedURLException {
        return getDataViewData(namespaceId, dataViewId, startIndex, endIndex, interval, "default", "Refresh", 1000);
    }

    /**
     * Get data for the provided index parameters with paging. See documentation on
     * paging for further information.
     *
     * @param namespaceId The namespace identifier
     * @param dataViewId  The data view identifier
     * @param startIndex  The requested start index, inclusive. The default value is
     *                    the .DefaultStartIndex of the data view. Optional if a
     *                    default value is specified.
     * @param endIndex    The requested end index, inclusive. The default value is
     *                    the .DefaultEndIndex of the data view. Optional if a
     *                    default value is specified.
     * @param interval    The requested interval between index values. The default
     *                    value is the .DefaultInterval of the data view. Optional
     *                    if a default is specified.
     * @param form        The requested data output format. Output formats: default,
     *                    table, tableh, csv, csvh.
     * @param cache       "Refresh" to force the resource to re-resolve. "Preserve"
     *                    to use cached information, if available. "Refresh" is the
     *                    default value.
     * @param count       The requested page size. The default value is 1000. The
     *                    maximum is 250,000.
     * @return ResponseWithLinks, an object containing the String Response in the
     *         requested format, and if returned by the server, also includes links
     *         to the Next and First pages of data.
     * @throws SdsError Error response
     */
    public ResponseWithLinks getDataViewData(String namespaceId, String dataViewId, String startIndex, String endIndex,
            String interval, String form, String cache, Integer count) throws SdsError, MalformedURLException {
        URL url = new URL(baseUrl + getDataInterpolated.replace("{namespaceId}", namespaceId)
                .replace("{dataViewId}", dataViewId).replace("{startIndex}", startIndex).replace("{endIndex}", endIndex)
                .replace("{interval}", interval).replace("{form}", form).replace("{cache}", cache)
                .replace("{count}", count.toString()));
        return getRequestResponseWithLinks(url, "GET", null);
    }
}
