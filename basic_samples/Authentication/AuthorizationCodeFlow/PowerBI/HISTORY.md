# Version History

## 1.0.3 / 2020-05-01

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
