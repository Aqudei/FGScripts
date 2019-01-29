using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.WindowsAPICodePack.Dialogs;

namespace DanielApp
{
    public partial class SettingsForm : Form
    {
        public SettingsForm()
        {
            InitializeComponent();
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            openFileDialog1.Filter = "TexturePath Executable File|Texture*.exe";

            var rslt = openFileDialog1.ShowDialog();
            if (rslt == DialogResult.OK)
            {
                labelExecutablePath.Text = openFileDialog1.FileName;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            openFileDialog1.Filter = "TexturePath Settings File|*.tps";

            var rslt = openFileDialog1.ShowDialog();
            if (rslt == DialogResult.OK)
            {
                textBoxLibGdxTps.Text = openFileDialog1.FileName;
            }
        }

        private void buttonBrowseSpriteKitTps_Click(object sender, EventArgs e)
        {
            openFileDialog1.Filter = "TexturePath Settings File|*.tps";

            var rslt = openFileDialog1.ShowDialog();
            if (rslt == DialogResult.OK)
            {
                textBoxSpriteKitTps.Text = openFileDialog1.FileName;
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            Properties.Settings.Default.DO_DEPOT = checkBoxDoDepot.Checked;
            Properties.Settings.Default.DEPOT_PATH = textBoxDepotPath.Text;

            Properties.Settings.Default.SKIP_RENAME = checkBoxSkipRename.Checked;
            Properties.Settings.Default.TP_EXECUTABLE_PATH = labelExecutablePath.Text;
            Properties.Settings.Default.LIBGDX_TPS_FILE = textBoxLibGdxTps.Text;
            Properties.Settings.Default.SPRITEKIT_TPS_FILE = textBoxSpriteKitTps.Text;

            Properties.Settings.Default.Save();
            MessageBox.Show(this, "Settings successfully saved!", "Success",
                MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void SettingsForm_Load(object sender, EventArgs e)
        {
            var tpExe = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), @"CodeAndWeb\TexturePacker\bin\TexturePacker.exe");
            tpExe = tpExe.Replace(" (x86)", "").Trim();
            if (!File.Exists(tpExe))
                tpExe = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), @"CodeAndWeb\TexturePacker\bin\TexturePacker.exe");
            if (File.Exists(tpExe))
            {
                labelExecutablePath.Text = tpExe;
                Properties.Settings.Default.TP_EXECUTABLE_PATH = tpExe;
                Properties.Settings.Default.Save();
            }
            else
                labelExecutablePath.Text = Properties.Settings.Default.TP_EXECUTABLE_PATH;

            textBoxLibGdxTps.Text = Properties.Settings.Default.LIBGDX_TPS_FILE;
            textBoxSpriteKitTps.Text = Properties.Settings.Default.SPRITEKIT_TPS_FILE;
            checkBoxSkipRename.Checked = Properties.Settings.Default.SKIP_RENAME;

            textBoxDepotPath.Text = Properties.Settings.Default.DEPOT_PATH;
            checkBoxDoDepot.Checked = Properties.Settings.Default.DO_DEPOT;
        }

        private void buttonDepot_Click(object sender, EventArgs e)
        {
            using (var ofd = new Microsoft.WindowsAPICodePack.Dialogs.CommonOpenFileDialog())
            {
                ofd.IsFolderPicker = true;
                ofd.Multiselect = false;

                var rslt = ofd.ShowDialog();
                if (rslt != CommonFileDialogResult.Ok)
                    return;

                textBoxDepotPath.Text = ofd.FileName;
            }
        }

        private void checkBoxDoDepot_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void checkBoxSkipRename_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
