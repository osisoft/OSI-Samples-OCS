# OSIsoft OCS Samples
OSIsoft Cloud Services ([OCS](https://www.osisoft.com/Solutions/OSIsoft-Cloud-Services/)) is a highly flexible cloud-based platform that provides scalable, elastic,
centralized environment to aggregate data for reporting, advanced analytics, and third-party applications.  OCS is powered by OSIsoft's Sequential Data Store (SDS). In this GitHub repo, we provide samples which will help you get started with the [OCS API](https://ocs-docs.osisoft.com/) against your [OCS instance](https://cloud.osisoft.com/welcome).

If you are interested in other OSIsoft samples please see [OSIsoft Samples](https://github.com/osisoft/OSI-Samples).  

There is currently one type of sample in the repo:

* <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon">  Getting Started - OCS focused samples for a task, usually implemented as a simple console app or single page application.  There are also base libraries that may be used in other apps.

Some tasks and individual language examples may have some additional labels as follows:

* \* denotes that the language example uses the rest API directily instead of a library

* <img src="./miscellaneous/images/ctp.png" alt="ctp icon">   This task and code uses services that are currently in preview.  If you are interested in this functionality, please contact OCS support.  



The official OCS samples are divided in multiple categories depending on the scenario and problem/task, accessible through the following table:


Task|Description|Languages|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Test&nbsp;Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
----|-----------|---------|-----------
**<a href="basic_samples/Authentication/">Authentication</a>**  <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | **Client Credential** <a href="basic_samples/Authentication/">Details</a> <br /> **Hybrid Authentication** <a href="basic_samples/Authentication/">Details</a> <br /> **Implicit Authentication** <a href="basic_samples/Authentication/">Details</a> <br /> **Authorization Code Flow** <a href="basic_samples/Authentication/">Details</a>  | <a href="basic_samples/Authentication/ClientCredentialFlow/DotNet/ClientCredentialFlow">.NET</a> <br /> <a href="basic_samples/Authentication/HybridFlow/DotNet/HybridFlow">.NET</a><br /><a href="basic_samples/Authentication/ImplicitFlow/DotNet/ImplicitFlow">.NET and JavaScript</a> <br /><a href="basic_samples/Authentication/AuthorizationCodeFlow/DotNet/AuthorizationCodeFlow">.NET and JavaScript</a>| [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/Auth_CC_DotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4917&branchName=master)<br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/Auth_Hybrid_DotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4918&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/Auth_Implicit_DotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4919&branchName=master)  <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/Auth_PKCE_DotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4920&branchName=master)
**<a href="basic_samples/SDS">Types, Streams, and retreiving Data -- WaveForm</a>** <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers some typical operations against the SDS, including client credential authentication, creating, updating, and deleting types, streams and events.  This uses a non-time Series Type.  Some tasks are different from the other "Types, Streams, and retreiving Data" task, so look at the task readme for details.  This is a recommended starting example, and a good a base for all other Tasks.  <a href="basic_samples/SDS">Details</a> | <a href="basic_samples/SDS/DotNet/SdsClientLibraries/SdsClientLibraries">.NET</a><br /><a href="basic_samples/SDS/DotNet/SdsRestApiCore/SdsRestApiCore">.NET*</a><br /><a href="basic_samples/SDS/Java/sdsjava">JAVA</a><br /><a href="basic_samples/SDS/JavaScript/Angular">Angular</a><br /><a href="basic_samples/SDS/JavaScript/NodeJs">nodeJS</a><br /><a href="basic_samples/SDS/Python/SDSPy/Python3">Python3</a> | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSDotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4912&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSDotNetAPI?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4914&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSJava?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4910&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSangJS?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4923&branchName=master) <br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSnodeJS?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4922&branchName=master) <br /> [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDSPy?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4907&branchName=master)
**<a href="basic_samples/SDS_TimeSeries">Types, Streams, and retreiving Data -- Time-Series</a>** <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers some typical operations against the SDS, including client credential authentication, creating, and deleting types and streams.  This sample is based on Time-Series data.  Some tasks are different from the other "Types, Streams, and retreiving Data" task, so look at the task readme for details.  This is a recommended starting example, and a good a base for all other Tasks.  <a href="basic_samples/SDS_TimeSeries">Details</a>| <a href="basic_samples/SDS_TimeSeries/Python">Python</a> <br /> <a href="basic_samples/SDS_TimeSeries/DotNet/Try">DotNet</a>|[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDS_TSPy?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4909&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/SDS_TSDotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4915&branchName=master)
**<a href="advanced_samples/UomsSample/Dotnet/UomsSample/UomsSample">UOM</a>** <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the basic functionality of the UOM system on OCS | <a href="advanced_samples/UomsSample/Dotnet/UomsSample/UomsSample">.NET</a>&nbsp; &nbsp; | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/UOM_DotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4921&branchName=master)
**<a href="basic_samples/OmfIngress/DotNet/OmfIngressClientLibraries/OmfIngressClientLibraries">OMF Ingress</a>** <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | Covers the basic functionality of configuring and using the OMF Ingress | <a href="basic_samples/OmfIngress/DotNet/OmfIngressClientLibraries/OmfIngressClientLibraries">.NET</a>&nbsp; &nbsp; | [![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/OMF_Ing_DotNet?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4916&branchName=master)
**<a href="library_samples/">Sample Libraries</a>** <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | These sample libraries are used as the base for the other samples.  They are designed to be straightforward implementations of the REST APIs.  They are for use in the samples.  <a href="library_samples/">Details</a>|  <a href="library_samples/Java/ocs_sample_library_preview/">Java</a><br /><a href="library_samples/Python3/">Python3</a>| ~~ <br /> ~~
<img src="./miscellaneous/images/ctp.png" alt="ctp icon">  **<a href="basic_samples/Dataviews/">Dataviews</a>** <img src="./miscellaneous/images/app-type-getting-started.png" alt="getting-started icon"> | These samples highlight basic operations of Dataviews for OCS, including creation, updating, getting data from and deletion of dataviews.  <a href="basic_samples/Dataviews">Details</a> |  <a href="basic_samples/Dataviews/Java/dataviewjava">Java</a><br /><a href="basic_samples/Dataviews/Python3">Python3</a>|[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/DataviewJava?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4911&branchName=master)<br />[![Build Status](https://osisoft.visualstudio.com/Engineering%20Incubation/_apis/build/status/All_Test/DataviewPy?branchName=master)](https://osisoft.visualstudio.com/Engineering%20Incubation/_build/latest?definitionId=4908&branchName=master)

~~ These libraries are tested by being used in other apps.
   
   __Note__: Tests with automated UI browser components (such as Hybrid Authentication, Implicit Authentication, Authorization Code Flow and Angular samples) fail intermittently due to automatation issues.  
   


For OMF to OCS samples please see the OMF repository: [OSIsoft-Samples--OMF](https://github.com/osisoft/OSIsoft-Samples--OMF)

## Credentials 

A credential file is used in the samples unless otherwise noted in the sample.  The name and location of the credential file should be noted in the sample's readme.  
   

     Note: This is not a secure way to store credentials.  This is to be used at your own risk.  
   
   
   You will need to modify these files locally when you run the samples.


## Feedback

If you have a need for a new sample; if there is a feature or capability that should be demonstrated; if there is an existing sample that should be in your favorite language; please reach out to us and give us feedback at https://feedback.osisoft.com under the OSIsoft GitHub Channel.  [Feedback](https://feedback.osisoft.com/forums/922279-osisoft-github).   
 
## Support

If your support question or issue is related to something with an OSIsoft product (an error message, a problem with product configuration, etc...), please open a case with OSIsoft Tech Support through myOSIsoft Customer Portal  (https://my.osisoft.com).

If your support question or issue is related to a non-modified sample (or test) or documentation for the sample; please email Samples@osisoft.com.


## Contributions

If you wish to contribute please take a look at the [contribution guide](CONTRIBUTING.md).

## License

[OSI Samples](https://github.com/osisoft/OSI-Samples) are licensed under the [Apache 2 license](./LICENSE.md).
