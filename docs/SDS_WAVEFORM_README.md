# Welcome

The SDS Client WaveForm samples are introductory, language-specific examples of programming against the SDS Service. They are intended as instructional samples only.

There are some differences between these samples and the TimesSeries samples. The differences include the Type being used, compresssion settings, and many of the steps. Please check out the Sample Pattern and code of both samples to determine which sample is most appropriate for you. All of the SDS Client WaveForm samples are set up to use GZip compression.

## Sample Pattern

All SDS WaveForm samples are console applications that follow the same sequence of events, allowing you to select the language with which you are most comfortable without missing any instructional features. The pattern followed is:

1. Instantiate an SDS client and obtain an authentication token
1. Create an SdsType to represent the data being stored
1. Create an SdsStream to store event data in
1. Create and insert events into the stream
1. Retrieve events for a specified range
1. Retrieve events in table format with headers
1. Update events
1. Replace events
1. Retrieve events and interpolated events
1. Retrieve filtered events
1. Retrieve Sampled values
1. Demonstrate SdsStream Property Overrides
1. Use SdsStreamViews and SdsStreamViewMaps
1. Use SdsStreamViews to update StreamType
1. Filtering on types
1. Create Tags & Metadata
1. Update Metadata
1. Delete events
1. Create an SdsStream with a secondary index, update an existing stream to a secondary index and remove a secondary index
1. Created an SdsType and SdsStream with Compound index
1. Inserting and retreiving compound index data
1. Delete objects

These steps illustrate the fundamental programming steps of SDS. Feel free to modify the samples and/or propose changes.

Step numbers are searchable in the code. For example, to find the relevant part of the code for filtering on types, search: `step 15`

| Languages                                                                         | Test Status                                                                                                                                                                                                                                                                                                                                      |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [.NET Libraries](https://github.com/osisoft/sample-ocs-waveform_libraries-dotnet) | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-waveform_libraries-dotnet?branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=3094&branchName=main)                                                                                      |
| [.NET REST API](https://github.com/osisoft/sample-ocs-waveform_rest_api-dotnet)   | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-waveform_rest_api-dotnet?branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=3093&branchName=main)                                                                                       |
| [Java](https://github.com/osisoft/sample-ocs-waveform-java)                       | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-waveform-java?repoName=osisoft%2Fsample-ocs-waveform-java&branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2629&repoName=osisoft%2Fsample-ocs-waveform-java&branchName=main)          |
| [Angular](https://github.com/osisoft/sample-ocs-waveform-angular)                 | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-waveform-angular?repoName=osisoft%2Fsample-ocs-waveform-angular&branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2626&repoName=osisoft%2Fsample-ocs-waveform-angular&branchName=main) |
| [NodeJS](https://github.com/osisoft/sample-ocs-waveform-nodejs)                   | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-waveform-nodejs?repoName=osisoft%2Fsample-ocs-waveform-nodejs&branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2630&repoName=osisoft%2Fsample-ocs-waveform-nodejs&branchName=main)    |
| [Python](https://github.com/osisoft/sample-ocs-waveform-python)</a>               | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-waveform-python?repoName=osisoft%2Fsample-ocs-waveform-python&branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2631&repoName=osisoft%2Fsample-ocs-waveform-python&branchName=main)    |

---

For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
