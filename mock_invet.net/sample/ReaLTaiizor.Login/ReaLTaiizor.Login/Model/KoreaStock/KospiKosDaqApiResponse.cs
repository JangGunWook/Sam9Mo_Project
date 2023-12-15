using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public partial class KospiKosDaqApiResponse
    {
        [JsonPropertyName("date")]
        public string date { get; set; }

        [JsonPropertyName("data")]
        public List<Data> data { get; set; }
}

public class Data
{
    private int? _timestamp;
    private double? _close;
    private double? _high;
    private double? _low;
    private double? _open;

    [JsonPropertyName("timestamp")]
    public int? timestamp  {
        get { return _timestamp; }
        set
        {
            _timestamp = value;
            if (_timestamp.HasValue)
            {
                DateTime = DateTimeOffset.FromUnixTimeSeconds(_timestamp.Value).ToOffset(TimeSpan.FromHours(9)).DateTime;
            }
        }
    }
    public DateTime? DateTime { get; set; }

    [JsonPropertyName("close")]
    public double? Close
    {
        get { return _close; }
        set
        {
            _close = value;
            if (_close.HasValue)
            {
                CloseInt = Convert.ToInt32(_close.Value);
            }
        }
    }
    public int? CloseInt { get; set; }
    [JsonPropertyName("high")]
    public double? high
    {
        get { return _high; }
        set
        {
            _high = value;
            if (_high.HasValue)
            {
                HighInt = Convert.ToInt32(_high.Value);
            }
        }
    }
    public int? HighInt { get; set; }

    [JsonPropertyName("volume")]
    public int? volume { get; set; }

    [JsonPropertyName("low")]
    public double? low {
        get { return _low; }
        set
        {
            _low = value;
            if (_low.HasValue)
            {
                LowInt = Convert.ToInt32(_low.Value);
            }
        }
    }
    public int? LowInt { get; set; }

    [JsonPropertyName("open")]
    public double? open
    {
        get { return _open; }
        set
        {
            _open = value;
            if (_open.HasValue)
            {
                OpenInt = Convert.ToInt32(_open.Value);
            }
        }
    }
    public int? OpenInt { get; set; }
}