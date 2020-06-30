using System;
using System.Collections.Generic;
using OSIsoft.Data;

namespace ExampleScenario
{
    public static class ExampleStreams
    {
        private const string WSBILT = "WS_BILT";
        private const string WSROSE = "WS_ROSE";
        private const string WSWINT = "WS_WINT";

        private const string SiteMetadata = "Site";
        private const string MeasurementMetadata = "Measurement";
        private const string MeterMetadata = "Meter";
        private const string InverterMetadata = "Inverter";
        private const string NominalPowerMetadata = "Nominal Power MW";

        public static List<SdsStream> GetExampleStreams()
            => new List<SdsStream>
            {
                GetInverterStream("BILT.Meter.Primary.Inverter.0.PwrIn"),
                GetInverterStream("BILT.Meter.Primary.Inverter.0.PwrOut"),
                GetInverterStream("BILT.Meter.Primary.Inverter.1.PwrIn"),
                GetInverterStream("BILT.Meter.Primary.Inverter.1.PwrOut"),
                GetInverterStream("BILT.Meter.Primary.Inverter.2.PwrIn"),
                GetInverterStream("BILT.Meter.Primary.Inverter.2.PwrOut"),
                GetInverterStream("BILT.Meter.Secondary.Inverter.0.PwrIn"),
                GetInverterStream("BILT.Meter.Secondary.Inverter.0.PwrOut"),
                GetInverterStream("ROSE.Meter.Primary.Inverter.0.PwrIn"),
                GetInverterStream("ROSE.Meter.Primary.Inverter.0.PwrOut"),
                GetInverterStream("ROSE.Meter.Primary.Inverter.1.PwrIn"),
                GetInverterStream("ROSE.Meter.Primary.Inverter.1.PwrOut"),
                GetInverterStream("WINT.Meter.Primary.Inverter.0.PwrIn"),
                GetInverterStream("WINT.Meter.Primary.Inverter.0.PwrOut"),
                GetInverterStream("WINT.Meter.Secondary.Inverter.0.PwrIn"),
                GetInverterStream("WINT.Meter.Secondary.Inverter.0.PwrOut"),
                GetWeatherGen1Stream(WSBILT),
                GetWeatherGen1Stream(WSROSE),
                GetWeatherGen2Stream(WSWINT),
            };

        public static Dictionary<string, string> GetMetadata(SdsStream stream)
        {
            switch (stream?.TypeId)
            {
                case ExampleTypes.InverterType:
                    return GetInverterMetadata(stream.Id);
                case ExampleTypes.WeatherGen1Type:
                case ExampleTypes.WeatherGen2Type:
                    return GetWeatherStationMetadata(stream.Id);
                default:
                    return null;
            }
        }

        public static List<string> GetTags(string id)
            => id switch
            {
                WSBILT => new List<string> { "Weather", "High Resolution", "Gen1" },
                WSROSE => new List<string> { "Weather", "Low Resolution", "Gen1" },
                WSWINT => new List<string> { "Weather", "High Resolution", "Gen2" },
                _ => GetInverterTag(),
            };

        private static SdsStream GetInverterStream(string id)
            => GetStream(id, "docs-pi-inverter");

        private static SdsStream GetWeatherGen1Stream(string id)
            => GetStream(id, "docs-omf-weather-gen1");

        private static SdsStream GetWeatherGen2Stream(string id)
            => GetStream(id, "docs-omf-weather-gen2");

        private static SdsStream GetStream(string id, string typeId)
            => new SdsStream()
            {
                Id = id,
                TypeId = typeId,
            };

        private static Dictionary<string, string> GetInverterMetadata(string id)
            => new Dictionary<string, string>
            {
                { SiteMetadata, GetSiteFromStreamId(id) },
                { MeasurementMetadata, GetMeasurementFromStreamId(id) },
                { MeterMetadata, GetMeterFromStreamId(id) },
                { InverterMetadata, GetInverterFromStreamId(id) },
                { NominalPowerMetadata, "1.21" },
            };

        private static Dictionary<string, string> GetWeatherStationMetadata(string id)
            => new Dictionary<string, string>
            {
                { SiteMetadata, GetSiteFromStreamId(id) },
            };

        private static string GetSiteFromStreamId(string id)
        {
            if (id.Contains("BILT", StringComparison.Ordinal))
            {
                return "Biltmore";
            }
            else if (id.Contains("ROSE", StringComparison.Ordinal))
            {
                return "Rosecliff";
            }
            else if (id.Contains("WINT", StringComparison.Ordinal))
            {
                return "Winterthur";
            }
            else
            {
                return null;
            }
        }

        private static string GetMeasurementFromStreamId(string id)
        {
            if (id.Contains("PwrIn", StringComparison.Ordinal))
            {
                return "Power In";
            }
            else if (id.Contains("PwrOut", StringComparison.Ordinal))
            {
                return "Power Out";
            }
            else
            {
                return null;
            }
        }

        private static string GetMeterFromStreamId(string id)
        {
            if (id.Contains("Primary", StringComparison.Ordinal))
            {
                return "Primary";
            }
            else if (id.Contains("Secondary", StringComparison.Ordinal))
            {
                return "Secondary";
            }
            else
            {
                return null;
            }
        }

        private static string GetInverterFromStreamId(string id)
        {
            if (id.Contains("0", StringComparison.Ordinal))
            {
                return "0";
            }
            else if (id.Contains("1", StringComparison.Ordinal))
            {
                return "1";
            }
            else if (id.Contains("2", StringComparison.Ordinal))
            {
                return "2";
            }
            else
            {
                return null;
            }
        }

        private static List<string> GetInverterTag()
        {
            Random random = new Random();
            int type = random.Next(0, 2);

            if (type == 0)
            {
                return new List<string> { "Commercial" };
            }
            else if (type == 1)
            {
                return new List<string> { "Residential" };
            }
            else if (type == 2)
            {
                return new List<string> { "Critical Asset" };
            }
            else
            {
                return null;
            }
        }
    }
}
