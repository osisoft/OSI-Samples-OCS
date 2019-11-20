using NUnit.Framework;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System;
using System.IO;
using Microsoft.Extensions.Configuration;

namespace ImplicitFlowTest
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
            IConfigurationBuilder builder = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json");
            IConfiguration configuration = builder.Build();

            AutoLogin(configuration["url"], configuration["userName"], configuration["password"]);
        }


        private static void AutoLogin(string url, string userName, string password)
        {
            // Automatic login works against Microsoft personal account option only
            // Must use Live account email that isn't also an AAD account
            // Account must have no 2FA enabled and the login flow must not have any other additional prompts after password entry
            using (IWebDriver driver = new ChromeDriver(Environment.ExpandEnvironmentVariables("%ChromeWebDriver%")))
            {
                driver.Url = url;
                int sleep = 6000;

                Thread.Sleep(sleep);
                driver.FindElement(By.XPath("//*[@id=\"login\"]")).Click();

                Thread.Sleep(sleep);

                driver.FindElement(By.XPath("descendant::a[@title=\"Personal Account\"]")).Click();

                Thread.Sleep(sleep);

                driver.FindElement(By.XPath("//*[@id=\"i0116\"]")).SendKeys(userName);
                driver.FindElement(By.XPath("//*[@id=\"idSIButton9\"]")).Click();

                Thread.Sleep(sleep);

                driver.FindElement(By.XPath("//*[@id=\"i0118\"]")).SendKeys(password);
                driver.FindElement(By.XPath("//*[@id=\"idSIButton9\"]")).Click();

                Thread.Sleep(sleep);

                driver.FindElement(By.XPath("//*[@id=\"users\"]")).Click();
                Thread.Sleep(sleep);

                var results = driver.FindElement(By.XPath("//*[@id=\"results\"]")).Text;

                if (results.Contains("not logged"))
                    throw new Exception("Logging in failed");

                driver.Close();
            }
        }
    }
}