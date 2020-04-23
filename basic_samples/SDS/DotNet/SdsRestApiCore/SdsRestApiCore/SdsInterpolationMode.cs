namespace SdsRestApiCore
{
    public enum SdsInterpolationMode
    {
        Default = Continuous,
        Continuous = 0,
        StepwiseContinuousLeading = 1,
        StepwiseContinuousTrailing = 2,
        Discrete = 3,
    }
}
