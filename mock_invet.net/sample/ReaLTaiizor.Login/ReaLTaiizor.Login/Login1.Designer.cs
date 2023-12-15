namespace ReaLTaiizor.Login
{
    partial class Login1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Login1));
            this.parrotFormEllipse1 = new ReaLTaiizor.Controls.ParrotFormEllipse();
            this.parrotFormHandle1 = new ReaLTaiizor.Controls.ParrotFormHandle();
            this.panel1 = new System.Windows.Forms.Panel();
            this.nightControlBox1 = new ReaLTaiizor.Controls.NightControlBox();
            this.parrotFormHandle2 = new ReaLTaiizor.Controls.ParrotFormHandle();
            this.panel2 = new System.Windows.Forms.Panel();
            this.notiBoxSignInError = new ReaLTaiizor.Controls.FoxNotification();
            this.btnAdminSignIn = new ReaLTaiizor.Controls.MaterialButton();
            this.materialLabel1 = new ReaLTaiizor.Controls.MaterialLabel();
            this.hopeSwitch1 = new ReaLTaiizor.Controls.HopeSwitch();
            this.txtBoxAdminPassword = new ReaLTaiizor.Controls.HopeTextBox();
            this.txtBoxAdminAccount = new ReaLTaiizor.Controls.HopeTextBox();
            this.hopePictureBox1 = new ReaLTaiizor.Controls.HopePictureBox();
            this.panel1.SuspendLayout();
            this.panel2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.hopePictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // parrotFormEllipse1
            // 
            this.parrotFormEllipse1.CornerRadius = 10;
            this.parrotFormEllipse1.EffectedForm = this;
            // 
            // parrotFormHandle1
            // 
            this.parrotFormHandle1.DockAtTop = true;
            this.parrotFormHandle1.HandleControl = this.panel1;
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.Color.Transparent;
            this.panel1.BackgroundImage = global::ReaLTaiizor.Login.Properties.Resources.pexels_guillaume_meurice_2529179;
            this.panel1.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.panel1.Controls.Add(this.nightControlBox1);
            this.panel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel1.Location = new System.Drawing.Point(280, 0);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(493, 539);
            this.panel1.TabIndex = 0;
            // 
            // nightControlBox1
            // 
            this.nightControlBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.nightControlBox1.BackColor = System.Drawing.Color.Transparent;
            this.nightControlBox1.CloseHoverColor = System.Drawing.Color.FromArgb(((int)(((byte)(199)))), ((int)(((byte)(80)))), ((int)(((byte)(80)))));
            this.nightControlBox1.CloseHoverForeColor = System.Drawing.Color.White;
            this.nightControlBox1.Cursor = System.Windows.Forms.Cursors.Hand;
            this.nightControlBox1.DefaultLocation = true;
            this.nightControlBox1.DisableMaximizeColor = System.Drawing.Color.FromArgb(((int)(((byte)(105)))), ((int)(((byte)(105)))), ((int)(((byte)(105)))));
            this.nightControlBox1.DisableMinimizeColor = System.Drawing.Color.FromArgb(((int)(((byte)(105)))), ((int)(((byte)(105)))), ((int)(((byte)(105)))));
            this.nightControlBox1.EnableCloseColor = System.Drawing.Color.FromArgb(((int)(((byte)(160)))), ((int)(((byte)(160)))), ((int)(((byte)(160)))));
            this.nightControlBox1.EnableMaximizeButton = false;
            this.nightControlBox1.EnableMaximizeColor = System.Drawing.Color.FromArgb(((int)(((byte)(160)))), ((int)(((byte)(160)))), ((int)(((byte)(160)))));
            this.nightControlBox1.EnableMinimizeButton = true;
            this.nightControlBox1.EnableMinimizeColor = System.Drawing.Color.FromArgb(((int)(((byte)(160)))), ((int)(((byte)(160)))), ((int)(((byte)(160)))));
            this.nightControlBox1.Location = new System.Drawing.Point(354, 0);
            this.nightControlBox1.MaximizeHoverColor = System.Drawing.Color.FromArgb(((int)(((byte)(15)))), ((int)(((byte)(255)))), ((int)(((byte)(255)))), ((int)(((byte)(255)))));
            this.nightControlBox1.MaximizeHoverForeColor = System.Drawing.Color.White;
            this.nightControlBox1.MinimizeHoverColor = System.Drawing.Color.FromArgb(((int)(((byte)(15)))), ((int)(((byte)(255)))), ((int)(((byte)(255)))), ((int)(((byte)(255)))));
            this.nightControlBox1.MinimizeHoverForeColor = System.Drawing.Color.White;
            this.nightControlBox1.Name = "nightControlBox1";
            this.nightControlBox1.Size = new System.Drawing.Size(139, 31);
            this.nightControlBox1.TabIndex = 6;
            // 
            // parrotFormHandle2
            // 
            this.parrotFormHandle2.DockAtTop = true;
            this.parrotFormHandle2.HandleControl = this.panel2;
            // 
            // panel2
            // 
            this.panel2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(30)))), ((int)(((byte)(30)))));
            this.panel2.Controls.Add(this.notiBoxSignInError);
            this.panel2.Controls.Add(this.btnAdminSignIn);
            this.panel2.Controls.Add(this.materialLabel1);
            this.panel2.Controls.Add(this.hopeSwitch1);
            this.panel2.Controls.Add(this.txtBoxAdminPassword);
            this.panel2.Controls.Add(this.txtBoxAdminAccount);
            this.panel2.Controls.Add(this.hopePictureBox1);
            this.panel2.Dock = System.Windows.Forms.DockStyle.Left;
            this.panel2.Location = new System.Drawing.Point(0, 0);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(280, 539);
            this.panel2.TabIndex = 1;
            // 
            // notiBoxSignInError
            // 
            this.notiBoxSignInError.BlueBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(217)))), ((int)(((byte)(237)))), ((int)(((byte)(248)))));
            this.notiBoxSignInError.BlueBarColor = System.Drawing.Color.FromArgb(((int)(((byte)(175)))), ((int)(((byte)(217)))), ((int)(((byte)(240)))));
            this.notiBoxSignInError.BlueTextColor = System.Drawing.Color.FromArgb(((int)(((byte)(73)))), ((int)(((byte)(143)))), ((int)(((byte)(184)))));
            this.notiBoxSignInError.Cursor = System.Windows.Forms.Cursors.Default;
            this.notiBoxSignInError.EnabledCalc = true;
            this.notiBoxSignInError.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.notiBoxSignInError.GreenBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(223)))), ((int)(((byte)(240)))), ((int)(((byte)(214)))));
            this.notiBoxSignInError.GreenBarColor = System.Drawing.Color.FromArgb(((int)(((byte)(206)))), ((int)(((byte)(229)))), ((int)(((byte)(182)))));
            this.notiBoxSignInError.GreenTextColor = System.Drawing.Color.FromArgb(((int)(((byte)(78)))), ((int)(((byte)(140)))), ((int)(((byte)(69)))));
            this.notiBoxSignInError.Location = new System.Drawing.Point(12, 233);
            this.notiBoxSignInError.Name = "notiBoxSignInError";
            this.notiBoxSignInError.RedBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(242)))), ((int)(((byte)(222)))), ((int)(((byte)(222)))));
            this.notiBoxSignInError.RedBarColor = System.Drawing.Color.FromArgb(((int)(((byte)(235)))), ((int)(((byte)(204)))), ((int)(((byte)(209)))));
            this.notiBoxSignInError.RedTextColor = System.Drawing.Color.FromArgb(((int)(((byte)(194)))), ((int)(((byte)(99)))), ((int)(((byte)(94)))));
            this.notiBoxSignInError.Size = new System.Drawing.Size(260, 40);
            this.notiBoxSignInError.Style = ReaLTaiizor.Controls.FoxNotification.Styles.Red;
            this.notiBoxSignInError.TabIndex = 22;
            this.notiBoxSignInError.Text = "error";
            this.notiBoxSignInError.Visible = false;
            this.notiBoxSignInError.YellowBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(252)))), ((int)(((byte)(248)))), ((int)(((byte)(225)))));
            this.notiBoxSignInError.YellowBarColor = System.Drawing.Color.FromArgb(((int)(((byte)(250)))), ((int)(((byte)(235)))), ((int)(((byte)(200)))));
            this.notiBoxSignInError.YellowTextColor = System.Drawing.Color.FromArgb(((int)(((byte)(144)))), ((int)(((byte)(131)))), ((int)(((byte)(88)))));
            // 
            // btnAdminSignIn
            // 
            this.btnAdminSignIn.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.btnAdminSignIn.AutoSize = false;
            this.btnAdminSignIn.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.btnAdminSignIn.CharacterCasing = ReaLTaiizor.Controls.MaterialButton.CharacterCasingEnum.Normal;
            this.btnAdminSignIn.Cursor = System.Windows.Forms.Cursors.Hand;
            this.btnAdminSignIn.Density = ReaLTaiizor.Controls.MaterialButton.MaterialButtonDensity.Default;
            this.btnAdminSignIn.Depth = 0;
            this.btnAdminSignIn.HighEmphasis = true;
            this.btnAdminSignIn.Icon = null;
            this.btnAdminSignIn.IconType = ReaLTaiizor.Controls.MaterialButton.MaterialIconType.Rebase;
            this.btnAdminSignIn.Location = new System.Drawing.Point(12, 443);
            this.btnAdminSignIn.Margin = new System.Windows.Forms.Padding(4, 6, 4, 6);
            this.btnAdminSignIn.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.btnAdminSignIn.Name = "btnAdminSignIn";
            this.btnAdminSignIn.NoAccentTextColor = System.Drawing.Color.Empty;
            this.btnAdminSignIn.Size = new System.Drawing.Size(260, 36);
            this.btnAdminSignIn.TabIndex = 20;
            this.btnAdminSignIn.Text = "Administrator Sign In";
            this.btnAdminSignIn.Type = ReaLTaiizor.Controls.MaterialButton.MaterialButtonType.Contained;
            this.btnAdminSignIn.UseAccentColor = true;
            this.btnAdminSignIn.UseVisualStyleBackColor = true;
            this.btnAdminSignIn.Click += new System.EventHandler(this.btnAdminSignIn_Click);
            // 
            // materialLabel1
            // 
            this.materialLabel1.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.materialLabel1.AutoSize = true;
            this.materialLabel1.Cursor = System.Windows.Forms.Cursors.Hand;
            this.materialLabel1.Depth = 0;
            this.materialLabel1.Font = new System.Drawing.Font("Roboto Medium", 14F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Pixel);
            this.materialLabel1.FontType = ReaLTaiizor.Manager.MaterialSkinManager.FontType.Subtitle2;
            this.materialLabel1.HighEmphasis = true;
            this.materialLabel1.Location = new System.Drawing.Point(60, 405);
            this.materialLabel1.MouseState = ReaLTaiizor.Helper.MaterialDrawHelper.MaterialMouseState.HOVER;
            this.materialLabel1.Name = "materialLabel1";
            this.materialLabel1.Size = new System.Drawing.Size(94, 17);
            this.materialLabel1.TabIndex = 12;
            this.materialLabel1.Text = "Remember me";
            this.materialLabel1.UseAccent = true;
            this.materialLabel1.Click += new System.EventHandler(this.MaterialLabel1_Click);
            // 
            // hopeSwitch1
            // 
            this.hopeSwitch1.Anchor = System.Windows.Forms.AnchorStyles.Left;
            this.hopeSwitch1.AutoSize = true;
            this.hopeSwitch1.BaseColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(12)))), ((int)(((byte)(45)))));
            this.hopeSwitch1.BaseOffColor = System.Drawing.Color.FromArgb(((int)(((byte)(221)))), ((int)(((byte)(141)))), ((int)(((byte)(144)))));
            this.hopeSwitch1.BaseOnColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(128)))), ((int)(((byte)(128)))));
            this.hopeSwitch1.Checked = true;
            this.hopeSwitch1.CheckState = System.Windows.Forms.CheckState.Checked;
            this.hopeSwitch1.Cursor = System.Windows.Forms.Cursors.Hand;
            this.hopeSwitch1.Location = new System.Drawing.Point(14, 403);
            this.hopeSwitch1.Name = "hopeSwitch1";
            this.hopeSwitch1.Size = new System.Drawing.Size(40, 20);
            this.hopeSwitch1.TabIndex = 10;
            this.hopeSwitch1.Text = "hopeSwitch1";
            this.hopeSwitch1.UseVisualStyleBackColor = true;
            // 
            // txtBoxAdminPassword
            // 
            this.txtBoxAdminPassword.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.txtBoxAdminPassword.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(12)))), ((int)(((byte)(45)))));
            this.txtBoxAdminPassword.BaseColor = System.Drawing.Color.Transparent;
            this.txtBoxAdminPassword.BorderColorA = System.Drawing.Color.DodgerBlue;
            this.txtBoxAdminPassword.BorderColorB = System.Drawing.Color.DarkGray;
            this.txtBoxAdminPassword.Font = new System.Drawing.Font("Segoe UI", 12F);
            this.txtBoxAdminPassword.ForeColor = System.Drawing.Color.Gainsboro;
            this.txtBoxAdminPassword.Hint = "Account : Password";
            this.txtBoxAdminPassword.Location = new System.Drawing.Point(12, 344);
            this.txtBoxAdminPassword.MaxLength = 20;
            this.txtBoxAdminPassword.Multiline = false;
            this.txtBoxAdminPassword.Name = "txtBoxAdminPassword";
            this.txtBoxAdminPassword.PasswordChar = '*';
            this.txtBoxAdminPassword.ScrollBars = System.Windows.Forms.ScrollBars.None;
            this.txtBoxAdminPassword.SelectedText = "";
            this.txtBoxAdminPassword.SelectionLength = 0;
            this.txtBoxAdminPassword.SelectionStart = 0;
            this.txtBoxAdminPassword.Size = new System.Drawing.Size(260, 38);
            this.txtBoxAdminPassword.TabIndex = 8;
            this.txtBoxAdminPassword.TabStop = false;
            this.txtBoxAdminPassword.UseSystemPasswordChar = true;
            this.txtBoxAdminPassword.KeyDown += new System.Windows.Forms.KeyEventHandler(this.txtBoxAdminPassword_KeyDown);
            // 
            // txtBoxAdminAccount
            // 
            this.txtBoxAdminAccount.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.txtBoxAdminAccount.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(4)))), ((int)(((byte)(12)))), ((int)(((byte)(45)))));
            this.txtBoxAdminAccount.BaseColor = System.Drawing.Color.Transparent;
            this.txtBoxAdminAccount.BorderColorA = System.Drawing.Color.DodgerBlue;
            this.txtBoxAdminAccount.BorderColorB = System.Drawing.Color.DarkGray;
            this.txtBoxAdminAccount.Font = new System.Drawing.Font("Segoe UI", 12F);
            this.txtBoxAdminAccount.ForeColor = System.Drawing.Color.Gainsboro;
            this.txtBoxAdminAccount.Hint = "Account : email";
            this.txtBoxAdminAccount.Location = new System.Drawing.Point(12, 290);
            this.txtBoxAdminAccount.MaxLength = 25;
            this.txtBoxAdminAccount.Multiline = false;
            this.txtBoxAdminAccount.Name = "txtBoxAdminAccount";
            this.txtBoxAdminAccount.PasswordChar = '\0';
            this.txtBoxAdminAccount.ScrollBars = System.Windows.Forms.ScrollBars.None;
            this.txtBoxAdminAccount.SelectedText = "";
            this.txtBoxAdminAccount.SelectionLength = 0;
            this.txtBoxAdminAccount.SelectionStart = 0;
            this.txtBoxAdminAccount.Size = new System.Drawing.Size(260, 38);
            this.txtBoxAdminAccount.TabIndex = 7;
            this.txtBoxAdminAccount.TabStop = false;
            this.txtBoxAdminAccount.UseSystemPasswordChar = false;
            this.txtBoxAdminAccount.Click += new System.EventHandler(this.txtBoxAdminAccount_Click);
            this.txtBoxAdminAccount.KeyDown += new System.Windows.Forms.KeyEventHandler(this.txtBoxAdminAccount_KeyDown);
            // 
            // hopePictureBox1
            // 
            this.hopePictureBox1.Anchor = System.Windows.Forms.AnchorStyles.Top;
            this.hopePictureBox1.BackColor = System.Drawing.Color.Transparent;
            this.hopePictureBox1.Enabled = false;
            this.hopePictureBox1.Image = global::ReaLTaiizor.Login.Properties.Resources.Sam9moLogo;
            this.hopePictureBox1.Location = new System.Drawing.Point(41, 12);
            this.hopePictureBox1.Name = "hopePictureBox1";
            this.hopePictureBox1.PixelOffsetType = System.Drawing.Drawing2D.PixelOffsetMode.HighQuality;
            this.hopePictureBox1.Size = new System.Drawing.Size(200, 196);
            this.hopePictureBox1.SmoothingType = System.Drawing.Drawing2D.SmoothingMode.HighQuality;
            this.hopePictureBox1.TabIndex = 0;
            this.hopePictureBox1.TabStop = false;
            this.hopePictureBox1.TextRenderingType = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;
            // 
            // Login1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(96F, 96F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Dpi;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center;
            this.ClientSize = new System.Drawing.Size(773, 539);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.panel2);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Login1";
            this.Text = "Here You Can Login";
            this.TransparencyKey = System.Drawing.Color.Fuchsia;
            this.panel1.ResumeLayout(false);
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.hopePictureBox1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion
        private Controls.ParrotFormEllipse parrotFormEllipse1;
        private Controls.ParrotFormHandle parrotFormHandle1;
        private System.Windows.Forms.Panel panel2;
        private Controls.HopePictureBox hopePictureBox1;
        private Controls.ParrotFormHandle parrotFormHandle2;
        private Controls.HopeTextBox txtBoxAdminAccount;
        private Controls.HopeSwitch hopeSwitch1;
        private Controls.HopeTextBox txtBoxAdminPassword;
        private Controls.MaterialLabel materialLabel1;
        private Controls.MaterialButton btnAdminSignIn;
        private System.Windows.Forms.Panel panel1;
        private Controls.NightControlBox nightControlBox1;
        private Controls.FoxNotification notiBoxSignInError;
    }
}