using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DanielApp
{
    class DebugTextListener : TraceListener
    {
        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        private static extern IntPtr SendMessage(IntPtr hWnd, int wMsg, IntPtr wParam, IntPtr lParam);
        private const int WM_VSCROLL = 277;
        private const int SB_PAGEBOTTOM = 7;

        internal static void ScrollToBottom(RichTextBox richTextBox)
        {
            SendMessage(richTextBox.Handle, WM_VSCROLL, (IntPtr)SB_PAGEBOTTOM, IntPtr.Zero);
            richTextBox.SelectionStart = richTextBox.Text.Length;
        }

        private readonly RichTextBox _richTextBox;

        private delegate void TextWriter(string text);

        private DateTime _lastScroll = DateTime.Now;

        private void AppendTextWriter(string text)
        {
            _richTextBox.AppendText(text);
            if ((DateTime.Now - _lastScroll).TotalSeconds < 2)
                return;

            ScrollToBottom(_richTextBox);
            _lastScroll = DateTime.Now;
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
