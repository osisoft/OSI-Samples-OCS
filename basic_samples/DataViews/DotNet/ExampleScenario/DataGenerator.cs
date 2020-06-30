using System;
using System.Collections.Generic;
using ExampleScenario.SdsTypes;

namespace ExampleScenario
{
    public class DataGenerator
    {
        private readonly Random _random;
        private readonly DateTime _start;
        private readonly TimeSpan _interval;
        private readonly int _count;

        public DataGenerator()
        {
            _random = new Random();
            _start = DateTime.UtcNow.AddDays(-1);
            _interval = TimeSpan.FromHours(1);
            _count = 24;
        }

        public List<InverterType> GetInverterValues()
            => GetValues(GetInverterValue);

        public List<WeatherGen1Type> GetWeatherGen1Values()
            => GetValues(GetWeatherGen1Value);

        public List<WeatherGen2Type> GetWeatherGen2Values()
            => GetValues(GetWeatherGen2Value);

        private List<T> GetValues<T>(Func<DateTime, T> randomValGenerator)
        {
            List<T> values = new List<T>();
            DateTime time = _start;

            for (int i = 0; i < _count; i++)
            {
                T value = randomValGenerator(time);

                values.Add(value);
                time += _interval;
            }

            return values;
        }

        private InverterType GetInverterValue(DateTime time)
            => new InverterType()
            {
                Timestamp = time,
                Value = GetRandomDouble(),
            };

        private WeatherGen1Type GetWeatherGen1Value(DateTime time)
            => new WeatherGen1Type()
            {
                Timestamp = time,
                SolarRadiation = GetRandomInt(),
                Temperature = GetRandomDouble(),
            };

        private WeatherGen2Type GetWeatherGen2Value(DateTime time)
            => new WeatherGen2Type()
            {
                Timestamp = time,
                SolarRadiation = GetRandomInt(),
                AmbientTemperature = GetRandomDouble(),
                CloudCover = GetRandomInt(),
            };

        private double GetRandomDouble()
            => _random.NextDouble() * 100;

        private int GetRandomInt()
            => _random.Next(int.MaxValue);
    }
}
