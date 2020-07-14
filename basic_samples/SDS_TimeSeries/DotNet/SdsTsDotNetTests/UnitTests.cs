using Xunit;

namespace SdsTsDotNetTests
{
    public class UnitTests
    {
        [Fact]
        public void SdsTsDotNetTest()
        {
            Assert.True(SdsTsDotNet.Program.MainAsync(true).Result);
        }
    }
}
