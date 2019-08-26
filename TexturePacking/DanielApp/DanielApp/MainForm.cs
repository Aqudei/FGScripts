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
using Newtonsoft.Json;

namespace DanielApp
{
    public partial class MainForm : Form
    {

        private List<Real3DV1> _real3DConfig;
        private string _csvLocation;

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
            if (Properties.Settings.Default.PACK_ANDROID)
            {
                CreateCleanDirectory(Path.Combine(folder, "V5", "Output"));
                CreateCleanDirectory(Path.Combine(folder, "V5", "Output", "HD", "libgdx"));
                CreateCleanDirectory(Path.Combine(folder, "V5", "Output", "HD", "SpriteKit"));
                CreateCleanDirectory(Path.Combine(folder, "V5", "Output", "SD", "libgdx"));
                CreateCleanDirectory(Path.Combine(folder, "V5", "Output", "SD", "SpriteKit"));
            }

            //if (Properties.Settings.Default.PACK_IOS)
            //{
            //    CreateCleanDirectory(Path.Combine(folder, "V5", "OutputIOS"));
            //    CreateCleanDirectory(Path.Combine(folder, "V5", "OutputIOS", "HD", "libgdx"));
            //    CreateCleanDirectory(Path.Combine(folder, "V5", "OutputIOS", "HD", "SpriteKit"));
            //    CreateCleanDirectory(Path.Combine(folder, "V5", "OutputIOS", "SD", "libgdx"));
            //    CreateCleanDirectory(Path.Combine(folder, "V5", "OutputIOS", "SD", "SpriteKit"));
            //}
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

        private void CollectSpritesBackgroundWorker_DoWork(object sender, DoWorkEventArgs e)
        {
            foreach (string inputFolder in listBoxFolders.Items)
                try
                {
                    if (Properties.Settings.Default.PACK_ANDROID)
                    {
                        PrepareAndroidPacking(inputFolder);
                    }

                    if (Properties.Settings.Default.PACK_IOS)
                    {
                        PrepareIosPacking(inputFolder);
                    }

                }
                catch (Exception exception)
                {
                    Debug.WriteLine(exception.Message);
                    Debug.WriteLine($"Error:In folder {inputFolder}. Moving on to next model.");
                }
        }

        private void PrepareAndroidPacking(string inputFolder)
        {
            var v5Dir = Path.Combine(inputFolder, "V5");

            if (Directory.Exists(v5Dir) && Properties.Settings.Default.PACK_ANDROID)
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
                Debug.WriteLine("Not running LigGdx/SpriteKit.");
                Debug.WriteLine("Processing done.");
                return;
            }

            backgroundWorkerRunTexturePacker.RunWorkerAsync();
        }

        private void ShowSettingsButton_Clicked(object sender, EventArgs e)
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
                Debug.WriteLine("No TexturePacker executable file found!");
                return;
            }

            Debug.WriteLine("TexturePacker Executable Found!");

            var libgdxTps = Properties.Settings.Default.LIBGDX_TPS_FILE;
            if (File.Exists(libgdxTps) == false)
            {
                Debug.WriteLine(@"Error: No libgdx TPS file found!");
                return;
            }
            Debug.WriteLine("Libgdx settings file Found!");

            var spritekittps = Properties.Settings.Default.SPRITEKIT_TPS_FILE;
            if (File.Exists(spritekittps) == false)
            {
                Debug.WriteLine("Error: No sprite-kit tps file found!");
                return;
            }

            var rgxModel = new Regex(@"(.*)_Model");
            foreach (string inputFolder in listBoxFolders.Items)
            {
                Debug.WriteLine("Packing " + inputFolder);

                var dirs = Directory.GetDirectories(inputFolder, "*_Model*", SearchOption.TopDirectoryOnly);
                if (dirs.Length <= 0)
                    continue;
                var rslt = rgxModel.Match(Path.GetFileName(dirs.First()));
                if (rslt.Success == false)
                {
                    Debug.WriteLine("Model name cannot be inferred from " + inputFolder);
                    MessageBox.Show(this, @"Model name cannot be inferred from " + inputFolder,
                        @"Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    continue;
                }

                var modelName = rslt.Groups[1].Value;
                Debug.WriteLine("Model name found : " + modelName);
                Debug.WriteLine($"Running TexturePacker on {inputFolder} with Model Name: {modelName}");

                if (Properties.Settings.Default.PACK_ANDROID)
                {
                    LibGdxPacker(tpExecutable, libgdxTps, inputFolder, modelName);
                    SpriteKit(tpExecutable, spritekittps, inputFolder, modelName);
                }

                if (Properties.Settings.Default.PACK_IOS)
                {
                    LibGdxPackerIos(tpExecutable, libgdxTps, inputFolder, modelName);
                    SpriteKitPackerIos(tpExecutable, spritekittps, inputFolder, modelName);
                }
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

        private string GetSeriesNumber(string input)
        {
            var rgxSeries = new Regex(@"\d\d\-\d\d\d");
            var result = rgxSeries.Match(input);
            if (result.Success)
                return result.Groups[0].Value;

            throw new Exception($"Series number not found from {input}!");
        }

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

            RunProcess($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitSDFrame01 + "/" + modelName + "-SD_Pack0.atlasc"}\" \"{sdFrame0}\" \"{tps}\"");

            Debug.WriteLine("Packing SpriteKit Frame1 SD...");
            Debug.WriteLine($"SpriteKit Packing: {sdFrame1}");
            RunProcess($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitSDFrame01 + "/" + modelName + "-SD_Pack1.atlasc"}\" \"{sdFrame1}\" \"{tps}\"");

            Debug.WriteLine("Packing SpriteKit Frame0 HD...");
            Debug.WriteLine($"SpriteKit Packing: {hdFrame0}");
            RunProcess($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitHDFrame01 + "/" + modelName + "_Pack0.atlasc"}\" \"{hdFrame0}\" \"{tps}\"");

            Debug.WriteLine("Packing SpriteKit Frame1 HD...");
            Debug.WriteLine($"SpriteKit Packing: {hdFrame1}");
            RunProcess($"\"{tpExecutable}\"", $"--data \"{outputSpriteKitHDFrame01 + "/" + modelName + "_Pack1.atlasc"}\" \"{hdFrame1}\" \"{tps}\"");
        }

        private void LibGdxPacker(string tpExecutable, string tpsFile, string inputFolder, string modelName)
        {
            var libGdxExt = Properties.Settings.Default.LIBGDX_DATFILE_EXTENTION;

            var sdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame0");
            var sdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "SD", "Frame1");
            var hdFrame0 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame0");
            var hdFrame1 = Path.Combine(inputFolder, "V5", "PACKSOURCE", "HD", "Frame1");

            var outputLibgdxSDFrame01 = Path.Combine(inputFolder, "V5", "Output", "SD", "libgdx");
            var outputLibgdxHDFrame01 = Path.Combine(inputFolder, "V5", "Output", "HD", "libgdx");

            Debug.WriteLine("Packing Libgdx Frame0 SD...");
            Debug.WriteLine($"LibGDX Packing: {sdFrame0}");
            RunProcess($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxSDFrame01 + "/" + modelName + "-SD_Pack0-{n}.png"}\" --data \"{outputLibgdxSDFrame01 + "/" + modelName + $"-SD_Pack0.{libGdxExt}"}\" \"{sdFrame0}\" \"{tpsFile}\"");

            Debug.WriteLine("Packing Libgdx Frame1 SD...");
            Debug.WriteLine($"LibGDX Packing: {sdFrame1}");
            RunProcess($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxSDFrame01 + "/" + modelName + "-SD_Pack1-{n}.png"}\" --data \"{outputLibgdxSDFrame01 + "/" + modelName + $"-SD_Pack1.{libGdxExt}"}\" \"{sdFrame1}\" \"{tpsFile}\"");

            Debug.WriteLine("Packing Libgdx Frame0 HD...");
            Debug.WriteLine($"LibGDX Packing: {hdFrame0}");
            RunProcess($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack0-{n}.png"}\" --data \"{outputLibgdxHDFrame01 + "/" + modelName + $"_Pack0.{libGdxExt}"}\" \"{hdFrame0}\" \"{tpsFile}\"");

            Debug.WriteLine("Packing Libgdx Frame1 HD...");
            Debug.WriteLine($"LibGDX Packing: {hdFrame1}");
            RunProcess($"\"{tpExecutable}\"", $"--sheet \"{outputLibgdxHDFrame01 + "/" + modelName + "_Pack1-{n}.png"}\" --data \"{outputLibgdxHDFrame01 + "/" + modelName + $"_Pack1.{libGdxExt}"}\" \"{hdFrame1}\" \"{tpsFile}\"");

            if (!string.IsNullOrWhiteSpace(_csvLocation))
            {
                try
                {
                    CountPngs(_csvLocation, inputFolder);
                }
                catch (Exception e)
                {
                    Debug.WriteLine(e);
                    Debug.WriteLine("Something went wrong while counting number of PNGs");
                }
            }
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

        private void CountPngs(string csvLocation, string modelFolder)
        {
            var modelName = GetModelName(modelFolder);

            Debug.WriteLine("Counting Pngs...");

            var libgdxFolderHd = Path.Combine(modelFolder, "V5", "Output", "HD", "libgdx");
            var libgdxFolderSd = Path.Combine(modelFolder, "V5", "Output", "SD", "libgdx");

            var data8Hd = Directory.GetFiles(libgdxFolderHd, "*Pack0*.png").Length;
            Debug.WriteLine($"data8Hd: {data8Hd}");

            var dataHd = Directory.GetFiles(libgdxFolderHd, "*Pack1*.png").Length;
            Debug.WriteLine($"data8Hd: {dataHd}");

            var data8Sd = Directory.GetFiles(libgdxFolderSd, "*Pack0*.png").Length;
            Debug.WriteLine($"data8Hd: {data8Sd}");

            var dataSd = Directory.GetFiles(libgdxFolderSd, "*Pack1*.png").Length;
            Debug.WriteLine($"data8Hd: {dataSd}");

            var outputCsv = Path.Combine(Path.GetDirectoryName(csvLocation),
                Path.GetFileNameWithoutExtension(csvLocation) + "_edited.csv");


            Debug.WriteLine("Writing to Real3d_V1.csv . . .");
            var items = new List<List<string>>();
            var headers = new List<string>();


            using (var fileStream = new FileStream(csvLocation, FileMode.Open))
            {
                var csvReader = Csv.CsvReader.ReadFromStream(fileStream);

                var rowCounter = 0;
                var data8HdIndex = -1;
                var dataHdIndex = -1;
                var data8SdIndex = -1;
                var dataSdIndex = -1;

                foreach (var csvLine in csvReader)
                {
                    if (rowCounter == 0)
                    {
                        data8HdIndex = Array.IndexOf(csvLine.Headers, "data8HD");
                        dataHdIndex = Array.IndexOf(csvLine.Headers, "dataHD");
                        data8SdIndex = Array.IndexOf(csvLine.Headers, "data8SD");
                        dataSdIndex = Array.IndexOf(csvLine.Headers, "dataSD");

                        headers.AddRange(csvLine.Headers.ToList());
                        rowCounter++;
                        continue;
                    }

                    if (csvLine[0] == modelName)
                    {
                        csvLine.Values[data8HdIndex] = data8Hd.ToString();
                        csvLine.Values[dataHdIndex] = dataHd.ToString();
                        csvLine.Values[data8SdIndex] = data8Sd.ToString();
                        csvLine.Values[dataSdIndex] = dataSd.ToString();
                    }

                    items.Add(csvLine.Values.ToList());

                    rowCounter++;
                }
            }

            using (var streamWriter = new StreamWriter(csvLocation))
            {
                Csv.CsvWriter.Write(streamWriter, headers.ToArray(), items.Select(i => i.ToArray()));
                Debug.WriteLine("Done writing to Real3d_V1.csv");
            }
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
                        RoboCopy(outputFolder, depotPath);

                        var outputFolderIos = Path.Combine(inputFolder, "V5", "OutputIOS");
                        RoboCopy(outputFolderIos, depotPath);

                        Debug.WriteLine("[Depot] Copying files from SAVE, MP3 and CSV files\n");
                        RunProcess("robocopy", $"\"{inputFolder}\" \"{depotPath}\" *.sav *.csv *.mp3");

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
                                // process = Process.Start("robocopy", $"\"{iconFolder}\" \"{Path.Combine(depotPath, modelName)}\" /MIR");

                                RoboCopy(iconFolder, Path.Combine(depotPath, modelName));
                                //process = Process.Start("robocopy", $"\"{iconFolder}\" \"{Path.Combine(depotPath, modelName)}\" /E");
                                //process.WaitForExit();
                                //process.Close();
                            }
                        }
                    }
            }
        }

        private void RoboCopy(string outputFolder, string depotPath)
        {
            if (Directory.Exists(outputFolder) && Directory.Exists(depotPath))
            {
                Debug.WriteLine($"[Depot] Copying files from {outputFolder} to {depotPath}\n");
                //process = Process.Start("robocopy", $"\"{outputFolder}\" \"{depotPath}\" /MIR");
                RunProcess("robocopy", $"\"{outputFolder}\" \"{depotPath}\" /E");
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

        private void RunDepotButtonClicked(object sender, EventArgs e)
        {
            RunDepot();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            Text = Application.ExecutablePath;

            Debug.Listeners.Add(new DebugTextListener(richTextBoxLogs));

            Parser.Default.ParseArguments<Options>(Environment.GetCommandLineArgs())
                                     .WithParsed(options =>
                                     {
                                         if (string.IsNullOrWhiteSpace(options.StartDirectory))
                                         {
                                             Debug.WriteLine("No arguments found. I'm not running in Auto Mode");
                                             return;
                                         }

                                         if (!Directory.Exists(options.StartDirectory))
                                         {
                                             Debug.WriteLine($"The folder {options.StartDirectory} does not exist. Please check start directory in your MacroScript.");
                                             return;
                                         }

                                         _csvLocation = Path.Combine(options.StartDirectory, "Real3d_V1.csv");

                                         Task.Run(() =>
                                         {
                                             try
                                             {
                                                 _real3DConfig = new List<Real3DV1>();

                                                 using (var streamReader = new StreamReader(Path.Combine(options.StartDirectory, "Real3d_V1.csv")))
                                                 using (var csv = new CsvReader(streamReader))
                                                 {
                                                     csv.Configuration.PrepareHeaderForMatch = (s, i) => s.Replace(" ", "").ToLower().Trim();
                                                     var config = csv.GetRecords<Real3DV1>().ToList();
                                                     _real3DConfig.AddRange(config.Where(dv1 => dv1.IsReady == 1));
                                                 }

                                                 if (!_real3DConfig.Any())
                                                 {
                                                     throw new Exception("Unable to obtain model names from 'Read3d_V1.csv' file");
                                                 }



                                                 var dirs = Directory.GetDirectories(options.StartDirectory);
                                                 foreach (var dir in dirs)
                                                 {
                                                     var modelName = ParseModelName(dir);

                                                     if (_real3DConfig.All(dv1 => dv1.Model.Trim() != modelName.Item1.Trim()))
                                                         continue;

                                                     if (!string.IsNullOrWhiteSpace(modelName.Item1))
                                                         listBoxFolders.BeginInvoke(new Action(() =>
                                                         {
                                                             var idx = listBoxFolders.Items.Add(Path.Combine(dir, "KeyShot", "Renders", modelName.Item1));
                                                         }));
                                                 }

                                                 if (options.Mode.ToLower() == "manual")
                                                     return;

                                                 buttonRunPacker.BeginInvoke(new Action(() =>
                                                 {
                                                     buttonRunPacker.PerformClick();
                                                 }));
                                             }
                                             catch (Exception exception)
                                             {
                                                 Debug.WriteLine("Error: " + exception.Message);
                                                 //Debug.WriteLine(exception.StackTrace);
                                             }
                                         });
                                     });


        }

        private Tuple<string, string> ParseModelName(string dirName)
        {
            var regexModelName = new Regex(@"((\d\d\-\d\d\d)_[a-z0-9]+)", RegexOptions.IgnoreCase);
            var matchResult = regexModelName.Match(dirName);
            // return (modelName, seriesNumber)
            return !matchResult.Success ? new Tuple<string, string>(string.Empty, string.Empty) : new Tuple<string, string>(matchResult.Groups[1].Value.Trim(), matchResult.Groups[2].Value.Trim());
        }

        private void CreateCleanDirectory(string directory)
        {
            Debug.WriteLine($"Creating a clean directory {directory}.");
            try
            {
                if (Directory.Exists(directory))
                    Directory.Delete(directory, true);

                Directory.CreateDirectory(directory);
            }
            catch (Exception e)
            {
                // ignored
            }
        }

        private void PrepareIosPacking(string modelFolder)
        {
            Debug.WriteLine("Preparing texture packer for IOS");

            var modelName = ParseModelName(modelFolder);

            var packSourceSD = Path.Combine(modelFolder, "V5", "PACKSOURCE", "SD");
            Debug.WriteLine($"Reading SD images from {packSourceSD}");

            var packSourceHD = Path.Combine(modelFolder, "V5", "PACKSOURCE", "HD");
            Debug.WriteLine($"Reading HD images from {packSourceHD}");

            if (!Directory.Exists(packSourceSD) || !Directory.Exists(packSourceHD))
            {
                throw new Exception("Please run packer for android first before running packer for IOS");
            }

            var packSourceIosSD = Path.Combine(modelFolder, "V5", "PACKSOURCEIOS", $"{modelName.Item2}_Model-SD");
            Debug.WriteLine($"Writing IOS packed SD texture to {packSourceIosSD}.");

            var packSourceIosHD = Path.Combine(modelFolder, "V5", "PACKSOURCEIOS", $"{modelName.Item2}_Model-HD");
            Debug.WriteLine($"Writing IOS packed HD texture to {packSourceIosHD}.");

            var packSourceIosUI_SD = Path.Combine(modelFolder, "V5", "PACKSOURCEIOS", $"{modelName.Item2}_UI-SD");
            var packSourceIosUI_HD = Path.Combine(modelFolder, "V5", "PACKSOURCEIOS", $"{modelName.Item2}_UI-HD");


            CreateCleanDirectory(packSourceIosSD);
            CreateCleanDirectory(packSourceIosHD);
            CreateCleanDirectory(packSourceIosUI_SD);
            CreateCleanDirectory(packSourceIosUI_HD);

            var rgx = new Regex(@"(.+)\.\d+\.png", RegexOptions.IgnoreCase);

            // copy hd
            Debug.WriteLine("Copying IOS HD sources...");
            foreach (var file in Directory.GetFiles(packSourceHD, "*.*", SearchOption.AllDirectories))
            {
                Debug.WriteLine($"Processing {file}...");
                File.Copy(file,
                    rgx.IsMatch(Path.GetFileName(file))
                        ? Path.Combine(packSourceIosHD, $"{modelName.Item2}_HD_{Path.GetFileName(file)}")
                        : Path.Combine(packSourceIosUI_HD, $"{modelName.Item2}_HD_{Path.GetFileName(file)}"));
            }

            // copy sd
            Debug.WriteLine("Copying IOS SD sources...");
            foreach (var file in Directory.GetFiles(packSourceSD, "*.*", SearchOption.AllDirectories))
            {
                Debug.WriteLine($"Processing {file}...");
                File.Copy(file,
                    rgx.IsMatch(Path.GetFileName(file))
                        ? Path.Combine(packSourceIosSD, $"{modelName.Item2}_SD_{Path.GetFileName(file)}")
                        : Path.Combine(packSourceIosUI_SD, $"{modelName.Item2}_SD_{Path.GetFileName(file)}"));
            }

            //arrange hd
            var files = Directory.GetFiles(packSourceIosHD, "*.png", SearchOption.AllDirectories).Where(s => rgx.IsMatch(s))
                .Select(s =>
                {
                    var result = rgx.Match(Path.GetFileName(s));
                    return new Tuple<string, string>(result.Groups[1].Value, Path.GetFileName(s));
                })
                .GroupBy(tuple => tuple.Item1);

            foreach (var group in files)
            {
                Debug.WriteLine($"Processing IOS HD image group {group.Key}");
                var combine = Path.Combine(packSourceIosHD, $"{group.Key}.atlas");
                Directory.CreateDirectory(combine);

                foreach (var tuple in group)
                {
                    var source = Path.Combine(packSourceIosHD, tuple.Item2);
                    var destination = Path.Combine(combine, tuple.Item2);
                    File.Move(source, destination);
                }
            }

            //arrange sd
            files = Directory.GetFiles(packSourceIosSD, "*.png", SearchOption.AllDirectories).Where(s => rgx.IsMatch(s))
                .Select(s =>
                {
                    var result = rgx.Match(Path.GetFileName(s));
                    return new Tuple<string, string>(result.Groups[1].Value, Path.GetFileName(s));
                })
                .GroupBy(tuple => tuple.Item1);

            foreach (var group in files)
            {
                Debug.WriteLine($"Processing IOS SD image group {group.Key}");

                var combine = Path.Combine(packSourceIosSD, $"{group.Key}.atlas");
                Directory.CreateDirectory(combine);

                foreach (var tuple in group)
                {
                    var source = Path.Combine(packSourceIosSD, tuple.Item2);
                    var destination = Path.Combine(combine, tuple.Item2);
                    File.Move(source, destination);
                }
            }

            // Json
            var packSourceIos = Path.Combine(modelFolder, "V5", "PACKSOURCEIOS");

            var uiFolders = Directory.GetDirectories(packSourceIos, "*_UI*");
            foreach (var uiFolder in uiFolders)
            {
                var isHd = uiFolder.ToLower().EndsWith("-hd");
                var uiJson = new UiJson();
                foreach (var file in Directory.GetFiles(uiFolder, "*.png"))
                {
                    uiJson.names.Add(Path.GetFileName(file));
                }

                File.WriteAllText(Path.Combine(uiFolder, "ui_items.json"),
                    JsonConvert.SerializeObject(uiJson, Formatting.Indented));
            }
        }

        private void LibGdxPackerIos(string tpExecutable, string tpsFile,
            string inputFolder, string modelName)
        {
            Debug.WriteLine("Running Ios LibGdx packer");
            var seriesNumber = GetSeriesNumber(modelName);

            CreateCleanDirectory(Path.Combine(inputFolder, "V5", "OutputIOS", "HD", "libgdx"));
            CreateCleanDirectory(Path.Combine(inputFolder, "V5", "OutputIOS", "SD", "libgdx"));

            var modelFolders = Directory.GetDirectories(Path.Combine(inputFolder, "V5", "PACKSOURCEIOS"), "*_Model*");
            foreach (var modelFolder in modelFolders)
            {
                var isHd = modelFolder.EndsWith("-HD");

                var outputAtlasFolder = Path.Combine(inputFolder, "V5", "OutputIOS", isHd ? "HD" : "SD", "libgdx");

                foreach (var altasInputFolder in Directory.GetDirectories(modelFolder))
                {
                    Debug.WriteLine($"Processing Ios LibGdx {altasInputFolder}");
                    RunProcess($"\"{tpExecutable}\"", $"--sheet \"{outputAtlasFolder + "/" + seriesNumber + $"_{(isHd ? "HD" : "SD")}" + "_" + Path.GetFileName(altasInputFolder) + "{n}.png"}\" --data \"{outputAtlasFolder + "/" + seriesNumber + $"_{(isHd ? "HD" : "SD")}" + "_" + Path.GetFileName(altasInputFolder) + ".atlas"}\" \"{altasInputFolder}\" \"{tpsFile}\"");
                }
            }
        }

        private void RunProcess(string executable, string arguments)
        {
            var startInfo = new ProcessStartInfo
            {
                CreateNoWindow = true,
                UseShellExecute = false,
                FileName = executable,
                Arguments = arguments,
                WindowStyle = ProcessWindowStyle.Hidden
            };

            using (var process = Process.Start(startInfo))
            {
                process.WaitForExit();
                process.Close();
            }
        }

        private void SpriteKitPackerIos(string tpExecutable, string tps, string inputFolder, string modelName)
        {
            Debug.WriteLine("Running Ios SpriteKit packer...");
            var seriesNumber = GetSeriesNumber(modelName);
            var modelFolders = Directory.GetDirectories(Path.Combine(inputFolder, "V5", "PACKSOURCEIOS"), "*_Model*");

            CreateCleanDirectory(Path.Combine(inputFolder, "V5", "OutputIOS", "SD", "SpriteKit"));
            CreateCleanDirectory(Path.Combine(inputFolder, "V5", "OutputIOS", "HD", "SpriteKit"));

            foreach (var modelFolder in modelFolders)
            {
                foreach (var partFolder in Directory.GetDirectories(modelFolder))
                {
                    Debug.WriteLine($"Processing Ios SpriteKit {partFolder}");
                    var isHd = modelFolder.EndsWith("-HD");
                    var outputAtlasFolder = Path.Combine(inputFolder, "V5", "OutputIOS", $"{(isHd ? "HD" : "SD")}", "SpriteKit");
                    RunProcess($"\"{tpExecutable}\"",
                        $"--data \"{outputAtlasFolder + "/" + seriesNumber + $"_{(isHd ? "HD" : "SD")}" + "_" + Path.GetFileName(partFolder) + ".atlasc"}\" \"{partFolder}\" \"{tps}\"");
                }
            }
        }

        private void listBoxFolders_DoubleClick(object sender, EventArgs e)
        {
            if (listBoxFolders.SelectedItem != null)
            {
                Process.Start("explorer.exe", listBoxFolders.SelectedItem.ToString());
            }
        }
    }
}

