# CSV to OCS sample

**Version:** 1.0.4

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/CSVtoOCS_DotNet?branchName=master)](https://dev.azure.com/osieng/engineering/_build?definitionId=1393&branchName=master)

Developed against DotNet core 3.1.

## About this sample

This sample sends data from a passed in csv file or from the datafile.csv file local to the application to OCS.
This sample uses the Authentication flow to authenticate against OCS. .  
By default it will create the type and the streams used in the defauly datafile.csv.
When testing it will check the values to make sure they are saved on OCS.
When testing, at the end, it will delete whatever it added to the system.

## Running this sample

In this example we assume that you have the dotnet core CLI.

### Prerequisites

- Register an Authorization Code client in OCS and ensure that the registered client in OCS contains `https://127.0.0.1:54567/signin-oidc` in the list of RedirectUris. For details on this please see this [video](https://www.youtube.com/watch?v=97QJjUKa6Pk)
- Replace the placeholders in the [appsettings](appsettings.json) file with your Tenant Id, Client Id, and Client Secret obtained from registration.

### Configure constants for connecting and authentication

The configuration of this application is done in the file [appsettings.placeholder.json](.\CSVtoOCS\appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

Please update the appsettings.json file with the appropriate information as shown below. This sample leverages PKCE login, so that way the user running this application has appropriate authorization.

```json
{
  "NamespaceId": "REPLACE_WITH_NAMESPACE_ID",
  "TenantId": "REPLACE_WITH_TENANT_ID",
  "Resource": "https://dat-b.osisoft.com",
  "ClientId": "REPLACE_WITH_APPLICATION_IDENTIFIER",
  "ClientKey": "REPLACE_WITH_APPLICATION_SECRET",
  "ApiVersion": "v1"
}
```

### Using Command Line

To run this example from the commandline run:

```shell
dotnet restore
dotnet run
```

To test this program change directories to the test and run:

```shell
dotnet restore
dotnet test
```

---

For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
