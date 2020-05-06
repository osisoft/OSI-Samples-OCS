using System.Text;
using OSIsoft.Data;

namespace SdsClientLibraries
{
    public class WaveData
    {
        [SdsMember(IsKey = true)]
        public int Order { get; set; }

        public double Tau { get; set; }

        public double Radians { get; set; }

        public double Sin { get; set; }

        public double Cos { get; set; }

        public double Tan { get; set; }

        public double Sinh { get; set; }

        public double Cosh { get; set; }

        public double Tanh { get; set; }

        public override string ToString()
        {
            var builder = new StringBuilder();
            builder.Append($"Order: {Order}");
            builder.Append($", Radians: {Radians}");
            builder.Append($", Tau: {Tau}");
            builder.Append($", Sin: {Sin}");
            builder.Append($", Cos: {Cos}");
            builder.Append($", Tan: {Tan}");
            builder.Append($", Sinh: {Sinh}");
            builder.Append($", Cosh: {Cosh}");
            builder.Append($", Tanh: {Tanh}");
            return builder.ToString();
        }
    }
}
