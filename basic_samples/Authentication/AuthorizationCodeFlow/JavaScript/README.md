# Authorization Code Flow + PKCE JavaScript Sample and Test

**Version:** 1.1.1

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/Auth_PKCE_JavaScript?branchName=master)](https://dev.azure.com/osieng/engineering/_build?definitionId=1203&branchName=master)

This client uses the OAuth2/OIDC Authorization Code Flow + PKCE to obtain an access token. See the root folder [README](../../../README.md) for more information about this flow.

## Requirements

- Node.js 12.6.0+
- Web Browser with Javascript enabled
  - You will need Google Chrome if you want to run the automated test

## Running the sample client

### Prerequisites

- Register an AuthorizationCode client in OCS and ensure that the registered client in OCS contains `http://localhost:5004/callback.html`, and `http://localhost:5004/silent-refresh.html` in the list of RedirectUris.
- Replace the placeholders in the [config](src/config.js) file with your TenantID and ClientID obtained from registration.

You can learn more about the config options [here](https://github.com/IdentityModel/oidc-client-js/wiki#other-optional-settings).

### Running the Sample from the Command Line

1. Make sure Node.js is installed, installation instructions are available at [node.js](https://nodejs.org/en/)
2. Clone the git repository
3. Open a command prompt and navigate to this folder (basic_samples/Authentication/AuthorizationCodeFlow/JavaScript)
4. Install dependencies, using the command line:

   ```shell
   npm ci
   ```

5. Start the http server to host the sample, using:

   ```shell
   npm start
   ```

6. Open a browser and navigate to `http://localhost:5004`
7. Click on `Login` and follow the prompts to log in to OCS

## Running the automated test

### Test Prerequisites

1. Make sure the sample client in the section above is running.
1. Make sure Google Chrome is installed on your test system.
1. Make sure the version of Chrome matches the version defined for the `chromedriver` dependency in [package.json](package.json).
   - If the dependency needs to be updated in `package.json`, after saving, run `npm i` in a command prompt inside this folder to update the package.
1. Update the [config.js](src/config.js) file with the username and password for the Microsoft account that will be used to log in. The test is only written to work with a personal Microsoft account and must only prompt for only username followed by password (no Two-Factor authentication or other consent or informational prompts). Also if the location of the sample application has been modified then change the url location.

### Running the test from the Command Line

Run the command:

```shell
npm test
```

---

For the general steps or switch languages see the Task [ReadMe](../../)  
For the main OCS page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main samples page on master [ReadMe](https://github.com/osisoft/OSI-Samples)
