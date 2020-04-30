# CSV to OCS sample

**Version:** 1.0.0

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/CSVtoOCS_DotNet?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=1393&branchName=master)

Developed against DotNet 3.2.

## Getting Started

In this example we assume that you have the dotnet core CLI.

To run this example from the commandline run

```
dotnet restore
dotnet run
```

to test this program change directories to the test and run

```
dotnet restore
dotnet test
```

## Configure constants for connecting and authentication

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

## About this sample

This sample sends data from a passed in csv file or from the datafile.csv file local to the application to OCS. 
By default it will create the type and the streams used in the defauly datafile.csv. 
When testing it will check the values to make sure they are saved on OCS. 
When testing, at the end, it will delete whatever it added to the system.

---

For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
