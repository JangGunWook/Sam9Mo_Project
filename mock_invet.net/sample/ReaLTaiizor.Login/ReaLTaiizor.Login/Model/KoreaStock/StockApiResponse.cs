using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

public partial class StockApiResponse
{
    [JsonPropertyName("initial")]
    public InitialProperty Initial;

    [JsonPropertyName("current_trade")]
    public CurrentTrade Current_trade { get; set; }

}
