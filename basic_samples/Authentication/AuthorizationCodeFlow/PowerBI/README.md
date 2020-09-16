# Authorization Code Flow + PKCE Sample and Test for Power BI Desktop

**Version:** 1.0.9

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
1. Rename the [url.placeholder](OCSConnector/url.placeholder), [tenant_id.placeholder](OCSConnector/tenant_id.placeholder), and [client_id.placeholder](OCSConnector/client_id.placeholder) to `url`, `tenant_id`, and `client_id`. This repository's `.gitignore` rules should prevent these files from being checked in to any fork or branch, to ensure this information is not compromised.
1. Update the files `url`, `tenant_id`, and `client_id` with your respective values
   - Note: URL may not need to be modified from the default of `https://dat-b.osisoft.com/`
1. Build the project
1. In your user's `Documents` folder, create a folder `Power BI Desktop` with a subfolder `Custom Connectors`
1. Copy the `.mez` file from either `/bin/Debug` or `/bin/Release` (depending on settings) into the new `Custom Connectors` folder
1. Start up Power BI Desktop, and the connector should be available

## Building without Visual Studio

As of Power BI Version 2.84.861.0 64-bit (August 2020), Visual Studio builds Custom Connectors into a `.zip` file with a custom file extension, `.mez`. Since these files are in reality simple `.zip` files, it is possible to build or update the connector without using Visual Studio.

To build the connector:

1. Copy and rename the file `OCSConnector.pq` to `OCSConnector.m`
1. Select the files `client_id`, `OCSConnector.m`, `resources.resx`, `tenant_id`, `url`, and all the `.png` files in the `OCSConnector folder
1. Zip these files, using the built in Windows tools or the zip tool of your choice, but be sure to use the `.zip` format
1. Rename the `.zip` file extension to `.mez`
1. Place this `.mez` folder in the same location described in [Setup](#Setup)

To change the settings of the connector:

1. Unzip the `.mez` into a folder
1. Make the necessary changes in the output folder, for example to the `tenant_id` and `client_id` files
1. Select all the files in that folder and zip those files using the `.zip` format
1. Rename the `.zip` file extension to `.mez`
1. Rename or move the old `.mez` file so that Power BI does not load it, and replace it with the updated `.mez` file

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

Included is an automated test that runs the Appium WebDriver to make sure that the OCS Connector sample works. To run this test, you must fill in the [appsettings.json](OCSConnectorTest/appsettings.json) with the OCS URL and a tenant ID that allows login via Personal Microsoft Accounts. You must also fill in the email address and password of a Microsoft Account to use for login.

This test will attempt to clear saved credentials, open the connector, and log in to OSIsoft Cloud Services using the provided credentials, then query the namespaces in that tenant. If this is successful, the test will pass.

Since the test uses Appium WebDriver, updates to Power BI Desktop or other differences in the UI automation fields may prevent the test from passing in environments other than the internal OSIsoft test agent. To resolve issues like this, use [inspect](https://docs.microsoft.com/en-us/windows/win32/winauto/inspect-objects) to validate the names and automation IDs used by the test.

To run the test from the command line on the machine with Power BI Desktop, run:

```shell
dotnet restore
dotnet test
```

**Note:** When running an Appium WebDriver test you should not move the mouse on that computer, or have anything else that can change the mouse movement or window focus during the test. Doing so can cause the test to fail.

---

For the general steps or switch languages see the Task [ReadMe](../../../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
