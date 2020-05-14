# Grafana OSIsoft Cloud Services Sample

**Version:** 1.0.0

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/Grafana_NodeJS?branchName=master)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=1680&branchName=master)

This sample demonstrates how to build a [Grafana](https://grafana.com/) plugin that runs queries against the Sequential Data Store of OSIsoft Cloud Services. The sample performs normal "Get Values" calls against a specified stream in OCS, using the time range of the Grafana dashboard. See the [Grafana Documentation](https://grafana.com/docs/grafana/latest/developers/plugins/) for more information on developing Grafana plugins.

## Requirements

- [Grafana 6.4+](https://grafana.com/grafana/download)
- Web Browser with JavaScript enbaled
- Register a Client Credentials Client in OSIsoft Cloud Services; a client secret will need to be provided to the sample plugin configuration
- [NodeJS](https://nodejs.org/en/)

## Known Security Issues

This sample has a dependency on the npm package [@grafana/toolkit](https://www.npmjs.com/package/@grafana/toolkit), which has multiple dependencies with security vulnerabilities. Please note that using this sample is potentially unsafe due to these issues. Please review these issues before using this sample. See [VULNERABILITIES.md](VULNERABILITIES.md) for details.

## Running the Sample

1. Copy this folder to your Grafana server's plugins directory, like `.../grafana/data/plugins`
1. (Optional) If using other plugins, rename the folder to `osisoft-cloud-services-sample`
1. Open a command prompt inside that folder
1. Install dependencies, using `npm ci`
1. Build the plugin, using `npm build` (or `npm dev` for browser debugging)
1. Restart the Grafana server to load the new plugin
1. Add a new Grafana datasource using the sample (see [Grafana docs](https://grafana.com/docs/grafana/latest/features/datasources/add-a-data-source/))
1. Enter the relevant required information; the client secret will be encrypted in the Grafana server and HTTP requests to OCS will be made by a server-side proxy, as described in the [Grafana docs](https://grafana.com/docs/grafana/latest/developers/plugins/authentication/)
1. Open a new or existing Grafana dashboard, and choose the OSIsoft Cloud Services Sample as the data source
1. Enter your OCS Namespace and Stream, and data will populate into the dashboard from the stream for the dashboard's time range

## Running the Automated Tests

1. Open a command prompt inside this folder
1. Install dependencies, using `npm ci`
1. Run the tests, using `npm test`

---

For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
