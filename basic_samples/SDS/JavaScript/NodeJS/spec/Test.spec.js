describe('Sds', function() {
  var Sample = require('../Sample');
  jasmine.DEFAULT_TIMEOUT_INTERVAL = 60000;

  beforeEach(function() {});

  it('should be able to complete the main method', function(done) {
    sample = Sample(null, null)
      .catch(function(err) {
        console.log(err);
      })
      .finally(function() {
        done();
      });
  });
});
