# OCS Dataview Data Analysis Sample using Jupyter

**Version:** 1.0.0

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/PI-System/PIWebAPI_Data_Analysis?branchName=master)](https://dev.azure.com/osieng/engineering/_build?definitionId=1644&branchName=master)

The sample code in this folder demonstrates how to utilize the OCS Dataviews to do some basic data analysis using Python Jupyter Notebook. In order to run this sample, you need to have [Python](https://www.python.org/downloads/) installed.

## Background and Problem

### Background


### Problem Statement


### Data Overview

## Getting Started

- Clone the GitHub repository
- Install the required modules by running the following command in the terminal : `pip install -r requirements.txt`

### Setting up the AF database and the PI Data Archive

- In the `Jupyter` folder, populate the values of `config.ini` with your own system configuration.
  For example:

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


### Running Jupyter Notebook

- Open a terminal and type in `jupyter notebook`. This will open a browser window. Navigate to the cloned repository and open up `Wind Turbine OCS Data_OCS Python Library .ipynb`. Run the cells one by one and you can see the output in browser itself.
- The last cell in the notebook is for running unit tests so that you can test your PI Web API connection is working properly. As it tests the methods defined earlier in the notebook, you need to run the previous cells (the one which defines the GET and POST methods) of the notebook before trying to run the unit tests.

## Documentation

The documentation for the various controllers and topics can be found at your local PI Web API help system: [https://your-server/piwebapi/help](https://your-server/piwebapi/help)

## Authentication and minimum versions

The sample works with Basic authentication.
This sample has been tested on `PI Web API 2018 SP1`, `PI AF Server 2018 SP2` and `PI Data Archive 2018 SP2`.

---

For the main PI Web API page [ReadMe](../)  
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
