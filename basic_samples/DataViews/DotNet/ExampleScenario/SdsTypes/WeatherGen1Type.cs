using System;
using OSIsoft.Data;

namespace ExampleScenario.SdsTypes
{
    public class WeatherGen1Type
    {
        [SdsMember(IsKey = true)]
        public DateTime Timestamp { get; set; }

        public int SolarRadiation { get; set; }

        public double Temperature { get; set; }
    }
}
