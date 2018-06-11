using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Interface2
{
    class Logic
    {
        // ------------------------------------------------------------------
        // Constant variables
        // ------------------------------------------------------------------

        static object threadLock;
        const int PROCESS_SIZE = 2;

        // ------------------------------------------------------------------
        // Member variables
        // ------------------------------------------------------------------
        
        private Process[] process;
        private Dictionary<Process, int> processMapIndex;

        // public
        public event Action<int, bool> processEnableChanged;
        public event Action<int, string> outputReceived; // -1 to main, 0~ processNumber

        // ------------------------------------------------------------------
        // public functions
        // ------------------------------------------------------------------

        public Logic()
        {
            threadLock = new Control();
            process = new Process[PROCESS_SIZE];
            processMapIndex = new Dictionary<Process, int>();

            processEnableChanged = null;
            outputReceived = null;
        }

        public void input(int v, string text)
        {
            processStdInput(v, text);
        }

        public void execute(int v, string path, string arg)
        {
            processExecute(v, path, arg);
        }

        public void finalize()
        {
            closeAllProcess();
        }

        public bool isProcessRunning(int i)
        {
            checkProcessDead(i);
            return process[i] != null;
        }

        // ------------------------------------------------------------------
        // private functions
        // ------------------------------------------------------------------

        private void checkProcessDead(int i)
        {
            if (process[i] == null) return;

            // catch process
            try
            {
                Process catched = Process.GetProcessById(process[i].Id);
            }
            catch (ArgumentException)
            {
                // process died in wild
                processEnableChanged(i, false);
                process[i] = null;
            }
        }

        private void processStdInput(int i, string text)
        {
            if (!isProcessRunning(i)) return;

            // 개행문자 제거
            text = text.Trim('\n', '\r');

            process[i].StandardInput.WriteLine(text);
        }

        private void processExecute(int i, string path, string arg)
        {
            if (isProcessRunning(i)) return;

            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.CreateNoWindow = true;
            startInfo.ErrorDialog = true;
            startInfo.FileName = path;
            startInfo.UseShellExecute = false;
            startInfo.RedirectStandardInput = true;
            startInfo.RedirectStandardOutput = true;
            startInfo.RedirectStandardError = true;
            startInfo.WorkingDirectory = path.Substring(0, path.LastIndexOf(@"\"));
            startInfo.Arguments = arg;
            
            process[i] = Process.Start(startInfo);
            process[i].OutputDataReceived += outputDataReceived;
            process[i].ErrorDataReceived += outputDataReceived;
            processMapIndex[process[i]] = i;
            process[i].BeginOutputReadLine();
            process[i].BeginErrorReadLine();

            //String output = process[i].StandardOutput.ReadToEnd();
            //MessageBox.Show(output);
            //process[i].WaitForInputIdle();
            //outputReceived(1, output);
            checkProcessDead(i);
        }

        private void closeAllProcess()
        {
            for (int i = 0; i < PROCESS_SIZE; ++i)
            {
                if (isProcessRunning(i))
                {
                    process[i].Kill();

                    process[i].WaitForExit(100);

                    checkProcessDead(i);
                }
            }
        }

        // WARNING :: this called form other thread
        private void outputDataReceived(object sender, DataReceivedEventArgs arg)
        {
            Process who = (Process)sender;
            int idx = processMapIndex[who];
            string data = arg.Data;
            
            if (!String.IsNullOrEmpty(data))
            {
                data = data.Trim();

                // 결과 메시지일 경우
                if (data.StartsWith("[Result]"))
                {
                    idx = -1;
                    data = data.Substring("[Result]".Length);
                }

                // 예측 요청 메시지일 경우 (Spoint)
                else if (data.StartsWith("[Predict]"))
                {
                    // 파이썬에 넘김
                    /* 과거코드
                    data = data.Substring("[Predict0]".Length);
                    processStdInput(1, data);
                    */
                    processStdInput(1, data);
                    return;
                }

                // UI Text 수정하는 이벤트 호출
                outputReceived(idx, data);
            }
        }
    }
}