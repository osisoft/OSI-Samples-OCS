# Building a Python client to make REST API calls to the SDS Service

**Version:** 1.0.17

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/SDS_TS_Python?branchName=master)](https://dev.azure.com/osieng/engineering/_build?definitionId=927&branchName=master)

The sample code in this topic demonstrates how to invoke SDS REST APIs using Python. By examining the code, you will see how to create an SdsType and SdsStream, and how to create, read, update, and delete values in SDS. You will also see the effect of the accept verbosity header, summaries value call, and how to do bulk streams calls.

This sample code uses the python `requests` module, which natively supports encoding. As a result, the requests in this sample will automatically include the `Accept-Encoding` header and automatically decompress the encoded responses before returning them to the user, so no special handling is required to support compression.

The sections that follow provide a brief description of the process from beginning to end.

Developed against Python 3.7.2.

## Running the Sample

1. Clone the GitHub repository
1. Install required modules: `pip install -r requirements.txt`
1. Open the folder with your favorite IDE
1. Configure the sample using the file [config.placeholder.ini](config.placeholder.ini). Before editing, rename this file to `config.ini`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.
1. Update `config.ini` with the credentials provided by OSIsoft
1. Run `program.py`

To Test the sample:

1. Run `python test.py`

or

1. Install pytest `pip install pytest`
1. Run `pytest program.py`

## Configure the Sample

Included in the sample there is a configuration file with placeholders that need to be replaced with the proper values. They include information for authentication, connecting to the SDS Service, and pointing to a namespace.

To run this sample against the Edge Data Store, the sample must be run locally on the machine where Edge Data Store is installed. In addition, the same config information must be entered with the exception of the `[Credentials]` section of the file. For a typical or default installation, the values will be:

- `Namespace = default`
- `Resource = http://localhost:5590`
- `Tenant = default`
- `ApiVersion = v1`

The values to be replaced are in `config.ini`:

```ini
[Configurations]
Namespace = Samples

[Access]
Resource = https://dat-b.osisoft.com
Tenant = REPLACE_WITH_TENANT_ID
ApiVersion = v1

[Credentials]
ClientId = REPLACE_WITH_APPLICATION_IDENTIFIER
ClientSecret = REPLACE_WITH_APPLICATION_SECRET
```

---

Automated test uses Python 3.6.8 x64

For the general steps or switch languages see the Task [ReadMe](../../../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
