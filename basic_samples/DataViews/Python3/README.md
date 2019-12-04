# Using the OCS Dataview Service in Python

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/DataViews_Python?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=885&branchName=master)

The sample code in this demonstrates how to invoke Dataview REST APIs via the sample Python client [library](https://github.com/osisoft/OSI-Samples/tree/master/library_samples/Python3/ocs_sample_library_preview). The sample demonstrates how to establish a connection to SDS, obtain an authorization token, create an SdsType and SdsStream with data (if needed), create a Dataview, update it, retreive it, and retrieve data from it in different ways. At the end of the sample, everything that was created is deleted.

This example uses the ocs_sample_library_preview library which is also included in this github repo. It is downloadable via pip.

Developed against Python 3.7.2.

## To Run this Sample:

1. Clone the GitHub repository
1. Install required modules: `pip install -r requirements.txt`
1. Open the folder with your favorite IDE
1. Update `config.ini` with the credentials provided by OSIsoft
1. Run `program.py`

To test the sample after running it:

1. Run `python test.py`

or

1. Install pytest `pip install pytest`
1. Run `pytest program.py`

---

Automated test uses Python 3.6.8 x64

For the general steps or switch languages see the Task [ReadMe](../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
