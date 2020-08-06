using System;
using System.Collections.Generic;
using System.IO;
using BulkUploader;
using Newtonsoft.Json;
using OSIsoft.Data;
using OSIsoft.DataViews;
using Xunit;
using Xunit.Abstractions;

namespace BulkUploaderTest
{
    public class UnitTest1
    {
        private static Exception _toThrow = null;

        [Fact]
        public void Test1()
        {
            try
            {
                Program.MainRunner();
            }
            catch (Exception ex)
            {
                LogError(ex);
            }

            Program.Cleanup();
            LogError(Program.ToThrow);

            if (_toThrow != null)
                throw _toThrow;
        }

        private static void LogError(Exception ex)
        {
            if (ex == null)
                return;

            Console.Write(ex);
            if (_toThrow != null)
            {
                _toThrow = ex;
            }
        }

    }
}
