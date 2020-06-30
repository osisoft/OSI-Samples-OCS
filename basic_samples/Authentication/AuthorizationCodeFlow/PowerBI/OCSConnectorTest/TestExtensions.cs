using System;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using Appium.Interfaces.Generic.SearchContext;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium.Interfaces;

namespace OCSConnectorTest
{
    public static class TestExtensions
    {
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Catch intended for retry logic")]
        public static T TryFindElementByName<T>(this IGenericFindsByName<T> element, string name, int seconds = 30) where T : IWebElement
        {
            if (element == null)
            {
                throw new ArgumentNullException(nameof(element));
            }

            Stopwatch sw = Stopwatch.StartNew();
            while (sw.Elapsed < TimeSpan.FromSeconds(seconds))
            {
                try
                {
                    var result = element.FindElementByName(name);
                    if (result != null) return result;
                }
                catch { }
            }

            Console.WriteLine($"TryFindElementByName: Failed to find element \"{name}\"");
            TakeScreenshot();
            return default;
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Catch intended for retry logic")]
        public static T TryClickAndFindElementByName<T>(this IGenericFindsByName<T> element, IWebElement button, string name, int seconds = 30) where T : IWebElement
        {
            if (element == null)
            {
                throw new ArgumentNullException(nameof(element));
            }

            if (button == null)
            {
                throw new ArgumentNullException(nameof(button));
            }

            Stopwatch sw = Stopwatch.StartNew();
            while (sw.Elapsed < TimeSpan.FromSeconds(seconds))
            {
                try
                {
                    button.Click();
                }
                catch { }

                try
                {
                    var result = element.FindElementByName(name);
                    if (result != null) return result;
                }
                catch { }
            }

            Console.WriteLine($"TryClickAndFindElementByName: Failed to find element \"{name}\"");
            TakeScreenshot();
            return default;
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Catch intended for retry logic")]
        public static T TryFindElementByAccessibilityId<T>(this IFindByAccessibilityId<T> element, string selector, int seconds = 30) where T : IWebElement
        {
            if (element == null)
            {
                throw new ArgumentNullException(nameof(element));
            }

            Stopwatch sw = Stopwatch.StartNew();
            while (sw.Elapsed < TimeSpan.FromSeconds(seconds))
            {
                try
                {
                    var result = element.FindElementByAccessibilityId(selector);
                    if (result != null) return result;
                }
                catch { }
            }

            Console.WriteLine($"TryFindElementByAccessibilityId: Failed to find element \"{selector}\"");
            TakeScreenshot();
            return default;
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Catch intended for retry logic")]
        public static T TryClickAndFindElementByAccessibilityId<T>(this IFindByAccessibilityId<T> element, IWebElement button, string selector, int seconds = 30) where T : IWebElement
        {
            if (element == null)
            {
                throw new ArgumentNullException(nameof(element));
            }

            if (button == null)
            {
                throw new ArgumentNullException(nameof(button));
            }

            Stopwatch sw = Stopwatch.StartNew();
            while (sw.Elapsed < TimeSpan.FromSeconds(seconds))
            {
                try
                {
                    button.Click();
                }
                catch { }

                try
                {
                    var result = element.FindElementByAccessibilityId(selector);
                    if (result != null) return result;
                }
                catch { }
            }

            Console.WriteLine($"TryClickAndFindElementByAccessibilityId: Failed to find element \"{selector}\"");
            TakeScreenshot();
            return default;
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Catch intended for retry logic")]
        public static ReadOnlyCollection<T> TryFindElementsByName<T>(this IGenericFindsByName<T> element, string name, int seconds = 30) where T : IWebElement
        {
            if (element == null)
            {
                throw new ArgumentNullException(nameof(element));
            }

            Stopwatch sw = Stopwatch.StartNew();
            while (sw.Elapsed < TimeSpan.FromSeconds(seconds))
            {
                try
                {
                    var result = element.FindElementsByName(name);
                    if (result != null && result.Count > 0) return result;
                }
                catch { }
            }

            Console.WriteLine($"TryFindElementsByName: Failed to find element \"{name}\"");
            TakeScreenshot();
            return default;
        }

        [System.Diagnostics.CodeAnalysis.SuppressMessage("Design", "CA1031:Do not catch general exception types", Justification = "Catch intended for retry logic")]
        public static ReadOnlyCollection<T> TryClickAndFindElementsByName<T>(this IGenericFindsByName<T> element, IWebElement button, string name, int seconds = 30) where T : IWebElement
        {
            if (element == null)
            {
                throw new ArgumentNullException(nameof(element));
            }

            if (button == null)
            {
                throw new ArgumentNullException(nameof(button));
            }

            Stopwatch sw = Stopwatch.StartNew();
            while (sw.Elapsed < TimeSpan.FromSeconds(seconds))
            {
                try
                {
                    button.Click();
                }
                catch { }

                try
                {
                    var result = element.FindElementsByName(name);
                    if (result != null && result.Count > 0) return result;
                }
                catch { }
            }

            Console.WriteLine($"TryClickAndFindElementsByName: Failed to find element \"{name}\"");
            TakeScreenshot();
            return default;
        }

        public static void TakeScreenshot()
        {
            using var captureBmp = new Bitmap(1920, 1024, PixelFormat.Format32bppArgb);
            using var captureGraphic = Graphics.FromImage(captureBmp);
            captureGraphic.CopyFromScreen(0, 0, 0, 0, captureBmp.Size);
            captureBmp.Save("capture.jpg", ImageFormat.Jpeg);
        }
    }
}
