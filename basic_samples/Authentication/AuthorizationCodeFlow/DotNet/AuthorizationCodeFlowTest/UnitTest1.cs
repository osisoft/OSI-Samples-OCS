using NUnit.Framework;

namespace AuthorizationCodeFlowTest
{
    public class Tests
    {
        [SetUp]
        public void Setup()
        {
            AuthorizationCodeFlow.SystemBrowser.openBrowser = new OpenTestBrowser();
        }

        [Test]
        public void Test1()
        {
            AuthorizationCodeFlow.Program.Main(new string[0]);
        }

    }
}