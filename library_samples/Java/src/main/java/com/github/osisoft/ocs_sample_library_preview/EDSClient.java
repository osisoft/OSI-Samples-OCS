package com.github.osisoft.ocs_sample_library_preview;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.util.Map;

import com.github.osisoft.ocs_sample_library_preview.sds.*;

/**
 * Client to call into for interacting with EDS
 */
public class EDSClient {

    /**
     * Client to help with interactions with streams
     */
    public StreamsClient Streams;
    /**
     * Client to help with interactions with types
     */
    public TypesClient Types;
    /**
     * Helper with json actions
     */
    public Gson mGson = null;

    private BaseClient baseClient;

    /**
     * Client to call into for interacting with EDS. Is configured from config file
     * running at base program's folder
     */
    public EDSClient() {
        baseClient = new BaseClient("v1", "default", "http://localhost:5590");
        init();
    }

    /**
     * Client to call into for interacting with EDS. Is configured from config file
     * running at base program's folder.
     * 
     * @param port       Port number for EDS, default is 5590
     * @param apiVersion API Version for EDS, default is v1
     */
    public EDSClient(String apiVersion, String resource) {
        baseClient = new BaseClient(apiVersion, "default", resource);
        init();
    }

    private void init() {
        Types = new TypesClient(baseClient);
        Streams = new StreamsClient(baseClient);
        mGson = baseClient.mGson;
    }

    /**
     * Helper function used in some of the clients
     * 
     * @param input json string
     * @return Map<String,Object>[]
     */
    public Map<String, Object>[] jsonStringToMapArray(String input) {
        return mGson.fromJson(input, new TypeToken<Map<String, Object>[]>() {
        }.getType());
    }
}
