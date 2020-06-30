using System;
using OSIsoft.Data;

namespace ExampleScenario.SdsTypes
{
    public class InverterType
    {
        [SdsMember(IsKey = true)]
        public DateTime Timestamp { get; set; }

        public double Value { get; set; }
    }
}
