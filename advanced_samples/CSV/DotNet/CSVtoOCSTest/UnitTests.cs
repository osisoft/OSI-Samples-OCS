namespace CSVtoOCSTest
{
    using Xunit;

    /// <summary>
    /// Holds all of the tests.
    /// </summary>
    public class UnitTests
    {
        /// <summary>
        /// Simple E2E test.
        /// </summary>
        [Fact]
        public void CSVtoOCSTest()
        {
            CSVtoOCS.SystemBrowser.OpenBrowser = new OpenTestBrowser();
            Assert.True(CSVtoOCS.Program.MainAsync(true).Result);
        }
    }
}