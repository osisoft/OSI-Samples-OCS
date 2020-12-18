# Bulk Uploader SDS DotNet Sample

**Version:** 1.0.7

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/CSVtoOCS_DotNet?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=1393&branchName=master)

Developed against DotNet core 3.1.

---

## About this sample

This sample uses SDS OCSclients to send values, streams, types and dataviews. This simple sample sends SDS JSON messages that are saved pre-formed as files named sdsType.json, sdsStream.json, sdsdata{streamID}.json, dataview.json. It sends the files in that order. If there are metadata or tag files it will send that for the streams.

It does only basic error checking to make sure the message was accepted by the endpoint. The primary function of this sample is for easy bulk loading of data for other samples (particularly ML based samples where the amount of data is prohibitive to include in the sample itself). Included in the [SampleCollections](../SampleCollections) are the data sets including an editable `appsettings.json`.

## Requirements

The [.NET Core CLI](https://docs.microsoft.com/en-us/dotnet/core/tools/) is referenced in this sample, and should be installed to run the sample from the command line.

## Configuration

This sample needs an OMF client credential created. For details on creating those see [OSIsoft Learning Channel](https://www.youtube.com/watch?v=52lAnkGC1IM).

Configure the sample using the file [appsettings.placeholder.json](BulkUploader/appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

1. `Resource` can usually be left as default, but should be the host specified at the beginning of the URL in the [OCS API Console](https://cloud.osisoft.com/apiconsole)
1. `TenantId` should be the ID that comes after `/Tenants/` in the same URL
1. `NamespaceId` should be the name of the OCS [Namespace](https://cloud.osisoft.com/namespaces) to send the data to
1. `ClientId` should be the ID of a [Client Credentials Client](https://cloud.osisoft.com/clients).
1. `ClientSecret` should be the secret from the Client Credentials Client that was specified
1. `DataView` is the path to the dataview json file.
1. `Type` is the path to the type json file.
1. `Metadata` is the path and start to the file name of the stream metadata json file. A streamId is appended to this to find the json file. (note streams must be sent too)
1. `Tags` is the path and start to the file name of the stream tags json file. A streamId is appended to this to find the json file. (note streams must be sent too)
1. `Data` is the path and start to the file name of the stream data json file. A streamId is appended to this to find the json file. (note streams must be sent too)
1. `DataOnly` is a boolean to indicate there are data files and to infer the stream name from the file name, of what comes between sdsdata and the file extension .json

## Running the Sample

1. Clone the GitHub repository
1. Open the folder with your favorite IDE
1. Update `appsettings.json` with your credentials
1. `dotnet restore`
1. `dotnet run`

## Running the Automated Test

From the command line, run

```shell
dotnet restore
dotnet test
```

---

For the OMF landing page [ReadMe](../../../)  
For the OSIsoft Samples landing page [ReadMe](https://github.com/osisoft/OSI-Samples)
