using Xunit;

namespace SdsRestApiCoreTest
{
    public class UnitTests
    {
        [Fact]
        public void SdsRestApiCoreTest()
        {
            Assert.True(SdsRestApiCore.Program.MainAsync(true).Result);
        }
    }
}
