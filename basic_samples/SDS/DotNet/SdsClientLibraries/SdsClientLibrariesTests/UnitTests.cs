using Xunit;

namespace SdsClientLibrariesCoreTests
{
    public class UnitTests
    {
        [Fact]
        public void Test1()
        {
            Assert.True(SdsClientLibraries.Program.MainAsync(true).Result);
        }
    }
}
