using NUnit.Framework;

namespace ClientCredentialFlowTest
{
    public class Tests
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void Test1()
        {
            ClientCredentialFlow.Program.Main(null);
        }
    }
}