using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Forms.VisualStyles;
using CommandLine;
using CsvHelper;

namespace DanielApp
{
    public partial class MainForm : Form
    {
        private readonly Regex _regex = new Regex(@"(\d\d\-\d\d\d_.+)[\\/]?");
        private List<Real3DV1> _real3DConfig;

        public MainForm()
        {
            InitializeComponent();
        }

        private void buttonClear_Click(object sender, EventArgs e)
        {
            listBoxFolders.Items.Clear();
        }

        private void buttonRemove_Click(object sender, EventArgs e)
        {
            var selected = listBoxFolders.SelectedItem;
            if (selected == null)
                return;
            listBoxFolders.Items.Remove(selected);
        }

        private void buttonNew_Click(object sender, EventArgs e)
        {
            using (var ofd = new Microsoft.WindowsAPICodePack.Dialogs.CommonOpenFileDialog())
            {
                ofd.IsFolderPicker = true;
                ofd.Multiselect = true;


                var rslt = ofd.ShowDialog();

                if (rslt != Microsoft.WindowsAPICodePack.Dialogs.CommonFileDialogResult.Ok)
                    return;

                foreach (var selectedPath in ofd.FileNames)
                {
                    if (listBoxFolders.Items.Contains(selectedPath))
                        return;

                    listBoxFolders.Items.Add(selectedPath);
                }
            }
        }

        private void buttonRunPacker_Click(object sender, EventArgs e)
        {
            if (listBoxFolders.Items.Count <= 0)
                return;

            progressBar1.Visible = true;
            collectSpriteBackgroundWorker.RunWorkerAsync();
        }

        private string FindFile(string directory, string pattern)
        {
            var files = Directory.GetFiles(directory, pattern);
            return files.Length > 0 ? files[0] : null;
        }

        private void CreateOutputDirectories(string folder)
        {
            Directory.CreateDirectory(Path.Combine(folder, "V5", "Output", "HD", "libgdx"));
            Directory.CreateDirectory(Path.Combine(folder, "V5", "Output", "HD", "SpriteKit"));
            Directory.CreateDirectory(Path.Combine(folder, "V5", "Output", "SD", "libgdx"));
            Directory.CreateDirectory(Path.Combine(folder, "V5", "Output", "SD", "SpriteKit"));
        }

        private void CopySongsCSVPartsFeature(string folder)
        {
            //Copy Parts, Features, song, sav to V5
            var files = Directory.GetFiles(folder, "*.*", SearchOption.TopDirectoryOnly);
            foreach (var file in files) File.Copy(file, Path.Combine(folder, "V5", Path.GetFileName(file)), true);
        }

        private void CreateV5TopDirectories(string folder)
        {
            //Create V5 Directories    
            Debug.WriteLine("Creating V5 Directories");
            Directory.CreateDirectory(Path.Combine(folder, "V5", "PACKSOURCE", "HD", "Frame0"));
            Directory.CreateDirectory(Path.Combine(folder, "V5", "PACKSOURCE", "HD", "Frame1"));
            Directory.CreateDirectory(Path.Combine(folder, "V5", "PACKSOURCE", "SD", "Frame0"));
            Directory.CreateDirectory(Path.Combine(folder, "V5", "PACKSOURCE", "SD", "Frame1"));
        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            foreach (string inputFolder in listBoxFolders.Items)
                try
                {
                    var v5Dir = Path.Combine(inputFolder, "V5");
                    if (Directory.Exists(v5Dir))
                    {
                        Debug.WriteLine("Removing old files...");
                        Directory.Delete(v5Dir, true);
                    }

                    var outputSDDirectory = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD");
                    var outputHDDirectory = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD");

                    var partCsvFilename = FindFile(inputFolder, "*_Parts.csv");
                    if (partCsvFilename == null) throw new Exception("Parts.csv was not found");

                    var partsCsv = new PartsCsv(partCsvFilename);

                    var featuresCsvFile = FindFile(inputFolder, "*_Features.csv");
                    if (featuresCsvFile == null) throw new Exception("Features.csv was not found");

                    CreateV5TopDirectories(inputFolder);

                    CopyFrames("SD", partsCsv, inputFolder);
                    CopyFrames("HD", partsCsv, inputFolder);
                    CopyUIImages("_UI", inputFolder);
                    CopyUIImages("_UI - LD", inputFolder);

                    if (!Properties.Settings.Default.SKIP_RENAME)
                    {
                        RenamePointToDash(outputSDDirectory);
                        RenamePointToDash(outputHDDirectory);
                    }

                    CopySongsCSVPartsFeature(inputFolder);
                    CreateOutputDirectories(inputFolder);

                }
                catch (Exception exception)
                {
                    Debug.WriteLine(exception);
                    Debug.WriteLine($"Error in folder {inputFolder}");
                    Debug.WriteLine(exception.Message);
                    Debug.WriteLine(exception.StackTrace);
                    Debug.WriteLine($"Error in folder {inputFolder}");
                }
        }

        private void RenamePointToDash(string outputSDDirectory)
        {
            var array = Directory.GetFiles(outputSDDirectory, "*.png", SearchOption.AllDirectories);
            for (var i = array.Length; i-- > 0;)
            {
                var file = array[i];

                var dirName = Path.GetDirectoryName(file);
                var filename = Path.GetFileName(file).ReplaceFirst(".", "-");
                File.Move(file, Path.Combine(dirName, filename));
            }

            array = Directory.GetFiles(outputSDDirectory, "*-png", SearchOption.AllDirectories);
            for (var i = array.Length; i-- > 0;)
            {
                var file = array[i];
                var output = file.Replace("-png", ".png");
                File.Move(file, output);
            }
        }

        private void CopyUIImages(string folderEndsWith, string inputFolder)
        {


            var rgx = new Regex(@"_(\d+)\.png", RegexOptions.IgnoreCase);

            var uiDir = FindDirectoryEndingIn(folderEndsWith, inputFolder);
            if (uiDir == null) throw new Exception($"No UI directories in {inputFolder}");

            Debug.WriteLine($"Copying UI images from folder: {uiDir}");

            var files = Directory.GetFiles(uiDir, "*.png", SearchOption.AllDirectories);
            foreach (var file in files)
            {
                var filename = file;

                if (file.Contains("_temp"))
                    continue;
                if (file.Contains("Tab_BG"))
                    continue;

                if (!Properties.Settings.Default.SKIP_RENAME)
                {
                    var rslt = rgx.Match(file);
                    if (rslt.Success)
                        filename = rgx.Replace(file, $"-{rslt.Groups[1].Value}.png");
                }

                var res = folderEndsWith.Trim() == "_UI" ? "HD" : "SD";
                File.Copy(file, Path.Combine(inputFolder, "V5", "PACKSOURCE",
                    res, "Frame0", Path.GetFileName(filename)), true);
            }
        }

        private void CopyFrames(string resolution, PartsCsv partsCsv, string inputFolder)
        {
            Debug.WriteLine($"Processing folder: {inputFolder}, resolution: {resolution}");
            resolution = resolution.ToUpper();

            var SHD_sourceFolder = FindDirectoryEndingIn($"-{resolution}", inputFolder);
            var files = Directory.GetFiles(SHD_sourceFolder, "*.png");

            foreach (var file in files)
            {
                var frame = FrameFile.Parse(file);
                if (frame == null)
                    continue;

                if (!partsCsv.ShouldCopy(frame.Model))
                    continue;

                var frame0 = "";
                var modelName = GetModelName(inputFolder);
                var modelConfig = _real3DConfig.FirstOrDefault(dv1 => dv1.Model == modelName);
                if (modelConfig != null && !string.IsNullOrWhiteSpace(modelConfig.FrameSetup))
                {
                    var tmp = modelConfig.FrameSetup.Split(",".ToCharArray());
                    frame0 = $".{tmp[2].Trim()}.";
                }
                else
                {
                    frame0 = ".8.";
                }

                if (file.Contains(frame0))
                    File.Copy(file, Path.Combine(inputFolder, "V5", "PACKSOURCE", resolution,
                        "Frame0", Path.GetFileName(file)), true);
                else
                    File.Copy(file, Path.Combine(inputFolder, "V5", "PACKSOURCE", resolution,
                        "Frame1", Path.GetFileName(file)), true);
            }
        }

        private string FindDirectoryEndingIn(string folderEndsWith, string inputFolder)
        {
            var dirs = Directory.GetDirectories(inputFolder, $"*{folderEndsWith}");
            if (dirs != null && dirs.Length > 0)
                foreach (var dir in dirs)
                    if (dir.EndsWith(folderEndsWith))
                        return dir;

            return null;
        }

        private void collectSpritesBackgroundWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (e.Result != null) //something went wrong
            {
                progressBar1.Visible = true;
                Debug.WriteLine("Processing done...");
                return;
            }

            backgroundWorkerRunTexturePacker.RunWorkerAsync();

        }


        private void button1_Click(object sender, EventArgs e)
        {
            using (var settings = new SettingsForm())
            {
                settings.ShowDialog();
            }
        }

        public void PullFilesToTopDirectory(string inputFolder)
        {
            var files = Directory.GetFiles(inputFolder, "*.*", SearchOption.AllDirectories);
            foreach (var file in files)
            {
                var destination = Path.Combine(inputFolder, Path.GetFileName(file));
                File.Copy(file, destination, true);
                File.Delete(file);
            }
        }

        private void backgroundWorkerRunTexturePacker_DoWork(object sender, DoWorkEventArgs e)
        {
            var tpExecutable = Properties.Settings.Default.TP_EXECUTABLE_PATH;
            if (File.Exists(tpExecutable) == false)
            {
                Debug.WriteLine("No tp executable file found!");
                BeginInvoke(new Action(() =>
                {
                    MessageBox.Show(this, "No tp executable file found!", "Error",
                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                }));

                return;
            }
            Debug.WriteLine("TP Executable Found!");

            var libgdxTps = Properties.Settings.Default.LIBGDX_TPS_FILE;
            if (File.Exists(libgdxTps) == false)
            {
                Debug.WriteLine("No libgdx tps file found!");
                MessageBox.Show(this, "No libgdx tps file found!", "Error",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            Debug.WriteLine("Libgdx settings file Found!");

            var spritekittps = Properties.Settings.Default.SPRITEKIT_TPS_FILE;
            if (File.Exists(spritekittps) == false)
            {
                Debug.WriteLine("No sprite-kit tps file found!");
                MessageBox.Show(this, "No sprite-kit tps file found!", "Error",
                   MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            var rgxModel = new Regex(@"(.*)_Model");
            foreach (string inputFolder in listBoxFolders.Items)
            {
                Debug.WriteLine("Processing " + inputFolder);

                var dirs = Directory.GetDirectories(inputFolder, "*_Model*", SearchOption.TopDirectoryOnly);
                if (dirs.Length <= 0)
                    continue;
                var rslt = rgxModel.Match(Path.GetFileName(dirs.First()));
                if (rslt.Success == false)
                {
                    Debug.WriteLine("Model name cannot be inferred from " + inputFolder);
                    MessageBox.Show(this, "Model name cannot be inferred from " + inputFolder,
                        "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    continue;
                }

                var modelName = rslt.Groups[1].Value;
                Debug.WriteLine("Model name found : " + modelName);
                Debug.WriteLine($"Running TexturePacker on {inputFolder} with Model Name: {modelName}");

                LibGdxPacker(tpExecutable, libgdxTps, inputFolder, modelName);
                SpriteKit(tpExecutable, spritekittps, inputFolder, modelName);
            }
        }

        //private void SpriteKit(string tpExecutable, string tps, string inputFolder, string modelName)
        //{
        //    var sdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame0");
        //    var sdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame1");
        //    var hdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame0");
        //    var hdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame1");

        //    var outputSpriteKitSDFrame01 = Path.Combine(inputFolder, "V5", "Output", "SD", "SpriteKit");
        //    var outputSpriteKitHDFrame01 = Path.Combine(inputFolder, "V5", "Output", "HD", "SpriteKit");

        //    Debug.WriteLine("Packing SpriteKit Frame0 SD...");
        //    Debug.WriteLine($"SpriteKit Packing: {sdFrame0}");
        //    var p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitSDFrame01 + "/" + modelName + "_Pack0.atlasc"}\" \"{sdFrame0}\" \"{tps}\"");
        //    p.WaitForExit();

        //    Debug.WriteLine("Packing SpriteKit Frame1 SD...");
        //    Debug.WriteLine($"SpriteKit Packing: {sdFrame1}");
        //    p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitSDFrame01 + "/" + modelName + "_Pack1.atlasc"}\" \"{sdFrame1}\" \"{tps}\"");
        //    p.WaitForExit();

        //    Debug.WriteLine("Packing SpriteKit Frame0 HD...");
        //    Debug.WriteLine($"SpriteKit Packing: {hdFrame0}");
        //    p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitHDFrame01 + "/" + modelName + "_Pack0.atlasc"}\" \"{hdFrame0}\" \"{tps}\"");
        //    p.WaitForExit();

        //    Debug.WriteLine("Packing SpriteKit Frame1 HD...");
        //    Debug.WriteLine($"SpriteKit Packing: {hdFrame1}");
        //    p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitHDFrame01 + "/" + modelName + "_Pack1.atlasc"}\" \"{hdFrame1}\" \"{tps}\"");
        //    p.WaitForExit();
        //}

        //private void LibGdxPacker(string tpExecutable, string tpsFile, string inputFolder, string modelName)
        //{
        //    var sdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame0");
        //    var sdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame1");
        //    var hdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame0");
        //    var hdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame1");

        //    var outputLibgdxSDFrame01 = Path.Combine(inputFolder, "V5", "Output", "SD", "libgdx");
        //    var outputLibgdxHDFrame01 = Path.Combine(inputFolder, "V5", "Output", "HD", "libgdx");

        //    Debug.WriteLine("Packing Libgdx Frame0 SD...");
        //    Debug.WriteLine($"LibGDX Packing: {sdFrame0}");
        //    var p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxSDFrame01 + "/" + modelName + "_Pack0-{n}.png"}\" --data \"{outputLibgdxSDFrame01 + "/" + modelName + "_Pack0.atlas"}\" \"{sdFrame0}\" \"{tpsFile}\"");
        //    p.WaitForExit();

        //    Debug.WriteLine("Packing Libgdx Frame1 SD...");
        //    Debug.WriteLine($"LibGDX Packing: {sdFrame1}");
        //    p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxSDFrame01 + "/" + modelName + "_Pack1-{n}.png"}\" --data \"{outputLibgdxSDFrame01 + "/" + modelName + "_Pack1.atlas"}\" \"{sdFrame1}\" \"{tpsFile}\"");
        //    p.WaitForExit();

        //    Debug.WriteLine("Packing Libgdx Frame0 HD...");
        //    Debug.WriteLine($"LibGDX Packing: {hdFrame0}");
        //    p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack0-{n}.png"}\" --data \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack0.atlas"}\" \"{hdFrame0}\" \"{tpsFile}\"");
        //    p.WaitForExit();

        //    Debug.WriteLine("Packing Libgdx Frame1 HD...");
        //    Debug.WriteLine($"LibGDX Packing: {hdFrame1}");
        //    p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack1-{n}.png"}\" --data \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack1.atlas"}\" \"{hdFrame1}\" \"{tpsFile}\"");
        //    p.WaitForExit();
        //}


        private void SpriteKit(string tpExecutable, string tps, string inputFolder, string modelName)
        {
            var sdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame0");
            var sdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame1");
            var hdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame0");
            var hdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame1");

            var outputSpriteKitSDFrame01 = Path.Combine(inputFolder, "V5", "Output", "SD", "SpriteKit");
            var outputSpriteKitHDFrame01 = Path.Combine(inputFolder, "V5", "Output", "HD", "SpriteKit");

            Debug.WriteLine("Packing SpriteKit Frame0 SD...");
            Debug.WriteLine($"SpriteKit Packing: {sdFrame0}");
            var p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitSDFrame01 + "/" + modelName + "-SD_Pack0.atlasc"}\" \"{sdFrame0}\" \"{tps}\"");
            p.WaitForExit();

            Debug.WriteLine("Packing SpriteKit Frame1 SD...");
            Debug.WriteLine($"SpriteKit Packing: {sdFrame1}");
            p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitSDFrame01 + "/" + modelName + "-SD_Pack1.atlasc"}\" \"{sdFrame1}\" \"{tps}\"");
            p.WaitForExit();

            Debug.WriteLine("Packing SpriteKit Frame0 HD...");
            Debug.WriteLine($"SpriteKit Packing: {hdFrame0}");
            p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitHDFrame01 + "/" + modelName + "_Pack0.atlasc"}\" \"{hdFrame0}\" \"{tps}\"");
            p.WaitForExit();

            Debug.WriteLine("Packing SpriteKit Frame1 HD...");
            Debug.WriteLine($"SpriteKit Packing: {hdFrame1}");
            p = Process.Start($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitHDFrame01 + "/" + modelName + "_Pack1.atlasc"}\" \"{hdFrame1}\" \"{tps}\"");
            p.WaitForExit();
        }

        private void LibGdxPacker(string tpExecutable, string tpsFile, string inputFolder, string modelName)
        {
            var sdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame0");
            var sdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame1");
            var hdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame0");
            var hdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame1");

            var outputLibgdxSDFrame01 = Path.Combine(inputFolder, "V5", "Output", "SD", "libgdx");
            var outputLibgdxHDFrame01 = Path.Combine(inputFolder, "V5", "Output", "HD", "libgdx");

            Debug.WriteLine("Packing Libgdx Frame0 SD...");
            Debug.WriteLine($"LibGDX Packing: {sdFrame0}");
            var p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxSDFrame01 + "/" + modelName + "-SD_Pack0-{n}.png"}\" --data \"{outputLibgdxSDFrame01 + "/" + modelName + "-SD_Pack0.atlas"}\" \"{sdFrame0}\" \"{tpsFile}\"");
            p.WaitForExit();

            Debug.WriteLine("Packing Libgdx Frame1 SD...");
            Debug.WriteLine($"LibGDX Packing: {sdFrame1}");
            p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxSDFrame01 + "/" + modelName + "-SD_Pack1-{n}.png"}\" --data \"{outputLibgdxSDFrame01 + "/" + modelName + "-SD_Pack1.atlas"}\" \"{sdFrame1}\" \"{tpsFile}\"");
            p.WaitForExit();

            Debug.WriteLine("Packing Libgdx Frame0 HD...");
            Debug.WriteLine($"LibGDX Packing: {hdFrame0}");
            p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack0-{n}.png"}\" --data \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack0.atlas"}\" \"{hdFrame0}\" \"{tpsFile}\"");
            p.WaitForExit();

            Debug.WriteLine("Packing Libgdx Frame1 HD...");
            Debug.WriteLine($"LibGDX Packing: {hdFrame1}");
            p = Process.Start($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack1-{n}.png"}\" --data \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack1.atlas"}\" \"{hdFrame1}\" \"{tpsFile}\"");
            p.WaitForExit();
        }

        private string GetModelName(string fromFolder)
        {
            var rgx = new Regex(@"(.*)_Model");
            foreach (var directory in Directory.GetDirectories(fromFolder, "*_Model*", SearchOption.TopDirectoryOnly))
            {
                var rslt = rgx.Match(Path.GetFileName(directory));
                if (rslt.Success) return rslt.Groups[1].Value;
            }

            return null;
        }

        private void RunDepot()
        {
            Process process;
            if (listBoxFolders.Items.Count <= 0)
            {
                Debug.WriteLine("[Depot] No folders to processed...");
                return;
            }

            if (Properties.Settings.Default.DO_DEPOT &&
                !string.IsNullOrWhiteSpace(Properties.Settings.Default.DEPOT_PATH))
            {
                var depotPath = Properties.Settings.Default.DEPOT_PATH;
                if (Directory.Exists(depotPath))
                    foreach (string inputFolder in listBoxFolders.Items)
                    {
                        var outputFolder = Path.Combine(inputFolder, "V5", "Output");
                        if (Directory.Exists(outputFolder))
                        {
                            Debug.WriteLine($"[Depot] Copying files from {outputFolder} to {depotPath}\n");
                            process = Process.Start("robocopy", $"\"{outputFolder}\" \"{depotPath}\" /MIR");
                            process.WaitForExit();
                            process.Close();
                        }

                        Debug.WriteLine("[Depot] Copying files from SAVE, MP3 and CSV files\n");
                        process = Process.Start("robocopy", $"\"{inputFolder}\" \"{depotPath}\" *.sav *.csv *.mp3");
                        process.WaitForExit();
                        process.Close();

                        //foreach (var file in Directory.GetFiles(inputFolder, "*.*"))
                        //{
                        //    Debug.WriteLine("[Depot] Copying files from SAVE, MP3 and CSV files\n");
                        //    process = Process.Start("robocopy", $"\"{inputFolder}\" \"{depotPath}\" *.sav *.csv *.mp3");
                        //    process.WaitForExit();
                        //    process.Close();
                        //    //File.Copy(file, Path.Combine(depotPath, Path.GetFileName(file)), true);
                        //}

                        var modelName = GetModelName(inputFolder);
                        if (!string.IsNullOrWhiteSpace(modelName))
                        {
                            var iconFolder = Path.Combine(inputFolder, modelName);
                            if (Directory.Exists(iconFolder))
                            {
                                Directory.CreateDirectory(Path.Combine(depotPath, modelName));
                                Debug.WriteLine($"[Depot] Copying icon files from {iconFolder} to {depotPath}\n");
                                process = Process.Start("robocopy", $"\"{iconFolder}\" \"{Path.Combine(depotPath, modelName)}\" /MIR");
                                process.WaitForExit();
                                process.Close();
                            }
                        }
                    }
            }
        }

        private void backgroundWorkerRunTexturePacker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            progressBar1.Visible = false;
            if (e.Result == null)
            {
                RunDepot();
                Debug.WriteLine("Processing done...");
                return;
            }

            Debug.WriteLine("Processing ended with error/s...");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            progressBar1.Visible = true;
            backgroundWorkerRunTexturePacker.RunWorkerAsync();
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            RunDepot();
        }

        private void button2_Click_2(object sender, EventArgs e)
        {
            RunDepot();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            Debug.Listeners.Add(new DebugTextListener(richTextBoxLogs));

            Task.Run(() =>
            {
                Parser.Default.ParseArguments<Options>(Environment.GetCommandLineArgs())
                    .WithParsed(options =>
                    {
                        _real3DConfig = new List<Real3DV1>();

                        if (string.IsNullOrWhiteSpace(options.StartDirectory))
                            return;

                        if (!Directory.Exists(options.StartDirectory))
                            return;

                        using (var streamReader = new StreamReader(Path.Combine(options.StartDirectory, "Real3d_V1.csv")))
                        using (var csv = new CsvReader(streamReader))
                        {
                            csv.Configuration.PrepareHeaderForMatch = (s, i) => s.Replace(" ", "").ToLower().Trim();
                            var config = csv.GetRecords<Real3DV1>().ToList();
                            _real3DConfig.AddRange(config.Where(dv1 => dv1.IsReady == 1));
                        }

                        if (!_real3DConfig.Any())
                            return;

                        var dirs = Directory.GetDirectories(options.StartDirectory);
                        foreach (var dir in dirs)
                        {
                            var modelName = ParseModelName(dir);

                            if (_real3DConfig.All(dv1 => dv1.Model.Trim() != modelName.Trim()))
                                continue;

                            if (!string.IsNullOrWhiteSpace(modelName))
                                listBoxFolders.BeginInvoke(new Action(() =>
                                {
                                    listBoxFolders.Items.Add(Path.Combine(dir, "KeyShot", "Renders", modelName));
                                }));
                        }

                        buttonRunPacker.BeginInvoke(new Action(() =>
                        {
                            buttonRunPacker.PerformClick();
                        }));
                    });
            });

        }



        private string ParseModelName(string dirName)
        {
            var rslt = _regex.Match(dirName);
            return !rslt.Success ? string.Empty : rslt.Groups[1].Value.Trim();
        }
    }
}
