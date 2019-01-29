using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DanielApp
{
    class PartsCsv
    {
        private List<List<string>> _csvLines;
        private List<int> columnsToCheck = new List<int>();
        private HashSet<string> _lookup = new HashSet<string>();

        public bool ShouldCopy(string name)
        {
            var ss = Path.GetFileName(name);
            var nameOnly = ss.Split(".-".ToCharArray())[0];
            return _lookup.Contains(nameOnly);
        }

        public PartsCsv(string filename)
        {
            if (!File.Exists(filename))
                throw new Exception("PartsCsv does not exists.");

            _csvLines = File.ReadLines(filename).Select(l => l.Split(",".ToCharArray()).ToList()).ToList();

            var csvLine1 = _csvLines[0];
            for (int i = 0; i < csvLine1.Count; i++)
            {
                var value = csvLine1[i];
                if (string.IsNullOrWhiteSpace(value))
                    continue;

                if (value.Trim().Contains("Part Base Image") ||
                    value.Trim().Contains("Part Gloss Image"))
                {
                    columnsToCheck.Add(i);
                }
            }

            for (int i = 1; i < _csvLines.Count; i++)
            {
                var line = _csvLines[i];
                for (var index = 0; index < columnsToCheck.Count; index++)
                {
                    var columnToCheck = columnsToCheck[index];
                    var value = line[columnToCheck];

                    if (string.IsNullOrWhiteSpace(value))
                        continue;

                    value = value.Trim(".-".ToCharArray());
                    _lookup.Add(value);
                }
            }
        }
    }
}
