# OCS Data View Data Analysis Sample using Jupyter

**Version:** 1.0.2

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/DataViewWindJupyter?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=1851&branchName=master)

The sample code in this folder demonstrates how to utilize the OCS Data Views to do some basic data analysis using Python Jupyter Notebook. In order to run this sample, you need to have [Python](https://www.python.org/downloads/) installed.

## About the Sample

This sample is intended to show you how you can use an OCS Data View to bring your data from OCS into Jupyter and easily into Pandas to do machine learning. Using an OCS Data View allows you to configure the data you want, in the way you want it, and not have to do as much client side processing of the data. This is a basic sample that shows you a possible way to do machine learning and a possible outcome of looking at the data. This is not a guide to Pandas or machine learning.

## Background and Problem

### Background

Wind turbines operate by capturing kinetic enrgy of wind to turn rotor blades that run a generator. Governed by Betz's law they can only capture 59.3% of kinetic enrgy from wind. This is important, because after a certain limit higher winds do not create additional power. At a certain wind speed, the power actually decreases.

### Problem Statement

Can we predict the power output of our wind turbines based on weather forecast data?

## Getting Started

- Clone the GitHub repository
- Install the required modules by running the following command in the terminal : `pip install -r requirements.txt`
- If running the tests, install the required modules by running the following command in the terminal : `pip install -r test-requirements.txt`

### Data Overview

The data we are using is available in our BulkUpload SampleCollections [folder](https://github.com/osisoft/OSI-Samples-OCS/tree/master/advanced_samples/BulkUpload/SampleCollections/DataViewWind). The steps to upload this data are included in that folder. This sample also skips over the exercise of creating the data view, this is included in the data that you can upload. To see how to create a Data View programmatically, please look at our other sample [here](https://github.com/osisoft/OSI-Samples-OCS/tree/master/basic_samples/DataViews).

This sample data is similar to what you might have from a site where the data has unexpected values and not every turbine behaves exactly the same. The data is only for 1 day. Repeating this exercise but using more days of data would give you a better prediction.

### Setting up the OCS connection

- In the `Jupyter` folder, populate the values of `config.placeholder.ini` with your own system configuration. Before editing, rename this file to `config.ini`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

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

Open a terminal and type in `jupyter notebook`. This will open a browser window. Navigate to the cloned repository and open up `Wind_Turbine_OCS_Data_OCS_Python_Library.ipynb`. Run the cells one by one and you can see the output in browser itself.

### Test Jupyter Notebook

The last cell in the notebook is for running unit tests so that you can test to make sure the whole notebook is working as expected. As it tests the methods defined earlier in the notebook, you need to run the previous cells of the notebook before trying to run the unit tests.

### Automated Tests

The automated tests assume that the data is already lodaded. The steps to load the data and delete the data are included in the .yml but are commented out to not send and delete large amounts of the same data often.

---

For the main PI Web API page [ReadMe](../)  
For the main landing page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
