/** BaseClient.java
 * 
 */

package com.github.osisoft.ocs_sample_library_preview;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.*;
import java.net.*;
import java.net.http.HttpRequest;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Date;
import java.util.Properties;
import java.util.zip.GZIPInputStream;

/**
 * Base client that helps with interactions to OCS
 */
public class BaseClient {
    /**
     * accessible json converter
     */
    public Gson mGson = null;
    /**
     * use this to see the base url for going against OCS
     */
    public String baseUrl = null;
    /**
     * api version used for the calls
     */
    public String apiVersion = null;

    private String cachedAccessToken = null;
    private Date accessTokenExpiration = new Date(Long.MIN_VALUE);
    private long FIVE_SECONDS_IN_MILLISECONDS = 5000;

    // config parameters
    private String TenantId = "";
    private String ClientId = "";
    private String ClientSecret = "";
    private String Resource = "";

    public String getTenantId() {
        return this.TenantId;
    }

    /**
     * Creates a baseclient. Reading information from the configuration file at the
     * program's running folder
     */
    public BaseClient() {
        this.TenantId = getConfiguration("tenantId");
        this.ClientId = getConfiguration("clientId");
        this.ClientSecret = getConfiguration("clientSecret");
        this.Resource = getConfiguration("resource");
        this.Resource = Resource.endsWith("/") ? Resource : Resource + "/";

        this.baseUrl = this.Resource;
        this.apiVersion = getConfiguration("apiVersion");
        this.mGson = new Gson();
    }

    /**
     * Creates a baseclient using the passed information rather than the
     * configuration settings
     * 
     * @param apiVersion API version of SDS
     * @param tenantId   The tenant identifier
     * @param resource   SDS url
     */
    public BaseClient(String apiVersion, String tenantId, String resource) {
        this.TenantId = tenantId;
        this.Resource = resource;
        this.Resource = this.Resource.endsWith("/") ? this.Resource : this.Resource + "/";

        this.baseUrl = this.Resource;
        this.apiVersion = apiVersion;
        this.mGson = new Gson();
    }

    /**
     * Creates a baseclient using the passed information rather than the
     * configuration settings
     * 
     * @param apiVersion   APIversion of OCS
     * @param tenantId     The tenant identifier
     * @param clientId     Client id to login with
     * @param clientSecret client secret to login with
     * @param resource     OCS url
     */
    public BaseClient(String apiVersion, String tenantId, String clientId, String clientSecret, String resource) {
        this.TenantId = tenantId;
        this.ClientId = clientId;
        this.ClientSecret = clientSecret;
        this.Resource = resource;
        this.Resource = this.Resource.endsWith("/") ? this.Resource : this.Resource + "/";

        this.baseUrl = this.Resource;
        this.apiVersion = apiVersion;
        this.mGson = new Gson();
    }

    /**
     * Makes the connection to the url
     * 
     * @param url    the url to connect to
     * @param method the method to do, put, get, delete, etc...
     * @return
     */
    public HttpURLConnection getConnection(URL url, String method) {
        HttpURLConnection urlConnection = null;
        String token = "";
        if (!this.ClientId.isEmpty()) {
            token = AcquireAuthToken();
        }

        try {
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(method);
            urlConnection.setRequestProperty("Accept", "*/*; q=1");
            urlConnection.setRequestProperty("Accept-Encoding", "gzip");
            urlConnection.setRequestProperty("Content-Type", "application/json");
            if (token != null && !token.isEmpty()) {
                urlConnection.setRequestProperty("Authorization", "Bearer " + token);
            }
            urlConnection.setUseCaches(false);
            urlConnection.setConnectTimeout(50000);
            urlConnection.setReadTimeout(50000);
            if ("POST".equals(method) || "PUT".equals(method) || "DELETE".equals(method)) {
                urlConnection.setDoOutput(true);
            } else if (method == "GET") {
                // Do nothing
            }
        } catch (SocketTimeoutException e) {
            e.printStackTrace();
        } catch (ProtocolException e) {
            e.printStackTrace();
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return urlConnection;
    }

    /**
     * Makes the connection to the url
     * 
     * @param url    the url to connect to
     * @param method the method to do, put, get, delete, etc...
     * @return
     */
    public HttpRequest.Builder getRequest(URI url) {
        HttpRequest.Builder builder = null;
        String token = "";
        if (!this.ClientId.isEmpty()) {
            token = AcquireAuthToken();
        }

        try {
            builder = HttpRequest.newBuilder(url).header("Accept", "*/*; q=1").header("Accept-Encoding", "gzip")
                    .header("Content-Type", "application/json");
            if (token != null && !token.isEmpty()) {
                builder.header("Authorization", "Bearer " + token);
            }
            builder.timeout(Duration.ofMillis(50000));
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return builder;
    }

    /**
     * Helper to get the bearer auth token
     * 
     * @return the token string
     */
    protected String AcquireAuthToken() {

        if (cachedAccessToken != null) {
            long tokenExpirationTime = accessTokenExpiration.getTime(); // returns time in milliseconds.
            long currentTime = System.currentTimeMillis();
            long timeDifference = tokenExpirationTime - currentTime;

            if (timeDifference > FIVE_SECONDS_IN_MILLISECONDS)
                return cachedAccessToken;
        }

        // get new token
        try {
            URL discoveryUrl = new URL(Resource + "identity/.well-known/openid-configuration");
            URLConnection request = discoveryUrl.openConnection();
            request.connect();
            JsonObject rootObj = JsonParser
                    .parseReader(new InputStreamReader((InputStream) request.getContent(), StandardCharsets.UTF_8))
                    .getAsJsonObject();
            String tokenUrl = rootObj.get("token_endpoint").getAsString();

            URL token = new URL(tokenUrl);
            HttpURLConnection tokenRequest = (HttpURLConnection) token.openConnection();
            tokenRequest.setRequestMethod("POST");
            tokenRequest.setRequestProperty("Accept", "application/json");
            tokenRequest.setDoOutput(true);
            tokenRequest.setDoInput(true);
            tokenRequest.setUseCaches(false);

            String postString = "client_id=" + URLEncoder.encode(ClientId, "UTF-8") + "&client_secret="
                    + URLEncoder.encode(ClientSecret, "UTF-8") + "&grant_type=client_credentials";
            byte[] postData = postString.getBytes("UTF-8");
            tokenRequest.setRequestProperty("Content-Length", Integer.toString(postData.length));
            try (OutputStream stream = tokenRequest.getOutputStream()) {
                stream.write(postData);
            }

            String result;
            try (InputStream in = new BufferedInputStream(tokenRequest.getInputStream())) {
                result = org.apache.commons.io.IOUtils.toString(in, "UTF-8");
            }

            JsonObject response = JsonParser.parseString(result).getAsJsonObject();
            cachedAccessToken = response.get("access_token").getAsString();
            Integer timeOut = response.get("expires_in").getAsInt();
            accessTokenExpiration = new Date(System.currentTimeMillis() + timeOut * 1000);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return cachedAccessToken;
    }

    /**
     * helper to get configuration information for the file
     * 
     * @param propertyId which property to retrieve from the file
     * @return the value retrieved
     */
    private String getConfiguration(String propertyId) {

        if (propertyId.equals("clientId") && !ClientId.isEmpty()) {
            return ClientId;
        }

        if (propertyId.equals("clientSecret") && !ClientSecret.isEmpty()) {
            return ClientSecret;
        }

        if (propertyId.equals("resource") && !Resource.isEmpty()) {
            return Resource;
        }

        String property = "";
        try (InputStream inputStream = new FileInputStream("config.properties")) {
            Properties props = new Properties();

            props.load(inputStream);
            property = props.getProperty(propertyId);
            inputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return property.trim();
    }

    /**
     * helper to check if the response code indicates success
     * 
     * @param responseCode code number
     * @return success
     */
    public boolean isSuccessResponseCode(int responseCode) {
        return responseCode >= 200 && responseCode < 300;
    }

    /**
     * helper to decompress the gzip response body of a request
     * 
     * @param urlConnection the request to decompress and read
     * @return decompressed body of request
     */
    public String getResponse(HttpURLConnection urlConnection) {
        String inputLine;
        StringBuffer response = new StringBuffer();

        try {
            String contentEncoding = urlConnection.getHeaderField("Content-Encoding");

            try (InputStreamReader streamReader = contentEncoding != null && contentEncoding.equals("gzip")
                    ? new InputStreamReader(new GZIPInputStream(urlConnection.getInputStream()))
                    : new InputStreamReader(urlConnection.getInputStream(), StandardCharsets.UTF_8)) {
                try (BufferedReader in = new BufferedReader(streamReader)) {
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return response.toString();
    }
}
