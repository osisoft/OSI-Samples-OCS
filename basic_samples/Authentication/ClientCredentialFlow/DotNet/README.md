# Client Credential Flow Sample and Test

**Version:** 1.1.1

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/Auth_CC_DotNet?branchName=master)](https://dev.azure.com/osieng/engineering/_build?definitionId=595&branchName=master)

This client uses the OAuth2/OIDC Client Credential Flow to obtain an access token. See the root folder [README](../../../README.md) for more information about this flow.

## Requirements

- .NET Core 3.1 or later

Replace the placeholders in the [appsettings](appsettings.json) file with your Tenant Id, Client Id and Client Secret, and the current Api Version. There is no need to replace the Namespace Id for this sample.

Developed against DotNet 3.1.

## Running the sample

### Prerequisites

- Register a Client Credential client in OCS.
- Replace the placeholders in the [appsettings](appsettings.json) file with your Tenant Id, Client Id, and Client Secret obtained from registration.

### Using Visual Studio

- Load the .csproj
- Rebuild project
- Run it
  - If you want to see the token and other outputs from the program, put a breakpoint at the end of the main method and run in debug mode

### Using Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of this project:

```shell
dotnet run
```

## Running the automated test

### Test Using Visual Studio

- Load the .csproj from the ClientCredentialFlowTest directory above this in Visual Studio
- Rebuild project
- Open Test Explorer and make sure there is one test called Test1 showing
- Run the test

### Test Using Command Line

- Make sure you have the install location of dotnet added to your path
- Run the following command from the location of the ClientCredentialFlowTest project:

```shell
dotnet test
```

---

Tested against DotNet 3.1.

For the general steps or switch languages see the Task [ReadMe](../../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
