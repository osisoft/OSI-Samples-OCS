using System;
using OSIsoft.Data;

namespace UomsSample
{
    public class Widget
    {
        [SdsMember(IsKey = true)]
        public DateTime Time { get; set; }

        [SdsMember(Uom = "degree Fahrenheit")]
        public double Temperature { get; set; }

        [SdsMember(Uom = "mile")]
        public double Distance { get; set; }
    }
}
