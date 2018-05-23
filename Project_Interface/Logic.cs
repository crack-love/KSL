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
        {   // 프로세스가 동작하는지 확인
            if (process[i] == null) return;

            // catch process
            try
            {
                Process catched = Process.GetProcessById(process[i].Id);
            }
            catch (ArgumentException)
            {
                // process died in wild
                processEnableChanged(i, false);  // 외부의 processEnableChanged를 호출
                process[i] = null;
            }
        }

        private void processStdInput(int i, string text)
        {   // process에게 표준입력으로 text를 입력함
            if (!isProcessRunning(i)) return;

            // 개행문자 제거
            text = text.Trim('\n', '\r');

            process[i].StandardInput.WriteLine(text);
        }

        private void processExecute(int i, string path, string arg)
        {   // path에 지정된 프로그램을 실행함.
            if (isProcessRunning(i)) return;

            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.CreateNoWindow = true;
            startInfo.ErrorDialog = true;
            startInfo.FileName = path;
            startInfo.UseShellExecute = false;
            startInfo.RedirectStandardInput = true;   // 표준입력을 받을 수 있도록 함
            startInfo.RedirectStandardOutput = true;  // 표준출력을 다른 곳에 출력할 수 있도록 함
            startInfo.RedirectStandardError = true;
            startInfo.WorkingDirectory = path.Substring(0, path.LastIndexOf(@"\"));  // 프로세스의 작업 디렉토리 설정
            startInfo.Arguments = arg;  // 실행 인자를 넘겨줌
            
            process[i] = Process.Start(startInfo);  // 프로세스 실행
            process[i].OutputDataReceived += outputDataReceived;  // 표준출력 값을 outputDataReceived를 통해 받음
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
        {   // 모든 프로세스 종료
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
                    data = data.Substring("[Result]".Length);  // [Result]를 잘라내어 결과값만 저장
                }

                // 예측 요청 메시지일 경우
                if (data.StartsWith("[Predict]"))
                {
                    // 파이썬에 넘김
                    data = data.Substring("[Predict]".Length);  // [Predict]를 잘라내어 예측해야할 데이터만 저장
                    processStdInput(1, data);
                    return; 
                }

                // UI Text 수정하는 이벤트 호출
                outputReceived(idx, data);
            }
        }
    }
}