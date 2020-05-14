# Dependency Vulnerabilities

This sample references the npm package [@grafana/toolkit](https://www.npmjs.com/package/@grafana/toolkit), which has some dependencies which have identified security vulnerabilities. This sample is potentially unsafe due to these issues. Please review these issues before using this sample.

- JQuery 3.4.1
  - [CVE-2018-18405](https://nvd.nist.gov/vuln/detail/CVE-2018-18405)
  - [CVE-2020-11022](https://nvd.nist.gov/vuln/detail/CVE-2020-11022)
  - [CVE-2020-11023](https://nvd.nist.gov/vuln/detail/CVE-2020-11023)
  - [XSS via 'jQuery.htmlPrefilter'](https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/)
- yargs-parser v11.1.1, 10.1.0
  - [CVE-2020-7608](https://nvd.nist.gov/vuln/detail/CVE-2020-7608)
- Lo-Dash 4.17.15
  - [DoS Vulnerability](https://hackerone.com/reports/670779)
- serialize-javascript 1.9.1
  - [CVE-2019-16769](https://nvd.nist.gov/vuln/detail/CVE-2019-16769)
- minimist 0.0.8
  - [CVE-2020-7598](https://nvd.nist.gov/vuln/detail/CVE-2020-7598)
