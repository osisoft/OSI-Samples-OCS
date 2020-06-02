import { AppPage } from './app.po';
import { browser } from 'protractor';

const fs = require('fs');

function writeScreenShot(data, filename) {
  const stream = fs.createWriteStream(filename);
  stream.write(new Buffer(data, 'base64'));
  stream.end();
}

describe('SDS Angular Sample', () => {
  let page: AppPage;
  let originalTimeout;

  beforeEach((done) => {
    originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
    jasmine.DEFAULT_TIMEOUT_INTERVAL = 1000000;
    page = new AppPage();
    done();
  });

  it('Should run to completion', async (done) => {
    await browser.waitForAngularEnabled(false);
    await page.navigateTo();
    await page.login2();
    await browser.driver.sleep(15000);
    await page.createType();
    await page.createStream();
    await page.writeData();
    await page.retrieveEvents();
    await page.updateValues();
    await page.replaceValues();
    await page.retrieveInterpolatedValues();
    await page.retrieveFilteredValues();
    await page.retrieveSampledValues();
    await page.propertyOverride();
    await page.createSdsType2();
    await page.createSdsStream2();
    await page.retrieveEventsBasedOnSdsView();
    await page.createStreamViewWithProps();
    await page.getEvents2();
    await page.sdsStreamViewMap();
    await browser.driver.sleep(5000);
    await page.updateStreamType();
    await page.queryTypes();
    await page.createTagsAndMetaData();
    await page.getTags();
    await page.getMetadata();
    await page.deleteVal();
    await page.secondaryCreate();
    await page.secondaryUpdate();
    await page.createCompoundTypeandStream();
    await page.createAndRetrieveCompoundData();
    await page.deleteRest();
    done();
  });

  afterEach((done) => {
    browser.takeScreenshot().then(function (png) {
      writeScreenShot(png, 'afterEach.png');
    });

    jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    done();
  });

  afterAll((done) => {
    browser.takeScreenshot().then(function (png) {
      writeScreenShot(png, 'afterAll.png');
    });
    page.deleteRest();
    done();
  });
});
