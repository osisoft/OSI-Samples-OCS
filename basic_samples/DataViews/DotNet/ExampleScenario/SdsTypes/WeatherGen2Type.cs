using System;
using OSIsoft.Data;

namespace ExampleScenario.SdsTypes
{
    public class WeatherGen2Type
    {
        [SdsMember(IsKey = true)]
        public DateTime Timestamp { get; set; }

        public int SolarRadiation { get; set; }

        public double AmbientTemperature { get; set; }

        public int CloudCover { get; set; }
    }
}
