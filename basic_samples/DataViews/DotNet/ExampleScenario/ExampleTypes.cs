using System.Collections.Generic;
using ExampleScenario.SdsTypes;
using OSIsoft.Data;
using OSIsoft.Data.Reflection;

namespace ExampleScenario
{
    public static class ExampleTypes
    {
        public const string InverterType = "docs-pi-inverter";
        public const string WeatherGen1Type = "docs-omf-weather-gen1";
        public const string WeatherGen2Type = "docs-omf-weather-gen2";

        public static List<SdsType> GetExampleTypes()
            => new List<SdsType>
            {
                GetInverterType(),
                GetWeatherGen1Type(),
                GetWeatherGen2Type(),
            };

        private static SdsType GetInverterType()
        {
            SdsType type = SdsTypeBuilder.CreateSdsType<InverterType>();
            type.Id = InverterType;
            type.Name = "Inverter";

            return type;
        }

        private static SdsType GetWeatherGen1Type()
        {
            SdsType type = SdsTypeBuilder.CreateSdsType<WeatherGen1Type>();
            type.Id = WeatherGen1Type;
            type.Name = "WeatherGen1";

            return type;
        }

        private static SdsType GetWeatherGen2Type()
        {
            SdsType type = SdsTypeBuilder.CreateSdsType<WeatherGen2Type>();
            type.Id = WeatherGen2Type;
            type.Name = "WeatherGen2";

            return type;
        }
    }
}
