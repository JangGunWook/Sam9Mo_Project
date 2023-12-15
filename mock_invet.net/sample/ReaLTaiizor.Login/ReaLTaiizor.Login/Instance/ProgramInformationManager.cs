using System.ComponentModel;

public class ProgramInformationManager
{
    private static ProgramInformationManager _instance;

    public static ProgramInformationManager Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = new ProgramInformationManager();
            }
            return _instance;
        }
    }

    private const string myServerIp = "221.156.60.18";
    private const string myServerPort = "8989";

    public const int MAIN_PAGE = 0;
    public const int MEMBERS_PAGE = 1;
    public const int NEWS_PAGE = 2;
    public const int SUB4_PAGE = 3;
    public const int SUB5_PAGE = 4;
    public const int SUB6_PAGE = 5;
    public const int SUB7_PAGE = 6;

    public string AccessToken { get; set; }
    public string RefreshToken { get; set; }
    [DefaultValue(myServerIp)]
    public string API_SERVER_IP { get; set; } = myServerIp;
    [DefaultValue(myServerPort)]
    public string API_SERVER_PORT { get; set; } = myServerPort;

}