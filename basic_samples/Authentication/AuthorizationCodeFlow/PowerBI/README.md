# Authorization Code Flow + PKCE Sample and Test for Power BI Desktop

**Version:** 1.0.4

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/Auth_PKCE_PowerBI?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=996&branchName=master)

The OCS Connector for Power BI Desktop is used to get data from the OCS API into Power BI Desktop. The connector uses the OAuth Authorization Code with PKCE flow to connect to the API and get an access token.

## Prerequisites

1. Visual Studio 2019+
1. [Power Query SDK](https://marketplace.visualstudio.com/items?itemName=Dakahn.PowerQuerySDK)
1. [Power BI Desktop](https://powerbi.microsoft.com/en-us/desktop/)
1. Register an Authorization Code Client in OCS and ensure that the registered client:
   - Contains `https://oauth.powerbi.com/views/oauthredirect.html` in the list of Allowed Redirect URLs
   - Contains `https://login.microsoftonline.com/logout.srf` in the list of Allowed Logout Redirect URLs
   - Contains `https://oauth.powerbi.com` in the list of Allowed CORS Origins
   - Use this Client ID when configuring the project in the [Setup](#Setup) section of this guide.

## Setup

1. Open Power BI Desktop, and navigate to File > Options and Settings > Options
1. Navigate to Security, and under Data Extensions select the option "(Not Recommended) Allow any extension to load without validation or warning"
1. Click OK, acknowledge any warnings, then close Power BI Desktop
1. Once prerequisites are installed, open `OCSConnector.sln` in Visual Studio
1. Update the files url, tenant_id, and client_id with your respective values
   - Note: URL may not need to be modified from the default of `https://dat-b.osisoft.com/`
1. Build the project
1. In your user's `Documents` folder, create a folder `Power BI Desktop` with a subfolder `Custom Connectors`
1. Copy the `.mez` file from either `/bin/Debug` or `/bin/Release` (depending on settings) into the new `Custom Connectors` folder
1. Start up Power BI Desktop, and the connector should be available

## Using the Connector

1. From Power BI Desktop, open Home > Get Data > More
1. The connector should be available as "OSIsoft Cloud Services Sample (Beta)" in the category "Online Services"
1. Select it and click "Connect"
1. If using the connector for the first time, you may get another warning regarding untrusted connectors
1. When prompted for what URL settings to use,
   - OCS URI: This should be the base url of OSIsoft Cloud Services, like `https://dat-b.osisoft.com`
   - API URL Path: This should be the API endpoint path and parameters to use, like `/api/v1/Tenants/{tenantId}/Namespaces/`
   - Timeout: Optionally, define a timeout in seconds for the request, usually only necessary for extremely large queries. By default, the timeout is 100 seconds.
1. Click OK, and you will be prompted to login if you have not already, using an organizational account
1. Once logged in, the Power Query Editor should open with the results.

When using the Power Query Advanced Editor, the function `OCSConnector_Sample.Contents` can be used. The parameters correspond to the parameters described above; `ocsUri`, `apiUri`, and `timeout`.

## Using the Results

The query will look something like:

```C#
let
    Source = OCSConnector.Contents("https://dat-b.osisoft.com", "/api/v1/Tenants/{tenantid}/")
in
    Source
```

However, the results will be displayed as binary content, which is not directly consumable by Power BI. The binary first needs to be parsed. Data from OSIsoft Cloud Services is usually returned as JSON, but some endpoints can also return CSV format. Generally, if the parameter `form=csv` or `form=csvh` is being used, the content is returned in CSV format, otherwise the content is in JSON format. Not all endpoints support the `form` parameter.

To parse the binary content, right click on it, and select either "CSV" or "JSON".

If your content is CSV, the data should be ready to use. If the column headers are using default names like Column1, make sure you are using `form=csvh` (CSV with headers) instead of `form=csv`. Power BI should parse the headers from `csvh` format into column headers automatically.

If your content is in JSON, you will now see a list of "Record" objects that are still not easily consumable. To convert the results to a table, right click the `List` header and select `To Table`, accepting the default options.

This does little better, the data is then displayed as a list of "Record" objects under the header "Column1." However, now there is an icon with two arrows in that column header. Click that button, and then select what fields to use in the table, and expand out the data.

Once the data is expanded, if necessary, right click on column headers and use the "Change Type" options to assign the proper types, as all fields are treated as strings by default.

At this point, the data should be consumable in a Power BI Dashboard! The final query will look something like:

```C#
let
    Source = OCSConnector_Sample.Contents("https://dat-b.osisoft.com/", "api/v1/Tenants/{tenantid}/Namespaces/"),
    Converted = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expanded = Table.ExpandRecordColumn(Converted, "Column1", {"Id", "Region", "Self", "Description", "State"}, {"Column1.Id", "Column1.Region", "Column1.Self", "Column1.Description", "Column1.State"})
in
    Expanded
```

## Tests

Included is an automated test that runs CodedUI to make sure that the OCS Connector sample works. To run this test, you must have at least one recent source in PowerBI that has at least 1 record, and you must have have been logged in and selected Stay Logged In.
This test simply checks to make sure the recent source works with a refresh and we can click on the first result. Since the test uses CodedUI, it might not work on environments other than the internal OSIsoft test agent due to window positioning and other settings.

To run the test from the command line on the machine with PowerBI Desktop:

1. Build the test project using `msbuild` from the folder with the test .csproj (see all steps and prerequisites above need to do that)
1. Navigate to the sub-directoy \bin\Debug
1. Run `mstest /testcontainer:OCSConnectorTest.dll`

**Note:** When running a CodedUI test you should not move the mouse on that computer, or have anything else that can change the mouse movement or window focus during the test. Doing so can cause the test to fail.

---

For the general steps or switch languages see the Task [ReadMe](../../../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
