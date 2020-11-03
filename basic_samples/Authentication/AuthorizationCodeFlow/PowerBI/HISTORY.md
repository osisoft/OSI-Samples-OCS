# Version History

## 1.0.11 / 2020-11-02

- Updated dependencies

## 1.0.10 / 2020-09-21

- Updated dependencies

## 1.0.9 / 2020-09-08

- Fix issue in test due to saved credentials

## 1.0.8 / 2020-08-06

- Updated dependencies

## 1.0.7 / 2020-08-04

- Add documentation name for connector dialog
- Convert ocsUri and apiUri parameters to single url parameter using Uri.Type

## 1.0.6 / 2020-07-29

- Add sample credentials file to gitignore and replace with placeholder

## 1.0.5 / 2020-06-26

- Updated test using Appium in place of Coded UI

## 1.0.4 / 2020-05-06

- Fix issues with build settings in solution file

## 1.0.3 / 2020-05-05

- Updated to use Polaris in place of Coverity

## 1.0.2 / 2020-05-01

- Converted API endpoint path to optional parameter so that OAuth token is reused
- Removed `Refresh` OAuth signature as no refresh token is provided by the Authorization Code + PKCE flow
- Added optional timeout parameter for large / long queries
- Removed `Json.Document` function call so that `form=csv` can be used in API

## 1.0.1 / 2020-01-31

- Updated README
- Updated build pipelines

## 1.0.0 / 2020-01-24

- Initial public release
