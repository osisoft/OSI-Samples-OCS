using System;
using System.Globalization;
using System.IO;
using Newtonsoft.Json;
using OpenQA.Selenium;
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

            // Start inspect.exe
            var appiumUri = new Uri("http://127.0.0.1:4723");
            var inspectOptions = new AppiumOptions();
            inspectOptions.AddAdditionalCapability("app", @"C:\Program Files (x86)\Windows Kits\10\bin\x86\inspect.exe");
            using var inspectSession = new WindowsDriver<WindowsElement>(appiumUri, inspectOptions);

            // Start Power BI
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

            // Close Start window
            var startWindow = powerBISession.TryFindElementByAccessibilityId("KoStartDialog", 10);
            if (startWindow != null)
            {
                var closeStart = startWindow.FindElementByName("Close");
                closeStart.Click();
            }

            // Clear cached credentials
            var queries = powerBISession.TryFindElementByName("Queries");
            var transformData = queries.TryFindElementsByName("Transform data");
            var dataSourceSettings = powerBISession.TryClickAndFindElementByName(transformData[2], "Data source settings");
            var dataSourceSettingsDialog = powerBISession.TryClickAndFindElementByAccessibilityId(dataSourceSettings, "ManageDataSourcesDialog");
            var clearPermissions = dataSourceSettingsDialog.TryFindElementsByName("Clear Permissions");
            var clearPermissionsDialog = dataSourceSettingsDialog.TryClickAndFindElementByAccessibilityId(clearPermissions[1], "MessageDialog", 10);
            if (clearPermissionsDialog != null)
            {
                var delete = clearPermissionsDialog.TryFindElementsByName("Delete");
                delete[1].Click();
            }

            var close = dataSourceSettingsDialog.TryFindElementByName("Close");
            close.Click();

            // Open OCS Connector
            var getData = powerBISession.TryFindElementByName("Get data");
            var getDataWindow = powerBISession.TryClickAndFindElementByAccessibilityId(getData, "DataSourceGalleryDialog");
            var search = getDataWindow.FindElementByName("Search");
            search.SendKeys("OSI");

            var sample = getDataWindow.TryFindElementByName("OSIsoft Cloud Services Sample (Beta)");
            var connect = getDataWindow.TryClickAndFindElementByName(sample, "Connect");

            // Enter query info
            var builderDialog = powerBISession.TryClickAndFindElementByAccessibilityId(connect, "BuilderDialog");
            var uri = builderDialog.TryFindElementsByName("OSIsoft Cloud Services API Path");
            uri[1].SendKeys($"{Settings.OcsAddress}/api/v1/Tenants/{Settings.OcsTenantId}/Namespaces");

            var timeout = builderDialog.TryFindElementsByName("Timeout (optional)");
            timeout[1].SendKeys("100");

            var ok = builderDialog.TryFindElementByName("OK");
            var signin = builderDialog.TryClickAndFindElementByName(ok, "Sign in");

            // Sign in
            var oauthDialog = powerBISession.TryClickAndFindElementByAccessibilityId(signin, "OAuthDialog");
            var personalAccount = oauthDialog.TryFindElementsByName("Personal Account");
            Assert.NotNull(personalAccount);
            personalAccount[1].Click();
            var email = oauthDialog.TryFindElementByAccessibilityId("i0116", 10);
            if (email == null)
            {
                // Try going back and choosing "Use another account"
                var back = oauthDialog.TryFindElementByAccessibilityId("idBtn_Back");
                back.Click();
                var otherAccount = oauthDialog.TryFindElementByName("Use another account");
                otherAccount.Click();
                email = oauthDialog.TryFindElementByAccessibilityId("i0116");
            }

            email.SendKeys(Settings.Login);

            var next = oauthDialog.TryFindElementByAccessibilityId("idSIButton9");
            next.Click();
            var pwd = oauthDialog.TryFindElementByAccessibilityId("i0118");
            pwd.SendKeys(Settings.Password);
            pwd.SendKeys(Keys.Enter);

            builderDialog = powerBISession.TryClickAndFindElementByAccessibilityId(connect, "BuilderDialog");
            connect = builderDialog.TryFindElementByName("Connect");
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
