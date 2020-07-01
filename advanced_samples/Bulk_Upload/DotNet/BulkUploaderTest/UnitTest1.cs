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
        [Fact]
        public void Test1()
        {
            var res = Program.MainAsync().Result;
            Cleanup();
            Assert.True(res);

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
                Program.dvService.DeleteDataViewAsync(dataview.Id).Wait();
            }
        }

        private static void DeleteTypes()
        {
            Console.WriteLine($"Deleting Types");
            string types = File.ReadAllText(Program.sdsTypePath);
            List<SdsType> typeList = JsonConvert.DeserializeObject<List<SdsType>>(types);
            foreach (var type in typeList)
            {
                Program.metadataService.DeleteTypeAsync(type.Id).Wait();
            }
        }

        private static void DeleteStreams()
        {
            Console.WriteLine($"Deleting streams");
            string streams = File.ReadAllText(Program.sdsStreamPath);
            var streamsList = JsonConvert.DeserializeObject<List<SdsStream>>(streams);
            foreach (var stream in streamsList)
            {
                Program.metadataService.DeleteStreamAsync(stream.Id).Wait();
            }
        }
    }
}
