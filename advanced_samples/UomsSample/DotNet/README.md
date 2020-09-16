# UOMs DotNet Sample

**Version:** 1.1.5

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/UOM_DotNet?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=928&branchName=master)

Developed against DotNet 3.1.

## Running the sample

Configure the sample using the file [appsettings.placeholder.json](UomsSample/appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

Replace the placeholders in the `appsettings.json` file with your TenantID, NamespaceId, ClientID and ClientSecret.

### Requirements

- .NET Core 3.1 or later
- Reliable internet connection

### Using Visual Studio

- Load the .csproj
- Rebuild solution
- Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode

### Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

## Sample Steps

The UOM sample follows these steps

1. Instantiate an SDS client and obtain an authentication token
1. Create an SdsType with UOMs specified
1. Create SdsStream with uom override
1. Create SdsStream using default uom
1. Generate data and send to both streams
1. Retrieve data for both streams using stream default UOM
1. Retrieve data for both streams using UOM request override
1. Delete objects

---

Tested against DotNet 3.1.

For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
