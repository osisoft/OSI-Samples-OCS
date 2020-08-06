const { JUnitXmlReporter } = require('jasmine-reporters');
const Sample = require('../Sample');

var junitReporter = new JUnitXmlReporter({
  savePath: 'TestResults',
});
console.log('test');
jasmine.getEnv().addReporter(junitReporter);
jasmine.DEFAULT_TIMEOUT_INTERVAL = 60000;

describe('SDS NodeJS Sample', function () {
  beforeEach(function () {});

  it('should be able to complete the main method', function (done) {
    console.log('hello?');
    sample = Sample(null, null)
      .catch(function (err) {
        console.log(err);
        expect(err).toBeFalsy();
      })
      .finally(function () {
        done();
      });
  });
});
