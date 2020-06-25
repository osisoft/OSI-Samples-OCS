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
            transformData[2].Click();

            var dataSourceSettings = powerBISession.TryFindElementByName("Data source settings");
            dataSourceSettings.Click();

            var clearPermissions = powerBISession.TryFindElementByName("Clear Permissions");
            clearPermissions.Click();

            var delete = powerBISession.TryFindElementByName("Delete", 5);
            if (delete != null)
            {
                delete.Click();
            }

            var close = powerBISession.TryFindElementByName("Close");
            close.Click();

            // Open OCS Connector
            var getData = powerBISession.TryFindElementByName("Get data");
            getData.Click();

            var search = powerBISession.TryFindElementByName("Search");
            search.SendKeys("OSI");

            var sample = powerBISession.TryFindElementByName("OSIsoft Cloud Services Sample (Beta)");
            sample.Click();

            var connect = powerBISession.TryFindElementByName("Connect");
            connect.Click();

            // Enter query info
            var uri = powerBISession.TryFindElementsByName("OSIsoft Cloud Services URI");
            uri[1].SendKeys(Settings.OcsUri.ToString());

            var path = powerBISession.TryFindElementsByName("API URI Path (optional)");
            path[1].SendKeys($"/api/v1/Tenants/{Settings.OcsTenantId}/Namespaces");

            var timeout = powerBISession.TryFindElementsByName("Timeout (optional)");
            timeout[1].SendKeys("100");

            var ok = powerBISession.TryFindElementByName("OK");
            ok.Click();

            // Sign in
            var signin = powerBISession.TryFindElementByName("Sign in");
            signin.Click();

            var personalAccount = powerBISession.TryFindElementByName("Personal Account");
            personalAccount.Click();

            var email = powerBISession.TryFindElementByAccessibilityId("i0116");
            email.SendKeys(Settings.Login);

            var next = powerBISession.TryFindElementByAccessibilityId("idSIButton9");
            next.Click();

            var pwd = powerBISession.TryFindElementByAccessibilityId("i0118");
            pwd.SendKeys(Settings.Password);

            signin = powerBISession.TryFindElementByAccessibilityId("idSIButton9");
            signin.Click();

            connect = powerBISession.TryFindElementByName("Connect");
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
            record.Click();

            var self = queryEditorSession.TryFindElementByName("Self");
            Assert.NotNull(self);
        }
    }
}
