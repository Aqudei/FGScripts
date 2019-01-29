using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace DanielApp
{
    class FrameFile
    {
        public string Model { get; set; }
        public string FrameName { get; set; }
        public string XNumber { get; set; }
        public string FileName { get; set; }

        public static FrameFile Parse(string file)
        {
            var rgxNum = new Regex(@"\.(\d+)\.png");
            var newFrame = new FrameFile();
            newFrame.FileName = file;
            var rslt = rgxNum.Match(file);
            if (rslt.Success == false)
                return null;

            newFrame.XNumber = rslt.Groups[1].Value;
            newFrame.FrameName = Path.GetFileName(file).Split(".".ToCharArray())[0];
            newFrame.Model = Path.GetFileName(file).Split(".".ToCharArray())[0];
            return newFrame;
        }
    }
}
