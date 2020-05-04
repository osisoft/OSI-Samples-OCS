namespace CSVtoOCSTest
{
    using Xunit;

    /// <summary>
    /// Holds all of the tests.
    /// </summary>
    public class UnitTest1
    {
        /// <summary>
        /// Simple E2E test.
        /// </summary>
        [Fact]
        public void Test1()
        {
            CSVtoOCS.SystemBrowser.OpenBrowser = new OpenTestBrowser();
            Assert.True(CSVtoOCS.Program.MainAsync(true).Result);
        }
    }
}