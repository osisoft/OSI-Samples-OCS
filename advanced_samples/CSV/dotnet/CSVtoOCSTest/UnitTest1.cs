using Xunit;

namespace CSVtoOCSTest
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            CSVtoOCS.SystemBrowser.OpenBrowser = new OpenTestBrowser();
            Assert.True(CSVtoOCS.Program.MainAsync(true).Result);
        }
    }
}