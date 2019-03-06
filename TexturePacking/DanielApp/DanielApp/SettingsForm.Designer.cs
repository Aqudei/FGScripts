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
            this.checkBoxPackAndroid = new System.Windows.Forms.CheckBox();
            this.checkBoxPackIOS = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(161, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "TexturePacker Executable Path:";
            // 
            // textBoxLibGdxTps
            // 
            this.textBoxLibGdxTps.Location = new System.Drawing.Point(15, 79);
            this.textBoxLibGdxTps.Name = "textBoxLibGdxTps";
            this.textBoxLibGdxTps.Size = new System.Drawing.Size(500, 20);
            this.textBoxLibGdxTps.TabIndex = 1;
            // 
            // labelExecutablePath
            // 
            this.labelExecutablePath.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.labelExecutablePath.Location = new System.Drawing.Point(12, 33);
            this.labelExecutablePath.Name = "labelExecutablePath";
            this.labelExecutablePath.Size = new System.Drawing.Size(503, 19);
            this.labelExecutablePath.TabIndex = 3;
            this.labelExecutablePath.Text = "[Please select path.]";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 63);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(83, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "LibGdx Tps File:";
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(521, 79);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(51, 23);
            this.button1.TabIndex = 5;
            this.button1.Text = "Browse";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // buttonBrowseSpriteKitTps
            // 
            this.buttonBrowseSpriteKitTps.Location = new System.Drawing.Point(521, 125);
            this.buttonBrowseSpriteKitTps.Name = "buttonBrowseSpriteKitTps";
            this.buttonBrowseSpriteKitTps.Size = new System.Drawing.Size(51, 23);
            this.buttonBrowseSpriteKitTps.TabIndex = 8;
            this.buttonBrowseSpriteKitTps.Text = "Browse";
            this.buttonBrowseSpriteKitTps.UseVisualStyleBackColor = true;
            this.buttonBrowseSpriteKitTps.Click += new System.EventHandler(this.buttonBrowseSpriteKitTps_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 109);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(89, 13);
            this.label4.TabIndex = 7;
            this.label4.Text = "SpriteKit Tps File:";
            // 
            // textBoxSpriteKitTps
            // 
            this.textBoxSpriteKitTps.Location = new System.Drawing.Point(15, 125);
            this.textBoxSpriteKitTps.Name = "textBoxSpriteKitTps";
            this.textBoxSpriteKitTps.Size = new System.Drawing.Size(500, 20);
            this.textBoxSpriteKitTps.TabIndex = 6;
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            this.openFileDialog1.Filter = "TexturePacker Settings File|*.tps";
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(521, 33);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(51, 23);
            this.button3.TabIndex = 9;
            this.button3.Text = "Browse";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // button4
            // 
            this.button4.Location = new System.Drawing.Point(300, 204);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(272, 31);
            this.button4.TabIndex = 10;
            this.button4.Text = "Save Settings";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // checkBoxSkipRename
            // 
            this.checkBoxSkipRename.AutoSize = true;
            this.checkBoxSkipRename.Location = new System.Drawing.Point(132, 212);
            this.checkBoxSkipRename.Name = "checkBoxSkipRename";
            this.checkBoxSkipRename.Size = new System.Drawing.Size(121, 17);
            this.checkBoxSkipRename.TabIndex = 11;
            this.checkBoxSkipRename.Text = "Skip Rename Step?";
            this.checkBoxSkipRename.UseVisualStyleBackColor = true;
            this.checkBoxSkipRename.CheckedChanged += new System.EventHandler(this.checkBoxSkipRename_CheckedChanged);
            // 
            // buttonDepot
            // 
            this.buttonDepot.Location = new System.Drawing.Point(518, 175);
            this.buttonDepot.Name = "buttonDepot";
            this.buttonDepot.Size = new System.Drawing.Size(51, 23);
            this.buttonDepot.TabIndex = 14;
            this.buttonDepot.Text = "Browse";
            this.buttonDepot.UseVisualStyleBackColor = true;
            this.buttonDepot.Click += new System.EventHandler(this.buttonDepot_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(9, 159);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(64, 13);
            this.label2.TabIndex = 13;
            this.label2.Text = "Depot Path:";
            // 
            // textBoxDepotPath
            // 
            this.textBoxDepotPath.Location = new System.Drawing.Point(12, 175);
            this.textBoxDepotPath.Name = "textBoxDepotPath";
            this.textBoxDepotPath.Size = new System.Drawing.Size(500, 20);
            this.textBoxDepotPath.TabIndex = 12;
            // 
            // checkBoxDoDepot
            // 
            this.checkBoxDoDepot.AutoSize = true;
            this.checkBoxDoDepot.Location = new System.Drawing.Point(15, 212);
            this.checkBoxDoDepot.Name = "checkBoxDoDepot";
            this.checkBoxDoDepot.Size = new System.Drawing.Size(98, 17);
            this.checkBoxDoDepot.TabIndex = 15;
            this.checkBoxDoDepot.Text = "Depot Images?";
            this.checkBoxDoDepot.UseVisualStyleBackColor = true;
            this.checkBoxDoDepot.CheckedChanged += new System.EventHandler(this.checkBoxDoDepot_CheckedChanged);
            // 
            // checkBoxPackAndroid
            // 
            this.checkBoxPackAndroid.AutoSize = true;
            this.checkBoxPackAndroid.Location = new System.Drawing.Point(15, 243);
            this.checkBoxPackAndroid.Name = "checkBoxPackAndroid";
            this.checkBoxPackAndroid.Size = new System.Drawing.Size(90, 17);
            this.checkBoxPackAndroid.TabIndex = 17;
            this.checkBoxPackAndroid.Text = "Pack Android";
            this.checkBoxPackAndroid.UseVisualStyleBackColor = true;
            // 
            // checkBoxPackIOS
            // 
            this.checkBoxPackIOS.AutoSize = true;
            this.checkBoxPackIOS.Location = new System.Drawing.Point(132, 243);
            this.checkBoxPackIOS.Name = "checkBoxPackIOS";
            this.checkBoxPackIOS.Size = new System.Drawing.Size(72, 17);
            this.checkBoxPackIOS.TabIndex = 16;
            this.checkBoxPackIOS.Text = "Pack IOS";
            this.checkBoxPackIOS.UseVisualStyleBackColor = true;
            // 
            // SettingsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(584, 272);
            this.Controls.Add(this.checkBoxPackAndroid);
            this.Controls.Add(this.checkBoxPackIOS);
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
        private System.Windows.Forms.CheckBox checkBoxPackAndroid;
        private System.Windows.Forms.CheckBox checkBoxPackIOS;
    }
}