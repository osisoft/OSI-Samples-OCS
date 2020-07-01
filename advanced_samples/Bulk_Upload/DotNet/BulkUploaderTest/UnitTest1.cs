using Bulk_Uploader;
using Newtonsoft.Json;
using OSIsoft.Data;
using OSIsoft.DataViews;
using System;
using System.Collections.Generic;
using System.IO;
using Xunit;
using Xunit.Abstractions;

namespace BulkUploaderTest
{
    public class UnitTest1
    {
        public static Exception toThrow = null;
        public static bool success = true;
        [Fact]
        public void Test1()           
        {

            try
            {
                _ = Program.MainAsync().Result;
            }
            catch (Exception ex)
            {
                LogError(ex);
            }

            Cleanup();
            if (!success)
                throw toThrow;
        }

        private void Cleanup()
        {
            if (!String.IsNullOrEmpty(Program.dataviewPath))
            {
                DeleteDataView();
            }

            if (!String.IsNullOrEmpty(Program.sdsStreamPath))
            {
                DeleteStreams();
            }

            if (!String.IsNullOrEmpty(Program.sdsTypePath))
            {
                DeleteTypes();
            }
        }


        private static void DeleteDataView()
        {
            Console.WriteLine($"Deleting Dataviews");
            string dataviewS = File.ReadAllText(Program.dataviewPath);
            List<DataView> dataviews = JsonConvert.DeserializeObject<List<DataView>>(dataviewS);
            foreach (var dataview in dataviews)
            {
                try
                {
                    Program.dvService.DeleteDataViewAsync(dataview.Id).Wait();
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
            if (success)
            {
                success = false;
                toThrow = ex;
            }
        }

        private static void DeleteTypes()
        {
            Console.WriteLine($"Deleting Types");
            string types = File.ReadAllText(Program.sdsTypePath);
            List<SdsType> typeList = JsonConvert.DeserializeObject<List<SdsType>>(types);
            foreach (var type in typeList)
            {
                try
                { 
                    Program.metadataService.DeleteTypeAsync(type.Id).Wait();
                }
                catch (Exception ex)
                {
                    Console.Write(ex); // not causing test to error because it is common that a type might exist on for other types
                    //LogError(ex);
                }
            }
        }

        private static void DeleteStreams()
        {
            Console.WriteLine($"Deleting streams");
            string streams = File.ReadAllText(Program.sdsStreamPath);
            var streamsList = JsonConvert.DeserializeObject<List<SdsStream>>(streams);
            foreach (var stream in streamsList)
            {
                try 
                {                 
                    Program.metadataService.DeleteStreamAsync(stream.Id).Wait();
                }
                catch (Exception ex)
                {
                    LogError(ex);
                }
            }
        }
    }
}
