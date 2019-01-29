using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DanielApp
{
    class DebugTextListener : TraceListener
    {
        private readonly RichTextBox _richTextBox;

        private delegate void TextWriter(string text);

        private void AppendTextWriter(string text)
        {
            _richTextBox.AppendText(text);
        }

        public DebugTextListener(RichTextBox richTextBox)
        {
            _richTextBox = richTextBox;
        }

        public override void Write(string message)
        {
            if (_richTextBox.InvokeRequired)
            {
                _richTextBox.BeginInvoke(new TextWriter(AppendTextWriter), message);
            }
            else
            {
                AppendTextWriter(message);
            }
        }

        public override void WriteLine(string message)
        {
            Write(message + Environment.NewLine);
        }
    }
}
