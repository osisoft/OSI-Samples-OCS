using System;
using OSIsoft.Data;

namespace SdsTsDotNet
{
    #region step2a
    public class TimeData
    {
        [SdsMember(IsKey = true)]
        public DateTime Time { get; set; }

        public double Value { get; set; }
    }
    #endregion
}
