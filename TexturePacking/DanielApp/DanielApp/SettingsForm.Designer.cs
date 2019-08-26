namespace DanielApp
{
    partial class SettingsForm
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
            this.label1 = new System.Windows.Forms.Label();
            this.textBoxLibGdxTps = new System.Windows.Forms.TextBox();
            this.labelExecutablePath = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.button1 = new System.Windows.Forms.Button();
            this.buttonBrowseSpriteKitTps = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.textBoxSpriteKitTps = new System.Windows.Forms.TextBox();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.checkBoxSkipRename = new System.Windows.Forms.CheckBox();
            this.buttonDepot = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.textBoxDepotPath = new System.Windows.Forms.TextBox();
            this.checkBoxDoDepot = new System.Windows.Forms.CheckBox();
            this.checkBoxPackAndroidLibGdx = new System.Windows.Forms.CheckBox();
            this.checkBoxPackIOSLibGdx = new System.Windows.Forms.CheckBox();
            this.label5 = new System.Windows.Forms.Label();
            this.textBoxLibGdxDataFileExtention = new System.Windows.Forms.TextBox();
            this.checkBoxPackAndroidSpritekit = new System.Windows.Forms.CheckBox();
            this.checkBoxPackIosSpriteKit = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(16, 11);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(210, 17);
            this.label1.TabIndex = 0;
            this.label1.Text = "TexturePacker Executable Path:";
            // 
            // textBoxLibGdxTps
            // 
            this.textBoxLibGdxTps.Location = new System.Drawing.Point(20, 97);
            this.textBoxLibGdxTps.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBoxLibGdxTps.Name = "textBoxLibGdxTps";
            this.textBoxLibGdxTps.Size = new System.Drawing.Size(665, 22);
            this.textBoxLibGdxTps.TabIndex = 1;
            // 
            // labelExecutablePath
            // 
            this.labelExecutablePath.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.labelExecutablePath.Location = new System.Drawing.Point(16, 41);
            this.labelExecutablePath.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.labelExecutablePath.Name = "labelExecutablePath";
            this.labelExecutablePath.Size = new System.Drawing.Size(671, 23);
            this.labelExecutablePath.TabIndex = 3;
            this.labelExecutablePath.Text = "[Please select path.]";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(16, 78);
            this.label3.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(110, 17);
            this.label3.TabIndex = 4;
            this.label3.Text = "LibGdx Tps File:";
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(695, 97);
            this.button1.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(68, 28);
            this.button1.TabIndex = 5;
            this.button1.Text = "Browse";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // buttonBrowseSpriteKitTps
            // 
            this.buttonBrowseSpriteKitTps.Location = new System.Drawing.Point(695, 154);
            this.buttonBrowseSpriteKitTps.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.buttonBrowseSpriteKitTps.Name = "buttonBrowseSpriteKitTps";
            this.buttonBrowseSpriteKitTps.Size = new System.Drawing.Size(68, 28);
            this.buttonBrowseSpriteKitTps.TabIndex = 8;
            this.buttonBrowseSpriteKitTps.Text = "Browse";
            this.buttonBrowseSpriteKitTps.UseVisualStyleBackColor = true;
            this.buttonBrowseSpriteKitTps.Click += new System.EventHandler(this.buttonBrowseSpriteKitTps_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(16, 134);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(119, 17);
            this.label4.TabIndex = 7;
            this.label4.Text = "SpriteKit Tps File:";
            // 
            // textBoxSpriteKitTps
            // 
            this.textBoxSpriteKitTps.Location = new System.Drawing.Point(20, 154);
            this.textBoxSpriteKitTps.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBoxSpriteKitTps.Name = "textBoxSpriteKitTps";
            this.textBoxSpriteKitTps.Size = new System.Drawing.Size(665, 22);
            this.textBoxSpriteKitTps.TabIndex = 6;
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            this.openFileDialog1.Filter = "TexturePacker Settings File|*.tps";
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(695, 41);
            this.button3.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(68, 28);
            this.button3.TabIndex = 9;
            this.button3.Text = "Browse";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // button4
            // 
            this.button4.Location = new System.Drawing.Point(400, 299);
            this.button4.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(363, 38);
            this.button4.TabIndex = 10;
            this.button4.Text = "Save Settings";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // checkBoxSkipRename
            // 
            this.checkBoxSkipRename.AutoSize = true;
            this.checkBoxSkipRename.Location = new System.Drawing.Point(206, 261);
            this.checkBoxSkipRename.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.checkBoxSkipRename.Name = "checkBoxSkipRename";
            this.checkBoxSkipRename.Size = new System.Drawing.Size(155, 21);
            this.checkBoxSkipRename.TabIndex = 11;
            this.checkBoxSkipRename.Text = "Skip Rename Step?";
            this.checkBoxSkipRename.UseVisualStyleBackColor = true;
            this.checkBoxSkipRename.CheckedChanged += new System.EventHandler(this.checkBoxSkipRename_CheckedChanged);
            // 
            // buttonDepot
            // 
            this.buttonDepot.Location = new System.Drawing.Point(691, 215);
            this.buttonDepot.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.buttonDepot.Name = "buttonDepot";
            this.buttonDepot.Size = new System.Drawing.Size(68, 28);
            this.buttonDepot.TabIndex = 14;
            this.buttonDepot.Text = "Browse";
            this.buttonDepot.UseVisualStyleBackColor = true;
            this.buttonDepot.Click += new System.EventHandler(this.buttonDepot_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 196);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(83, 17);
            this.label2.TabIndex = 13;
            this.label2.Text = "Depot Path:";
            // 
            // textBoxDepotPath
            // 
            this.textBoxDepotPath.Location = new System.Drawing.Point(16, 215);
            this.textBoxDepotPath.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBoxDepotPath.Name = "textBoxDepotPath";
            this.textBoxDepotPath.Size = new System.Drawing.Size(665, 22);
            this.textBoxDepotPath.TabIndex = 12;
            // 
            // checkBoxDoDepot
            // 
            this.checkBoxDoDepot.AutoSize = true;
            this.checkBoxDoDepot.Location = new System.Drawing.Point(20, 261);
            this.checkBoxDoDepot.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.checkBoxDoDepot.Name = "checkBoxDoDepot";
            this.checkBoxDoDepot.Size = new System.Drawing.Size(125, 21);
            this.checkBoxDoDepot.TabIndex = 15;
            this.checkBoxDoDepot.Text = "Depot Images?";
            this.checkBoxDoDepot.UseVisualStyleBackColor = true;
            this.checkBoxDoDepot.CheckedChanged += new System.EventHandler(this.checkBoxDoDepot_CheckedChanged);
            // 
            // checkBoxPackAndroidLibGdx
            // 
            this.checkBoxPackAndroidLibGdx.AutoSize = true;
            this.checkBoxPackAndroidLibGdx.Location = new System.Drawing.Point(20, 287);
            this.checkBoxPackAndroidLibGdx.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.checkBoxPackAndroidLibGdx.Name = "checkBoxPackAndroidLibGdx";
            this.checkBoxPackAndroidLibGdx.Size = new System.Drawing.Size(162, 21);
            this.checkBoxPackAndroidLibGdx.TabIndex = 17;
            this.checkBoxPackAndroidLibGdx.Text = "Pack Android LibGdx";
            this.checkBoxPackAndroidLibGdx.UseVisualStyleBackColor = true;
            // 
            // checkBoxPackIOSLibGdx
            // 
            this.checkBoxPackIOSLibGdx.AutoSize = true;
            this.checkBoxPackIOSLibGdx.Location = new System.Drawing.Point(206, 287);
            this.checkBoxPackIOSLibGdx.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.checkBoxPackIOSLibGdx.Name = "checkBoxPackIOSLibGdx";
            this.checkBoxPackIOSLibGdx.Size = new System.Drawing.Size(136, 21);
            this.checkBoxPackIOSLibGdx.TabIndex = 16;
            this.checkBoxPackIOSLibGdx.Text = "Pack IOS LibGdx";
            this.checkBoxPackIOSLibGdx.UseVisualStyleBackColor = true;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(406, 264);
            this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(174, 17);
            this.label5.TabIndex = 19;
            this.label5.Text = "LibGdx DataFile Extention:";
            // 
            // textBoxLibGdxDataFileExtention
            // 
            this.textBoxLibGdxDataFileExtention.Location = new System.Drawing.Point(588, 261);
            this.textBoxLibGdxDataFileExtention.Margin = new System.Windows.Forms.Padding(4);
            this.textBoxLibGdxDataFileExtention.Name = "textBoxLibGdxDataFileExtention";
            this.textBoxLibGdxDataFileExtention.Size = new System.Drawing.Size(171, 22);
            this.textBoxLibGdxDataFileExtention.TabIndex = 18;
            // 
            // checkBoxPackAndroidSpritekit
            // 
            this.checkBoxPackAndroidSpritekit.AutoSize = true;
            this.checkBoxPackAndroidSpritekit.Location = new System.Drawing.Point(20, 316);
            this.checkBoxPackAndroidSpritekit.Margin = new System.Windows.Forms.Padding(4);
            this.checkBoxPackAndroidSpritekit.Name = "checkBoxPackAndroidSpritekit";
            this.checkBoxPackAndroidSpritekit.Size = new System.Drawing.Size(171, 21);
            this.checkBoxPackAndroidSpritekit.TabIndex = 21;
            this.checkBoxPackAndroidSpritekit.Text = "Pack Android SpriteKit";
            this.checkBoxPackAndroidSpritekit.UseVisualStyleBackColor = true;
            // 
            // checkBoxPackIosSpriteKit
            // 
            this.checkBoxPackIosSpriteKit.AutoSize = true;
            this.checkBoxPackIosSpriteKit.Location = new System.Drawing.Point(206, 316);
            this.checkBoxPackIosSpriteKit.Margin = new System.Windows.Forms.Padding(4);
            this.checkBoxPackIosSpriteKit.Name = "checkBoxPackIosSpriteKit";
            this.checkBoxPackIosSpriteKit.Size = new System.Drawing.Size(145, 21);
            this.checkBoxPackIosSpriteKit.TabIndex = 20;
            this.checkBoxPackIosSpriteKit.Text = "Pack IOS SpriteKit";
            this.checkBoxPackIosSpriteKit.UseVisualStyleBackColor = true;
            // 
            // SettingsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(779, 365);
            this.Controls.Add(this.checkBoxPackAndroidSpritekit);
            this.Controls.Add(this.checkBoxPackIosSpriteKit);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.textBoxLibGdxDataFileExtention);
            this.Controls.Add(this.checkBoxPackAndroidLibGdx);
            this.Controls.Add(this.checkBoxPackIOSLibGdx);
            this.Controls.Add(this.checkBoxDoDepot);
            this.Controls.Add(this.buttonDepot);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.textBoxDepotPath);
            this.Controls.Add(this.checkBoxSkipRename);
            this.Controls.Add(this.button4);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.buttonBrowseSpriteKitTps);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.textBoxSpriteKitTps);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.labelExecutablePath);
            this.Controls.Add(this.textBoxLibGdxTps);
            this.Controls.Add(this.label1);
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "SettingsForm";
            this.Text = "SettingsForm";
            this.Load += new System.EventHandler(this.SettingsForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBoxLibGdxTps;
        private System.Windows.Forms.Label labelExecutablePath;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button buttonBrowseSpriteKitTps;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox textBoxSpriteKitTps;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.CheckBox checkBoxSkipRename;
        private System.Windows.Forms.Button buttonDepot;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox textBoxDepotPath;
        private System.Windows.Forms.CheckBox checkBoxDoDepot;
        private System.Windows.Forms.CheckBox checkBoxPackAndroidLibGdx;
        private System.Windows.Forms.CheckBox checkBoxPackIOSLibGdx;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox textBoxLibGdxDataFileExtention;
        private System.Windows.Forms.CheckBox checkBoxPackAndroidSpritekit;
        private System.Windows.Forms.CheckBox checkBoxPackIosSpriteKit;
    }
}