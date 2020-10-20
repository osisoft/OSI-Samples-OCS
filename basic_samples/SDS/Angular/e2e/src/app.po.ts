import { browser, by, element, protractor } from 'protractor';
import cred from './cred.json';

export class AppPage {
  helper(path: string, expectation: string): any {
    console.log(path);
    return element(by.id(path))
      .click()
      .then((res) => {
        browser.driver.sleep(2500);
        element(by.id(path + 'Message'))
          .getText()
          .then((txt) => {
            expect(txt).toContain(expectation);
          });
      });
  }

  createType(): any {
    return this.helper('createType', '20');
  }

  createStream(): any {
    return this.helper('createStream', '20');
  }

  writeData(): any {
    return this.helper('writeWaveDataEvents', '20');
  }

  retrieveEvents(): any {
    return this.helper('retrieveWaveDataEvents', '10 events');
  }

  // todo update this
  retrieveWaveDataEventsHeaders(): any {
    return this.helper('retrieveWaveDataEventsHeaders', '');
  }

  updateValues(): any {
    return this.helper('updateWaveDataEvents', '20');
  }

  replaceValues(): any {
    return this.helper('replaceWaveDataEvents', '20');
  }

  // todo update this
  retrieveInterpolatedValues(): any {
    return this.helper('retrieveInterpolatedValues', '');
  }

  // todo update this
  retrieveFilteredValues(): any {
    return this.helper('retrieveFilteredValues', '');
  }

  // todo update this
  retrieveSampledValues(): any {
    return this.helper('retrieveSampledValues', '');
  }

  propertyOverride(): any {
    return this.helper('createPropertyOverrideAndUpdateStream', '20');
  }

  createSdsType2(): any {
    return this.helper('createAutoStreamViewTargetType', '20');
  }

  createSdsStream2(): any {
    return this.helper('createAutoStreamView', '20');
  }

  retrieveEventsBasedOnSdsView(): any {
    return this.helper('retrieveWaveDataEventsAutoStreamView', '');
  }

  createStreamViewWithProps(): any {
    return this.helper('createSdsStreamViewPropertiesAndManualType', '20');
  }

  getEvents2(): any {
    return this.helper('retrieveWaveDataEventsManualStreamView', '');
  }

  sdsStreamViewMap(): any {
    return this.helper('getSdsStreamViewMap', '');
  }

  updateStreamType(): any {
    return this.helper('updateStreamType', '');
  }

  queryTypes(): any {
    return this.helper('queryTypes', '');
  }

  createTagsAndMetaData(): any {
    return this.helper('createTagsAndMetadata', '20');
  }

  getTags(): any {
    return this.helper('getAndPrintTags', '');
  }

  getMetadata(): any {
    return this.helper('getAndPrintMetadata', '');
  }

  patchMetaData(): any {
    return this.helper('patchMetadata', '20');
  }

  getMetadata2(): any {
    return this.helper('getAndPrintMetadata2', '');
  }

  deleteVal(): any {
    return this.helper('deleteAllValues', '20');
  }

  secondaryCreate(): any {
    return this.helper('secondaryCreate', '');
  }

  secondaryUpdate(): any {
    return this.helper('secondaryUpdate', '');
  }

  secondaryDelete(): any {
    return this.helper('secondaryDelete', '');
  }

  createCompoundTypeandStream(): any {
    return this.helper('createCompoundTypeandStream', '');
  }

  createAndRetrieveCompoundData(): any {
    return this.helper('createAndRetrieveCompoundData', '');
  }

  deleteRest(): any {
    return this.helper('cleanup', '');
  }

  navigateTo() {
    return browser.get(browser.baseUrl) as Promise<any>;
  }

  getTitleText() {
    return element(by.css('app-root h1')).getText() as Promise<string>;
  }

  login2() {
    return element(by.xpath('/html/body/app-root/nav/div/a[2]'))
      .click()
      .then(() => {
        browser.driver.sleep(3000).then(() => {
          browser.driver.findElement(by.css('a.osi-provider')).then((ele) => {
            ele.click().then(() => {
              browser.driver.sleep(3000).then(() => {
                this.loginWithOutlook(cred.login, cred.pass);
              });
            });
          });
        });
      });
  }

  loginWithOutlook(username, passphrase) {
    return this.selectWindow(0).then(() => {
      return browser.driver
        .findElement(by.xpath('//*[@id="i0116"]'))
        .then((el) => {
          el.sendKeys(username + protractor.Key.ENTER);
        })
        .then(() => {
          browser.driver.sleep(4000);
        })
        .then(() => {
          browser.driver
            .findElement(by.xpath('//*[@id="i0118"]'))
            .then((el) => {
              el.sendKeys(passphrase + protractor.Key.ENTER);
            })
            .then(() => {
              browser.driver.sleep(4000);
            })
            .then(() => {
              // Login may or may not prompt to save credentials, try this inside try/catch
              try {
                browser.driver
                  .findElement(by.xpath('//*[@id="idSIButton9"]'))
                  .then((el) => {
                    el.click();
                  });
              } catch {}
            });
        });
    });
  }

  selectWindow(index) {
    browser.driver.wait(function () {
      return browser.driver.getAllWindowHandles().then((handles) => {
        if (handles.length > index) {
          return true;
        }
      });
    });

    return browser.driver.getAllWindowHandles().then((handles) => {
      return browser.driver.switchTo().window(handles[index]);
    });
  }
}
