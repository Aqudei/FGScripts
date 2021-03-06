﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CommandLine;

namespace DanielApp
{
    class Options
    {
        [Option('d', "directory", Required = false)]
        public string StartDirectory { get; set; }

        [Option('m', "mode", Required = false, Default = "manual")]
        public string Mode { get; set; }
    }
}
