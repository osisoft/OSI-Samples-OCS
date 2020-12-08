require('chromedriver');
const assert = require('assert');
const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const { JUnitXmlReporter } = require('jasmine-reporters');
const config = require('../src/config');

var junitReporter = new JUnitXmlReporter({
  savePath: 'TestResults',
});
jasmine.getEnv().addReporter(junitReporter);
jasmine.DEFAULT_TIMEOUT_INTERVAL = 60000;

const wait = 5000;

describe('Sample App', () => {
  let driver;

  beforeEach(async function () {
    const options = new chrome.Options();
    options.addArguments('--headless');
    options.addArguments('--no-sandbox');
    driver = await new Builder()
      .forBrowser('chrome')
      .setChromeOptions(options)
      .build();
  });

  afterEach(() => driver && driver.quit());

  it('Should log in to OCS', async function () {
    await driver.get('http://localhost:5004');

    // Click to log in
    await driver.findElement(By.id('login')).click();

    // Select 'Personal Account' Microsoft login
    await driver
      .wait(
        until.elementLocated(
          By.xpath('descendant::a[@title="Personal Account"]')
        ),
        wait
      )
      .then((e) => {
        e.click();
      });

    // Enter user name, and click Next
    await driver
      .wait(until.elementLocated(By.id('i0116')), wait)
      .then((e) => e.sendKeys(config.userName));
    await driver
      .wait(until.elementLocated(By.id('idSIButton9')), wait)
      .then(async function (e) {
        await driver.wait(until.elementIsEnabled(e), wait);
        setTimeout(async function () {
          await driver.findElement(By.id('idSIButton9')).click();
        }, 500);
      });

    // Enter password, and click Next
    await driver.wait(until.urlContains('username='), wait);
    await driver
      .findElement(By.id('i0118'))
      .then((e) => e.sendKeys(config.password));
    await driver
      .wait(until.elementLocated(By.id('idSIButton9')), wait)
      .then(async function (e) {
        await driver.wait(until.elementIsEnabled(e), wait);
        setTimeout(async function () {
          await driver.findElement(By.id('idSIButton9')).click();
        }, 500);
      });

    try {
      // Login may or may not prompt to save credentials, use try/catch.
      await driver
        .wait(until.elementLocated(By.id('idSIButton9')), wait)
        .then(async function (e) {
          await driver.wait(until.elementIsEnabled(e), wait);
          setTimeout(async function () {
            try {
              await driver.findElement(By.id('idSIButton9')).click();
            } catch {}
          }, 500);
        });
    } catch {}

    // Click tenant button, and verify results
    await driver
      .wait(until.elementLocated(By.id('tenant')), wait)
      .then(async function (e) {
        await driver.wait(until.elementIsEnabled(e), wait);
        await driver.findElement(By.id('tenant')).click();
      });
    const results = await driver.findElement(By.id('results')).getText();
    assert(results.includes('User logged in'));
  });
});
