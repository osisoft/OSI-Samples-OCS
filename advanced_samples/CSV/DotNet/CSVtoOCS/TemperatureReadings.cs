using System;
using OSIsoft.Data;

namespace CSVtoOCS
{
    public class TemperatureReadings
    {
        public TemperatureReadings()
        {
        }

        public TemperatureReadings(TemperatureReadingsWithIds tempReading)
        {
            if (tempReading == null)
            {
                throw new ArgumentNullException(nameof(tempReading));
            }

            Timestamp = tempReading.Timestamp;
            Temperature1 = tempReading.Temperature1;
            Temperature2 = tempReading.Temperature2;
            Code = tempReading.Code;
        }

        [SdsMember(IsKey = true)]
        public DateTime Timestamp { get; set; }
        public int Temperature1 { get; set; }
        public double Temperature2 { get; set; }
        public string Code { get; set; }
    }
}
