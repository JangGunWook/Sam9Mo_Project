using Newtonsoft.Json;
using ReaLTaiizor.Colors;
using ReaLTaiizor.Controls;
using ReaLTaiizor.Enum.Material;
using ReaLTaiizor.Forms;
using ReaLTaiizor.Manager;
using ReaLTaiizor.Util;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.WebSockets;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Windows.Forms;
using System.Linq;
using System.Xml.Linq;
using System.Windows.Forms.DataVisualization.Charting;

namespace ReaLTaiizor.Login
{
    public partial class AdminMain : MaterialForm
    {
        private readonly MaterialSkinManager materialSkinManager;
        public AdminMain()
        {
            InitializeComponent();
            // Initialize MaterialSkinManager
            materialSkinManager = MaterialSkinManager.Instance;

            // Set this to false to disable backcolor enforcing on non-materialSkin components
            // This HAS to be set before the AddFormToManage()
            materialSkinManager.EnforceBackcolorOnAllComponents = true;

            // MaterialSkinManager properties
            materialSkinManager.AddFormToManage(this);
            materialSkinManager.Theme = MaterialSkinManager.Themes.LIGHT;
            materialSkinManager.ColorScheme = new MaterialColorScheme(MaterialPrimary.Indigo500, MaterialPrimary.Indigo700, MaterialPrimary.Indigo100, MaterialAccent.Pink200, MaterialTextShade.WHITE);
        }

        private void AdminMain_Load(object sender, EventArgs e)
        {
            loadNewsComboBox();
            metroTextBox1.Text = ProgramInformationManager.Instance.AccessToken;
            metroTextBox2.Text = ProgramInformationManager.Instance.RefreshToken;
        }
        NewsResponse newsResponseData = null;
        MembersResponse membersResponseData = null;

        /****
         * Kospi 40, Kosdaq 40 개 회사, 총 80개 회사의 주식 정보와 그외 정보
         * 
         */
        private async void loadKoreaStockInformation()
        {
            try
            {
                HttpClientApi httpClientApi = new HttpClientApi("http://121.179.83.68:8881");
                string? returnData = await httpClientApi.actionHttpApi("GET", null, "/stock_api_all");
                if (returnData != null)
                {
                    Dictionary<string, StockApiResponse> values = JsonConvert.DeserializeObject<Dictionary<string, StockApiResponse>>(returnData);
                    var InitialDataArray = from row in values
                                           select new
                                           {
                                               종목코드 = row.Key,
                                               종목명 = row.Value.Initial?.hts_kor_isnm,
                                               row.Value.Initial?.prdy_vrss,
                                               row.Value.Initial?.prdy_vrss_sign,
                                               row.Value.Initial?.prdy_ctrt,
                                               row.Value.Initial?.stck_prdy_clpr,
                                               row.Value.Initial?.acml_vol,
                                               row.Value.Initial?.acml_tr_pbmn,
                                               row.Value.Initial?.stck_prpr,
                                               row.Value.Initial?.stck_shrn_iscd,
                                               row.Value.Initial?.prdy_vol,
                                               row.Value.Initial?.stck_mxpr,
                                               row.Value.Initial?.stck_llam,
                                               row.Value.Initial?.stck_oprc,
                                               row.Value.Initial?.stck_hgpr,
                                               row.Value.Initial?.stck_lwpr,
                                               row.Value.Initial?.stck_prdy_oprc,
                                               row.Value.Initial?.stck_prdy_hgpr,
                                               row.Value.Initial?.stck_prdy_lwpr,
                                               row.Value.Initial?.askp,
                                               row.Value.Initial?.bidp,
                                               row.Value.Initial?.prdy_vrss_vol,
                                               row.Value.Initial?.vol_tnrt,
                                               row.Value.Initial?.stck_fcam,
                                               row.Value.Initial?.lstn_stcn,
                                               row.Value.Initial?.cpfn,
                                               row.Value.Initial?.hts_avls,
                                               row.Value.Initial?.per,
                                               row.Value.Initial?.eps,
                                               row.Value.Initial?.pbr
                                           };
                    var CurrentTradeDataArray = from row in values
                                           select new
                                           {
                                               row.Key,
                                               row.Value.Current_trade?.COMPANY,
                                               row.Value.Current_trade?.MKSC_SHRN_ISCD,
                                               row.Value.Current_trade?.STCK_CNTG_HOUR,
                                               row.Value.Current_trade?.STCK_PRPR,
                                               row.Value.Current_trade?.PRDY_VRSS_SIGN,
                                               row.Value.Current_trade?.PRDY_VRSS,
                                               row.Value.Current_trade?.PRDY_CTRT,
                                               row.Value.Current_trade?.WGHN_AVRG_STCK_PRC,
                                               row.Value.Current_trade?.STCK_OPRC,
                                               row.Value.Current_trade?.STCK_HGPR,
                                               row.Value.Current_trade?.STCK_LWPR,
                                               row.Value.Current_trade?.ASKP1,
                                               row.Value.Current_trade?.BIDP1,
                                               row.Value.Current_trade?.CNTG_VOL,
                                               row.Value.Current_trade?.ACML_VOL,
                                               row.Value.Current_trade?.ACML_TR_PBMN,
                                               row.Value.Current_trade?.SELN_CNTG_CSNU,
                                               row.Value.Current_trade?.SHNU_CNTG_CSNU,
                                               row.Value.Current_trade?.NTBY_CNTG_CSNU,
                                               row.Value.Current_trade?.CTTR,
                                               row.Value.Current_trade?.SELN_CNTG_SMTN,
                                               row.Value.Current_trade?.SHNU_CNTG_SMTN,
                                               row.Value.Current_trade?.CCLD_DVSN,
                                               row.Value.Current_trade?.SHNU_RATE,
                                               row.Value.Current_trade?.PRDY_VOL_VRSS_ACML_VOL_RATE,
                                               row.Value.Current_trade?.OPRC_HOUR,
                                               row.Value.Current_trade?.OPRC_VRSS_PRPR_SIGN,
                                               row.Value.Current_trade?.HGPR_HOUR,
                                               row.Value.Current_trade?.HGPR_VRSS_PRPR_SIGN,
                                               row.Value.Current_trade?.HGPR_VRSS_PRPR,
                                               row.Value.Current_trade?.LWPR_HOUR,
                                               row.Value.Current_trade?.LWPR_VRSS_PRPR_SIGN,
                                               row.Value.Current_trade?.LWPR_VRSS_PRPR,
                                               row.Value.Current_trade?.BSOP_DATE,
                                               row.Value.Current_trade?.NEW_MKOP_CLS_CODE 
                                           };
                    koreaStockApiInitialDataGridView.DataSource = InitialDataArray.ToArray();
                    koreaStockApiCurrentTradeDataGridView.DataSource = CurrentTradeDataArray.ToArray();
                }
                else
                {
                    MessageBox.Show("값을 불러오지 못하였습니다. 잠시 후 재시도하여 주시기 바랍니다.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
        private void foxButton1_Click(object sender, EventArgs e)
        {
            loadNews();
        }

        private void foxButton2_Click(object sender, EventArgs e)
        {
            loadMembers();
        }
        private async void loadNewsComboBox()
        {
            try
            {
                HttpClientApi httpClientApi = new HttpClientApi($"http://{ProgramInformationManager.Instance.API_SERVER_IP}:{ProgramInformationManager.Instance.API_SERVER_PORT}");
                string? returnData = await httpClientApi.actionHttpApi("GET", null, "/admin/news/company");

                if (returnData != null)
                {
                    NewsFieldDistinctData apiResponse = JsonConvert.DeserializeObject<NewsFieldDistinctData>(returnData);
                    if (apiResponse.status == "SUCCESS")
                    {
                        stockCompanyComboBox.DataSource = null;
                        stockCompanyComboBox.DataSource = apiResponse.data.stockCompany;

                        newsCategoryComboBox.DataSource = null;
                        newsCategoryComboBox.DataSource = apiResponse.data.newsCategory;
                    } else {
                        MessageBox.Show(apiResponse.message.ToString());
                    }

                    accessTokenTextBox.Text = ProgramInformationManager.Instance.AccessToken;
                    refreshTextBox.Text = ProgramInformationManager.Instance.RefreshToken;
                } else
                {
                    MessageBox.Show("값을 불러오지 못하였습니다. 잠시 후 재시도하여 주시기 바랍니다.");
                }
            } catch (Exception ex) {
                MessageBox.Show(ex.Message);
            }
        }
        private async void loadNews()
        {
            var data = new
            {
                stockCompany = stockCompanySwitch.Checked == true ? stockCompanyComboBox.Text : "",
                newsCategory = newsCategorySwitch.Checked == true ? newsCategoryComboBox.Text : "",
                newsYear = newsDateSwitch.Checked == true ? newsYearComboBox.Text : "",
                newsMonth = newsDateSwitch.Checked == true ? newsMonthComboBox.Text : "",
                newsDay = newsDateSwitch.Checked == true ? newsDayComboBox.Text : "",
                page = 0
            };
            String myContent = JsonConvert.SerializeObject(data);

            HttpClientApi httpClientApi = new HttpClientApi($"http://{ProgramInformationManager.Instance.API_SERVER_IP}:{ProgramInformationManager.Instance.API_SERVER_PORT}");
            String returnData = await httpClientApi.actionHttpApi("POST", myContent, "/admin/news");

            metroTextBox1.Text = ProgramInformationManager.Instance.AccessToken;
            if (returnData != null)
            {
                newsResponseData = JsonConvert.DeserializeObject<NewsResponse>(returnData);
                if (newsResponseData.status == "SUCCESS")
                {
                    newsDataGridView.DataSource = newsResponseData.data.newsData;
                    totalItemsTextBox.Text = newsResponseData.data.totalItems.ToString();
                    totalPagesTextBox.Text = newsResponseData.data.totalPages.ToString();
                    currentPageTextBox.Text = newsResponseData.data.currentPage.ToString();
                } else
                {
                    MessageBox.Show(newsResponseData.message.ToString());
                }
            } else
            {
                MessageBox.Show(returnData + "$returnData 값을 불러오지 못하였습니다. 잠시 후 재시도하여 주시기 바랍니다.");
            }

        }

        private async void loadMembers()
        {
            HttpClientApi httpClientApi = new HttpClientApi($"http://{ProgramInformationManager.Instance.API_SERVER_IP}:{ProgramInformationManager.Instance.API_SERVER_PORT}");
            string returnData = await httpClientApi.actionHttpApi("GET", null, "/admin/members/0");

            if (returnData != null)
            {
                membersResponseData = JsonConvert.DeserializeObject<MembersResponse>(returnData);
                if (membersResponseData.status == "SUCCESS")
                {
                    membersDataGridView.DataSource = membersResponseData.data.membersData;
                }
                else
                {
                    MessageBox.Show(newsResponseData.message.ToString());
                }

                accessTokenTextBox.Text = ProgramInformationManager.Instance.AccessToken;
                refreshTextBox.Text = ProgramInformationManager.Instance.RefreshToken;
            }
            else
            {
                MessageBox.Show("값을 불러오지 못하였습니다. 잠시 후 재시도하여 주시기 바랍니다.");
            }
        }

        private void loadKospiD1()
        {
            
            HttpClientApi httpClientApi = new HttpClientApi($"http://{ProgramInformationManager.Instance.API_SERVER_IP}:9199");

            koreaStockDataGridView(httpClientApi, "/kospi/kospi_D1", kospiD1DataGridView, kospiD1Chart);
            
            if (!loadKoreaStockInfo)
            {
                koreaStockDataGridView(httpClientApi, "/kospi/kospi_D5", kospiD5DataGridView, kospiD5Chart);
                koreaStockDataGridView(httpClientApi, "/kospi/kospi_M1", kospiM1DataGridView, kospiM1Chart);
                koreaStockDataGridView(httpClientApi, "/kospi/kospi_M6", kospiM6DataGridView, kospiM6Chart);
                koreaStockDataGridView(httpClientApi, "/kospi/kospi_YTD", kospiYTDDataGridView, kospiYTDChart);
            }

            koreaStockDataGridView(httpClientApi, "/kospi200/kospi200_D1", kospi200D1DataGridView, kospi200D1Chart);
            if (!loadKoreaStockInfo)
            {
                koreaStockDataGridView(httpClientApi, "/kospi200/kospi200_D5", kospi200D5DataGridView, kospi200D5Chart);
                koreaStockDataGridView(httpClientApi, "/kospi200/kospi200_M1", kospi200M1DataGridView, kospi200M1Chart);
                koreaStockDataGridView(httpClientApi, "/kospi200/kospi200_M6", kospi200M6DataGridView, kospi200M6Chart);
                koreaStockDataGridView(httpClientApi, "/kospi200/kospi200_YTD", kospi200YTDDataGridView, kospi200YTDChart);
            }

            koreaStockDataGridView(httpClientApi, "/kosdaq/kosdaq_D1", kosdaqD1DataGridView, kosdaqD1Chart);
            if (!loadKoreaStockInfo)
            {
                koreaStockDataGridView(httpClientApi, "/kosdaq/kosdaq_D5", kosdaqD5DataGridView, kosdaqD5Chart);
                koreaStockDataGridView(httpClientApi, "/kosdaq/kosdaq_M1", kosdaqM1DataGridView, kosdaqM1Chart);
                koreaStockDataGridView(httpClientApi, "/kosdaq/kosdaq_M6", kosdaqM6DataGridView, kosdaqM6Chart);
                koreaStockDataGridView(httpClientApi, "/kosdaq/kosdaq_YTD", kosdaqYTDDataGridView, kosdaqYTDChart);
            }
            loadKoreaStockInfo = true;
        }
        /*
        private void newsDataGridView_Scroll(object sender, ScrollEventArgs e)
        {
            DataGridView dataGridView = sender as DataGridView;
            if (dataGridView.DisplayedRowCount(false) + dataGridView.FirstDisplayedScrollingRowIndex >= dataGridView.RowCount)
            {
                loadNews();
            }
        }
        */

        private async void koreaStockDataGridView(HttpClientApi httpClientApi, String param, DataGridView dataGridView,Chart chart)
        {
            string returnStockData = await httpClientApi.actionHttpApi("GET", null, param);
            KospiKosDaqApiResponse apiResponse = null;
            if (returnStockData != null)
            {
                try
                {
                    apiResponse = JsonConvert.DeserializeObject<KospiKosDaqApiResponse>(returnStockData);

                    if (apiResponse.date is not null)
                    {
                        if (chart != null)
                        {
                            int? max = 0;
                            int? min = 0;
                            apiResponse.data.ForEach(data =>
                            {
                                if (max == 0)
                                {
                                    max = data.HighInt;
                                }
                                if (data.HighInt > 0 && data.HighInt > max) max = data.HighInt;
                                if (min == 0)
                                {
                                    min = data.LowInt;
                                }
                                if (data.LowInt > 0 && data.LowInt < min) min = data.LowInt;
                            });
                            //Clear Grid
                            chart.ChartAreas["ChartArea1"].AxisX.MajorGrid.LineWidth = 1;
                            chart.ChartAreas["ChartArea1"].AxisY.MajorGrid.LineWidth = 1;
                            chart.ChartAreas["ChartArea1"].AxisY.Maximum = (double) (max * 1.001);
                            chart.ChartAreas["ChartArea1"].AxisY.Minimum = (double) (min * 0.999);
                            chart.ChartAreas["ChartArea1"].AxisX.LabelAutoFitStyle = LabelAutoFitStyles.WordWrap;
                            chart.ChartAreas["ChartArea1"].AxisX.IsLabelAutoFit = true;
                            chart.ChartAreas["ChartArea1"].AxisX.LabelStyle.Enabled = true;

                            //Init
                            chart.Series["Daily"].XValueMember = "Date";
                            chart.Series["Daily"].YValueMembers = "High,Low,Open,Close";
                            
                            chart.Series["Daily"].XValueType = ChartValueType.String;
                            chart.Series["Daily"].YValueType = ChartValueType.Int64;
                            chart.Series["Daily"].CustomProperties = "PriceDownColor=Red,PriceUpColor=Blue";
                            chart.Series["Daily"]["OpenCloseStyle"] = "Triangle";
                            chart.Series["Daily"]["ShowOpenClose"] = "Both";
                            chart.DataManipulator.IsStartFromFirst = true;

                            chart.DataSource = apiResponse.data.Select(d => new
                            {
                                Date = d.DateTime.ToString(),
                                Open = d.OpenInt,
                                Close = d.CloseInt,
                                High = d.HighInt,
                                Low = d.LowInt,
                                Volume = d.volume
                            }).ToList();
                            chart.DataBind();
                        }

                        dataGridView.DataSource = apiResponse.data.Select(d => new
                        {
                            Date = d.DateTime,
                            Open = d.OpenInt,
                            Close = d.CloseInt,
                            High = d.HighInt,
                            Low = d.LowInt,
                            Volume = d.volume
                        }).ToList();
                    }
                }
                catch (JsonSerializationException ex)
                {
                    MessageBox.Show(ex.ToString());
                }
            }
            else
            {
                MessageBox.Show("값을 불러오지 못하였습니다. 잠시 후 재시도하여 주시기 바랍니다.");
            }
        }

        private void newsDataGridView_Click(object sender, EventArgs e)
        {
            newsDetailsPanel.Visible = false;
        }

        private void newsDetailsSaveButton_Click(object sender, EventArgs e)
        {
            newsDetailsPanel.Visible = false;
        }

        private void newsDetailsDeleteButton_Click(object sender, EventArgs e)
        {
            newsDetailsPanel.Visible = false;
        }

        private void newsDetailsCloseButton_Click(object sender, EventArgs e)
        {
            newsDetailsPanel.Visible = false;
        }
        private void newsDataGridView_CellDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            // PoisonDataGridView cell = sender as PoisonDataGridView;
            if (e.RowIndex >= 0)
            {
                try
                {
                    newsDetailsPanel.Visible = true;
                    newsDetailsTitle.Text = newsResponseData.data.newsData[e.RowIndex].newsTitle;
                    newsDetailsKeyword.Text = newsResponseData.data.newsData[e.RowIndex].keyword;
                    newsDetailsContentTextBox.Text = newsResponseData.data.newsData[e.RowIndex].newsContent;
                    newsDetailsKeywordTextBox.Text = newsResponseData.data.newsData[e.RowIndex].keyword;
                }
                catch (Exception ex)
                {
                    return;
                }
            }
           }

        private void membersDataGridView_CellDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            PoisonDataGridView cell = sender as PoisonDataGridView;
            if (e.RowIndex >= 0)
            {
                try
                {
                    MessageBox.Show(cell.Rows[e.RowIndex].Cells[0].Value.ToString());
                } catch (Exception ex)
                {
                    return;
                }
            }
        }
        private void stockCompanySwitch_CheckedChanged(object sender, EventArgs e)
        {
            MaterialSwitch materialSwitch = sender as MaterialSwitch;

            if (materialSwitch.Checked)
            {
                newsCategorySwitch.Checked = false;
                newsDateSwitch.Checked = false;
            }
        }

        private void newsCategorySwitch_CheckedChanged(object sender, EventArgs e)
        {
            MaterialSwitch materialSwitch = sender as MaterialSwitch;

            if (materialSwitch.Checked)
            {
                stockCompanySwitch.Checked = false;
                newsDateSwitch.Checked = false;
            }
        }

        private void newsDateSwitch_CheckedChanged(object sender, EventArgs e)
        {
            MaterialSwitch materialSwitch = sender as MaterialSwitch;

            if (materialSwitch.Checked)
            {
                stockCompanySwitch.Checked = false;
                newsCategorySwitch.Checked = false;
            }
        }

        private void stockCompanyComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            stockCompanySwitch.Checked = true;
            loadNews();
        }

        private void newsCategoryComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            newsCategorySwitch.Checked = true;
            loadNews();
        }

        private bool loadKoreaStockInfo = false;
        private void materialTabControl1_SelectedIndexChanged(object sender, EventArgs e)
        {
            MaterialTabControl materialTabControl = sender as MaterialTabControl;

            switch (materialTabControl.SelectedIndex)
            {
                case ProgramInformationManager.MAIN_PAGE:
                    break;
                case ProgramInformationManager.MEMBERS_PAGE:
                    loadMembers();
                    break;
                case ProgramInformationManager.NEWS_PAGE:
                    newsDateSwitch.Checked = true;

                    DateTime today = DateTime.Now;
                    newsYearComboBox.Text = today.ToString("yyyy");
                    newsMonthComboBox.Text = today.ToString("MM");
                    newsDayComboBox.Text = today.ToString("dd");

                    loadNews();

                    stockCompanySwitch.Checked = false;
                    newsCategorySwitch.Checked = false;

                    break;
                case ProgramInformationManager.SUB4_PAGE:
                    loadKoreaStockInformation();
                    break;
                case ProgramInformationManager.SUB5_PAGE:
                    loadKospiD1();
                    break;
                case ProgramInformationManager.SUB6_PAGE:
                    break;
                case ProgramInformationManager.SUB7_PAGE:
                    break;
                default:
                    break;
            }
        }
    }
}
