using NUnit.Framework;

namespace HybridFlowTest
{
    public class Tests
    {
        [SetUp]
        public void Setup()
        {
            HybridFlow.SystemBrowser.openBrowser = new OpenTestBrowser();
        }

        [Test]
        public void Test1()
        {
            HybridFlow.Program.Main(new string[0]);
        }

    }
}