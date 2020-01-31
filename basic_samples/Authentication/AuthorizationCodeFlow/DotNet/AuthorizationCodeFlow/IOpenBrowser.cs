namespace AuthorizationCodeFlow
{
    public interface IOpenBrowser
    {
        void OpenBrowser(string url, string userName, string password);
    }
}
