using System;
using OSIsoft.Data;

namespace SdsTsDotNet
{
    #region step5a
    public class PressureTemperatureData
    {
        [SdsMember(IsKey = true)]
        public DateTime Time { get; set; }

        public double Pressure { get; set; }
        public double Temperature { get; set; }
    }
    #endregion
}
