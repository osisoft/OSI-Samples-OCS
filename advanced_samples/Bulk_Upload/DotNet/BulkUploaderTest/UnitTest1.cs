using System;
using System.Collections.Generic;
using System.IO;
using Bulk_Uploader;
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

            Cleanup();
            if (_toThrow != null)
                throw _toThrow;
        }

        private void Cleanup()
        {
            if (!string.IsNullOrEmpty(Program.DataviewPath))
            {
                DeleteDataView();
            }

            if (!string.IsNullOrEmpty(Program.SdsStreamPath))
            {
                DeleteStreams();
            }

            if (!string.IsNullOrEmpty(Program.SdsTypePath))
            {
                DeleteTypes();
            }
        }


        private static void DeleteDataView()
        {
            Console.WriteLine($"Deleting Dataviews");
            string dataviewS = File.ReadAllText(Program.DataviewPath);
            List<DataView> dataviews = JsonConvert.DeserializeObject<List<DataView>>(dataviewS);
            foreach (var dataview in dataviews)
            {
                try
                {
                    Program.DvService.DeleteDataViewAsync(dataview.Id).Wait();
                }
                catch (Exception ex)
                {
                    LogError(ex);
                }

            }
        }

        private static void LogError(Exception ex)
        {
            Console.Write(ex);
            if (_toThrow != null)
            {
                _toThrow = ex;
            }
        }

        private static void DeleteTypes()
        {
            Console.WriteLine($"Deleting Types");
            string types = File.ReadAllText(Program.SdsTypePath);
            List<SdsType> typeList = JsonConvert.DeserializeObject<List<SdsType>>(types);
            foreach (var type in typeList)
            {
                try
                { 
                    Program.MetadataService.DeleteTypeAsync(type.Id).Wait();
                }
                catch (Exception ex)
                {
                    Console.Write(ex);

                    // Note: For delete of type we are not causing the test to error if it failes because it is common that a type might exist on for other streams.  If you want to make sure it delete uncomment the line below.

                    // LogError(ex);
                }
            }
        }

        private static void DeleteStreams()
        {
            Console.WriteLine($"Deleting streams");
            string streams = File.ReadAllText(Program.SdsStreamPath);
            var streamsList = JsonConvert.DeserializeObject<List<SdsStream>>(streams);
            foreach (var stream in streamsList)
            {
                try 
                {                 
                    Program.MetadataService.DeleteStreamAsync(stream.Id).Wait();
                }
                catch (Exception ex)
                {
                    LogError(ex);
                }
            }
        }
    }
}
