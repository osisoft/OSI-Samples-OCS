using NUnit.Framework;

namespace CSVtoOCS_pkceTest
{
    public class UnitTest1
    {
        [SetUp]
        public void Setup()
        {
            CSVtoOCS.SystemBrowser.OpenBrowser = new OpenTestBrowser();
        }

        [Test]
        public void Test1()
        {
            Assert.True(CSVtoOCS.Program.MainAsync(true).Result);
        }
    }
}