namespace AuthorizationCodeFlow
{
    public interface IOpenBrowser
    {
        void OpenBrowser(string address, string userName, string password);
    }
}
