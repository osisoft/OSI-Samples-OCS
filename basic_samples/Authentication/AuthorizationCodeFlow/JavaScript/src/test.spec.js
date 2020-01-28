require('chromedriver');
const assert = require('assert');
const { Builder, By, until } = require('selenium-webdriver');
const config = require('./config');

const wait = 5000;

describe('Sample App', () => {
  let driver;

  before(async function() {
    driver = await new Builder().forBrowser('chrome').build();
  });

  after(() => driver && driver.quit());

  it('Should log in to OCS', async function() {
    console.log('open page');
    await driver.get('http://localhost:5004');

    // Click to log in
    console.log('log in');
    await driver.findElement(By.id('login')).click();

    // Select 'Personal Account' Microsoft login
    console.log('personal account');
    await driver
      .wait(
        until.elementLocated(
          By.xpath('descendant::a[@title="Personal Account"]')
        ),
        wait
      )
      .then(e => {
        e.click();
        console.log('click 1');
      });

    // Enter user name, and click Next
    console.log('enter user name');
    await driver
      .wait(until.elementLocated(By.id('i0116')), wait)
      .then(e => e.sendKeys(config.userName));
    console.log('click next');
    await driver
      .wait(until.elementLocated(By.id('idSIButton9')), wait)
      .then(async function(e) {
        await driver.wait(until.elementIsEnabled(e), wait);
        setTimeout(async function() {
          await driver.findElement(By.id('idSIButton9')).click();
          console.log('click 2');
        }, 500);
      });

    // Enter password, and click Next
    console.log('wait for page');
    await driver.wait(until.urlContains('username='), wait);
    console.log('enter password');
    await driver
      .findElement(By.id('i0118'))
      .then(e => e.sendKeys(config.password));
    console.log('click next');
    await driver
      .wait(until.elementLocated(By.id('idSIButton9')), wait)
      .then(async function(e) {
        await driver.wait(until.elementIsEnabled(e), wait);
        setTimeout(async function() {
          await driver.findElement(By.id('idSIButton9')).click();
          console.log('click 3');
        }, 500);
      });

    // Click tenant button, and verify results
    console.log('click tenant');
    await driver
      .wait(until.elementLocated(By.id('tenant')), wait)
      .then(async function(e) {
        await driver.wait(until.elementIsEnabled(e), wait);
        await driver.findElement(By.id('tenant')).click();
        console.log('click 4');
      });
    console.log('get results');
    const results = await driver.findElement(By.id('results')).getText();
    console.log('assert logged in');
    assert(results.includes('User logged in'));
    console.log('complete');
  });
});
