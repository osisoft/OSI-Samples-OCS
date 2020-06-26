using System;
using System.Globalization;
using System.IO;
using Newtonsoft.Json;
using OpenQA.Selenium.Appium;
using OpenQA.Selenium.Appium.Windows;
using Xunit;

namespace OCSConnectorTest
{
    public class UnitTests
    {
        public static AppSettings Settings { get; set; }

        [Fact]
        public void OCSConnectorTest()
        {
            // Load test settings
            Settings = JsonConvert.DeserializeObject<AppSettings>(File.ReadAllText(Directory.GetCurrentDirectory() + "\\appsettings.json"));
            
            // Start Power BI
            var appiumUri = new Uri("http://127.0.0.1:4723");
            var splashOptions = new AppiumOptions();
            splashOptions.AddAdditionalCapability("app", @"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe");
            using var splashSession = new WindowsDriver<WindowsElement>(appiumUri, splashOptions);

            // Find main Power BI Window
            var desktopOptions = new AppiumOptions();
            desktopOptions.AddAdditionalCapability("app", "Root");
            using var desktopSession = new WindowsDriver<WindowsElement>(appiumUri, desktopOptions);

            var powerBIWindow = desktopSession.TryFindElementByName("Untitled - Power BI Desktop");
            var powerBIWindowHandle = powerBIWindow.GetAttribute("NativeWindowHandle");
            powerBIWindowHandle = int.Parse(powerBIWindowHandle, CultureInfo.InvariantCulture)
                .ToString("x", CultureInfo.InvariantCulture); // Convert to Hex

            var powerBIOptions = new AppiumOptions();
            powerBIOptions.AddAdditionalCapability("appTopLevelWindow", powerBIWindowHandle);
            using var powerBISession = new WindowsDriver<WindowsElement>(appiumUri, powerBIOptions);

            // Clear cached credentials
            var queries = powerBISession.TryFindElementByName("Queries");
            var transformData = queries.TryFindElementsByName("Transform data");
            var dataSourceSettings = powerBISession.TryClickAndFindElementByName(transformData[2], "Data source settings");
            var clearPermissions = powerBISession.TryClickAndFindElementByName(dataSourceSettings, "Clear Permissions");
            var delete = powerBISession.TryClickAndFindElementByName(clearPermissions, "Delete", 5);
            if (delete != null)
            {
                delete.Click();
            }

            var close = powerBISession.TryFindElementByName("Close");
            var getData = powerBISession.TryClickAndFindElementByName(close, "Get data");

            // Open OCS Connector
            var search = powerBISession.TryClickAndFindElementByName(getData, "Search");
            search.SendKeys("OSI");

            var sample = powerBISession.TryFindElementByName("OSIsoft Cloud Services Sample (Beta)");
            var connect = powerBISession.TryClickAndFindElementByName(sample, "Connect");
            connect.Click();

            // Enter query info
            var uri = powerBISession.TryFindElementsByName("OSIsoft Cloud Services URI");
            uri[1].SendKeys(Settings.OcsAddress);

            var path = powerBISession.TryFindElementsByName("API URI Path (optional)");
            path[1].SendKeys($"/api/v1/Tenants/{Settings.OcsTenantId}/Namespaces");

            var timeout = powerBISession.TryFindElementsByName("Timeout (optional)");
            timeout[1].SendKeys("100");

            var ok = powerBISession.TryFindElementByName("OK");
            var signin = powerBISession.TryClickAndFindElementByName(ok, "Sign in");

            // Sign in
            var personalAccount = powerBISession.TryClickAndFindElementsByName(signin, "Personal Account");
            Assert.NotNull(personalAccount);
            personalAccount[1].Click();
            var email = powerBISession.TryFindElementByAccessibilityId("i0116", 15);
            if (email == null)
            {
                // Try going back and choosing "Use another account"
                var back = powerBISession.TryFindElementByAccessibilityId("idBtn_Back");
                var otherAccount = powerBISession.TryClickAndFindElementByName(back, "Use another account");
                email = powerBISession.TryClickAndFindElementByAccessibilityId(otherAccount, "i0116");
            }

            email.SendKeys(Settings.Login);

            var next = powerBISession.TryFindElementByAccessibilityId("idSIButton9");
            var pwd = powerBISession.TryClickAndFindElementByAccessibilityId(next, "i0118");
            pwd.SendKeys(Settings.Password);

            signin = powerBISession.TryFindElementByAccessibilityId("idSIButton9");
            connect = powerBISession.TryClickAndFindElementByName(signin, "Connect");
            connect.Click();

            // Find Power Query Editor window
            var queryEditorWindow = desktopSession.TryFindElementByName("Untitled - Power Query Editor");
            var queryEditorWindowHandle = queryEditorWindow.GetAttribute("NativeWindowHandle");
            queryEditorWindowHandle = int.Parse(queryEditorWindowHandle, CultureInfo.InvariantCulture)
                .ToString("x", CultureInfo.InvariantCulture); // Convert to Hex

            var queryEditorOptions = new AppiumOptions();
            queryEditorOptions.AddAdditionalCapability("appTopLevelWindow", queryEditorWindowHandle);
            using var queryEditorSession = new WindowsDriver<WindowsElement>(appiumUri, queryEditorOptions);

            // Verify results
            var record = queryEditorSession.TryFindElementByName("Record");
            var self = queryEditorSession.TryClickAndFindElementByName(record, "Self");
            Assert.NotNull(self);
        }
    }
}
