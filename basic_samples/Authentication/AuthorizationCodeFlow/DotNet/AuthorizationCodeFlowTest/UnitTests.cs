using Xunit;

namespace AuthorizationCodeFlowTest
{
    public class UnitTests
    {
        [Fact]
        public void AuthorizationCodeFlowTest()
        {
            AuthorizationCodeFlow.SystemBrowser.OpenBrowser = new OpenTestBrowser();
            AuthorizationCodeFlow.Program.Main();
        }
    }
}