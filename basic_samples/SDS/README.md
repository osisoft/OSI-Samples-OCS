Welcome
========

The SDS Client waveform samples are introductory, language-specific examples of programming against the SDS Service. They are intended as instructional samples only.

There are some differences between these samples and the TimesSeries samples.  The differences include the Type being used and some of the calls being highlighted.  Please check out the Sample Patterns and the code to determine which sample is most appropriate for you.

Note: The calls highlighted here which are not in the other sample are not specific to non-Time-Series data.

Sample Pattern
--------------

All SDS waveform samples are console applications that follow the same sequence of events, allowing you to select the langauge with which you are most comfortable without missing any instructional features. The pattern followed is:

1.  Instantiate an SDS client and Obtain an authentication token
2.  Create an SdsType to represent the data being stored
3.  Create an SdsStream to store event data in
4.  Create and insert events into the stream
5.  Retrieve events for a specified range
6.  Retrieve events in table format with headers
7.  Update events
8.  Replace events
9.  Retrieve events and interpolated events 
10. Retrieve filtered events
11. Retrieve Sampled values 
12. Demonstrate SdsStream Property Overrides
13. Use SdsStreamViews and SdsStreamViewMaps
14. Use SdsStreamViews to update StreamType
15. Filtering on types 
16. Tags & Metadata
17. Delete events
18. Create an SdsStream with a secondary index, update an existing stream to a secondary index and remove a secondary index
19. Created an SdsType and SdsStream with Compound index
20. Inserting and retreiving compound index data
21. Delete objects

These steps illustrate the fundamental programming steps of SDS.  Feel free to modify the samples and propose changes.

Step numbers are searchable in the code.  For find the relevant part of the code for filtering on types search: Step 14


|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
------|------------
<a href="DotNet/SdsClientLibraries/SdsClientLibraries">.NET</a><br /><a href="DotNet/SdsRestApiCore">.NET*</a><br /><a href="Java/sdsjava">JAVA</a><br /><a href="JavaScript/Angular">Angular</a><br /><a href="JavaScript/NodeJs">nodeJS</a><br /><a href="Python/SDSPy/Python3">Python3</a> | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSDotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4912&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSDotNetAPI?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4914&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSJava?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4910&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSangJS?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4923&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSnodeJS?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4922&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSPy?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4907&branchName=master)


For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)<br />
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
