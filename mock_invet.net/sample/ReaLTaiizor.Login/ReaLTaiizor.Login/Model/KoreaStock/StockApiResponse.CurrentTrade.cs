using System.Text.Json.Serialization;

public partial class StockApiResponse
{
    public class CurrentTrade
    {
        [JsonPropertyName("MKSC_SHRN_ISCD")]
        public string MKSC_SHRN_ISCD { get; set; }

        [JsonPropertyName("STCK_CNTG_HOUR")]
        public string STCK_CNTG_HOUR { get; set; }

        [JsonPropertyName("STCK_PRPR")]
        public string STCK_PRPR { get; set; }

        [JsonPropertyName("PRDY_VRSS_SIGN")]
        public string PRDY_VRSS_SIGN { get; set; }

        [JsonPropertyName("PRDY_VRSS")]
        public string PRDY_VRSS { get; set; }

        [JsonPropertyName("PRDY_CTRT")]
        public string PRDY_CTRT { get; set; }

        [JsonPropertyName("WGHN_AVRG_STCK_PRC")]
        public string WGHN_AVRG_STCK_PRC { get; set; }

        [JsonPropertyName("STCK_OPRC")]
        public string STCK_OPRC { get; set; }

        [JsonPropertyName("STCK_HGPR")]
        public string STCK_HGPR { get; set; }

        [JsonPropertyName("STCK_LWPR")]
        public string STCK_LWPR { get; set; }

        [JsonPropertyName("ASKP1")]
        public string ASKP1 { get; set; }

        [JsonPropertyName("BIDP1")]
        public string BIDP1 { get; set; }

        [JsonPropertyName("CNTG_VOL")]
        public string CNTG_VOL { get; set; }

        [JsonPropertyName("ACML_VOL")]
        public string ACML_VOL { get; set; }

        [JsonPropertyName("ACML_TR_PBMN")]
        public string ACML_TR_PBMN { get; set; }

        [JsonPropertyName("SELN_CNTG_CSNU")]
        public string SELN_CNTG_CSNU { get; set; }

        [JsonPropertyName("SHNU_CNTG_CSNU")]
        public string SHNU_CNTG_CSNU { get; set; }

        [JsonPropertyName("NTBY_CNTG_CSNU")]
        public string NTBY_CNTG_CSNU { get; set; }

        [JsonPropertyName("CTTR")]
        public string CTTR { get; set; }

        [JsonPropertyName("SELN_CNTG_SMTN")]
        public string SELN_CNTG_SMTN { get; set; }

        [JsonPropertyName("SHNU_CNTG_SMTN")]
        public string SHNU_CNTG_SMTN { get; set; }

        [JsonPropertyName("CCLD_DVSN")]
        public string CCLD_DVSN { get; set; }

        [JsonPropertyName("SHNU_RATE")]
        public string SHNU_RATE { get; set; }

        [JsonPropertyName("PRDY_VOL_VRSS_ACML_VOL_RATE")]
        public string PRDY_VOL_VRSS_ACML_VOL_RATE { get; set; }

        [JsonPropertyName("OPRC_HOUR")]
        public string OPRC_HOUR { get; set; }

        [JsonPropertyName("OPRC_VRSS_PRPR_SIGN")]
        public string OPRC_VRSS_PRPR_SIGN { get; set; }

        [JsonPropertyName("OPRC_VRSS_PRPR")]
        public string OPRC_VRSS_PRPR { get; set; }

        [JsonPropertyName("HGPR_HOUR")]
        public string HGPR_HOUR { get; set; }

        [JsonPropertyName("HGPR_VRSS_PRPR_SIGN")]
        public string HGPR_VRSS_PRPR_SIGN { get; set; }

        [JsonPropertyName("HGPR_VRSS_PRPR")]
        public string HGPR_VRSS_PRPR { get; set; }

        [JsonPropertyName("LWPR_HOUR")]
        public string LWPR_HOUR { get; set; }

        [JsonPropertyName("LWPR_VRSS_PRPR_SIGN")]
        public string LWPR_VRSS_PRPR_SIGN { get; set; }

        [JsonPropertyName("LWPR_VRSS_PRPR")]
        public string LWPR_VRSS_PRPR { get; set; }

        [JsonPropertyName("BSOP_DATE")]
        public string BSOP_DATE { get; set; }

        [JsonPropertyName("NEW_MKOP_CLS_CODE")]
        public string NEW_MKOP_CLS_CODE { get; set; }

        [JsonPropertyName("TRHT_YN")]
        public string TRHT_YN { get; set; }

        [JsonPropertyName("ASKP_RSQN1")]
        public string ASKP_RSQN1 { get; set; }

        [JsonPropertyName("BIDP_RSQN1")]
        public string BIDP_RSQN1 { get; set; }

        [JsonPropertyName("TOTAL_ASKP_RSQN")]
        public string TOTAL_ASKP_RSQN { get; set; }

        [JsonPropertyName("TOTAL_BIDP_RSQN")]
        public string TOTAL_BIDP_RSQN { get; set; }

        [JsonPropertyName("VOL_TNRT")]
        public string VOL_TNRT { get; set; }

        [JsonPropertyName("PRDY_SMNS_HOUR_ACML_VOL")]
        public string PRDY_SMNS_HOUR_ACML_VOL { get; set; }

        [JsonPropertyName("PRDY_SMNS_HOUR_ACML_VOL_RATE")]
        public string PRDY_SMNS_HOUR_ACML_VOL_RATE { get; set; }

        [JsonPropertyName("HOUR_CLS_CODE")]
        public string HOUR_CLS_CODE { get; set; }

        [JsonPropertyName("MRKT_TRTM_CLS_CODE")]
        public string MRKT_TRTM_CLS_CODE { get; set; }

        [JsonPropertyName("VI_STND_PRC")]
        public string VI_STND_PRC { get; set; }

        [JsonPropertyName("COMPANY")]
        public string COMPANY { get; set; }
    }
}
