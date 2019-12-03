# Using the OCS Dataview Service in Java

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/DataViews_Java?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=884&branchName=master)

The sample code in this demonstrates how to invoke Dataview REST APIs via the sample Java client [library](https://github.com/osisoft/OSI-Samples/tree/master/library_samples/Java/ocs_sample_library_preview). The sample demonstrates how to establish a connection to SDS, obtain an authorization token, create an SdsType and SdsStream with data (if needed), create a Dataview, update it, retreive it, and retrieve data from it in different ways. At the end of the sample, everything that was created is deleted.

## Summary of steps to run the Java demo

Using Eclipse or any IDE:

1. Clone a local copy of the GitHub repository.
1. Install Maven.
1. \*Install the ocs_sample_library_preview to your local Maven repo using run mvn install pom.xml from `\library_samples\Java\ocs_sample_library_preview\`
1. If you are using Eclipse, select `File` > `Import` > `Maven`> `Existing maven project` and then select the local copy.
1. Replace the configuration strings in `config.properties`

Using a command line:

1. Clone a local copy of the GitHub repository.
1. Download apache-maven-x.x.x.zip from http://maven.apache.org and extract it.
1. Setting environment variables.
   1. For Java JDK  
      Variable name - JAVA_HOME  
      Variable value - location to the Java JDK in User variables.  
      and, also add JDK\bin path to the Path variable in System variables.
   1. For Maven  
      Variable name - MAVEN_HOME  
      Variable value - location to the extracted folder for the  
      maven ~\apache-maven-x.x.x in User variables.  
      and, also add ~\apache-maven-x.x.x\bin path to the Path variable in System variables.
1. \*Install the ocs_sample_library_preview to your local Maven repo using run mvn install pom.xml from \library_samples\Java\ocs_sample_library_preview\
1. Building and running the project.
   1. cd to your project location.
   1. run "mvn package exec:java" on cmd.

\*Currently this project is not hosted on the central Maven repo and must be compiled and installed locally.

---

Tested against Maven 3.6.1 and Java 1.8.0_212.

For the general steps or switch languages see the Task [ReadMe](../../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
