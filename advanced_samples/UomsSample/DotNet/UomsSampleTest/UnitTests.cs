using Xunit;

namespace Tests
{
    public class UnitTests
    {
        [Fact]
        public void UomsSampleTest()
        {
            Assert.True(UomsSample.Program.MainAsync(true).Result);
        }
    }
}