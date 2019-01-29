using CsvHelper.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DanielApp
{
    class PartMap : ClassMap<Part>
    {
        public PartMap()
        {
            Map(m => m.ModelPart).Name("Model Part");
        }
    }
}
