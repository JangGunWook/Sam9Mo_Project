using Newtonsoft.Json;
using ReaLTaiizor.Forms;
using System;
using System.Net.Mail;
using System.Windows.Forms;

namespace ReaLTaiizor.Login
{
    public partial class Login1 : CrownForm
    {
        public Login1()
        {
            InitializeComponent();
        }

        private void MaterialLabel1_Click(object sender, EventArgs e)
        {
            hopeSwitch1.Checked = !hopeSwitch1.Checked;
        }

        private bool isLoading = false;
        private void btnAdminSignIn_Click(object sender, EventArgs e)
        {
            if (isLoading) return;
               
            Button button = sender as Button;

            button.Enabled = false;
            adminSignInAction();
            button.Enabled = true;
        }

        private bool checkAdminAccount()
        {
            string adminAccount = txtBoxAdminAccount.Text;
            if (adminAccount == null || adminAccount.Length < 10)
            {
                return false;
            }
            if (!IsValid(adminAccount))
            {
                return false;
            }
            return true;
        }
        private async void adminSignInAction()
        {
            isLoading = true;
            string adminAccount = txtBoxAdminAccount.Text;
            string adminPassword = txtBoxAdminPassword.Text;

            if (!checkAdminAccount())
            {
                isLoading = false;
                notiBoxSignInError.Visible = true;
                notiBoxSignInError.Text = "Account EMail 을 확인하여 주십시요.";
                return;
            }
            if (adminPassword == null || adminPassword.Length == 0)
            {
                isLoading = false;
                notiBoxSignInError.Visible = true;
                notiBoxSignInError.Text = "Password 를 입력해 주십시요.";
                txtBoxAdminPassword.Focus();
                return;
            }

            var data = new
            {
                account = adminAccount,
                password = adminPassword
            };

            String myContent = JsonConvert.SerializeObject(data);

            HttpClientApi httpClientApi = new HttpClientApi($"http://{ProgramInformationManager.Instance.API_SERVER_IP}:{ProgramInformationManager.Instance.API_SERVER_PORT}");
            String returnData = await httpClientApi.actionHttpApi("POST", myContent, "/sign-in");

            if (returnData == null)
            {
                isLoading = false;
                notiBoxSignInError.Visible = true;
                notiBoxSignInError.Text = "Account, Password Error";
                txtBoxAdminPassword.Focus();
                return;
            }
            SignInResponse responseData = JsonConvert.DeserializeObject<SignInResponse>(returnData);
            if (responseData.status == "SUCCESS")
            {
                ProgramInformationManager.Instance.AccessToken = responseData.data.accessToken;

                ProgramInformationManager.Instance.RefreshToken = responseData.data.refreshToken;

                MessageBox.Show("마지막 접속 시간 : " + responseData.data.lastConnectedTime);
                var mainForm = new AdminMain();
                mainForm.FormClosed += (s, args) => this.Close();
                this.Hide();
                mainForm.Show();
            }
        }
        public bool IsValid(string emailaddress)
        {
            try
            {
                MailAddress m = new MailAddress(emailaddress);

                return true;
            }
            catch (FormatException)
            {
                return false;
            }
        }

        private void txtBoxAdminAccount_Click(object sender, EventArgs e)
        {
            notiBoxSignInError.Visible = false;
        }

        private void txtBoxAdminAccount_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            notiBoxSignInError.Visible = false;
            if (e.KeyCode == System.Windows.Forms.Keys.Enter)
            {
                if (!checkAdminAccount())
                {
                    notiBoxSignInError.Visible = true;
                    notiBoxSignInError.Text = "Account EMail 을 확인하여 주십시요.";
                    return;
                }
                txtBoxAdminPassword.Focus();
            }
        }

        private void txtBoxAdminPassword_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
        {
            notiBoxSignInError.Visible = false;
            if (e.KeyCode == System.Windows.Forms.Keys.Enter)
            {
                if (isLoading) return;
                adminSignInAction();
            }
        }
    }
}