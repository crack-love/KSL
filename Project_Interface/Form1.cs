using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Interface2
{
    public partial class Form : System.Windows.Forms.Form
    {
        enum ProcessStatus
        {
            None, Ready, Dead 
        }

        UserData data;
        Logic logic;
        Timer runningCheck;
        bool isLeftStarted;
        bool isRightStarted;

        public Form()
        {
            InitializeComponent();
            initComponetData();
            initUserData();
            initLogic();
            initTimer();
        }

        private void initComponetData()
        {
            isLeftStarted = false;
            isRightStarted = false;
            labelMain.Text = "";
            textBoxInputLeft.Text = "";
            textBoxInputRight.Text = "";
            textBoxOutputLeft.Text = "";
            textBoxOutputRight.Text = "";
            textBoxInputLeft.Enabled = false;
            textBoxInputRight.Enabled = false;
            setLabelStatus(0, ProcessStatus.None);
            setLabelStatus(1, ProcessStatus.None);
        }

        private void initUserData()
        {   // UserData 할당 후 userdata.dat에서 python 위치, kinectProgram 위치 정보를 불러옴
            data = new UserData();
            data.load();
        }

        private void initLogic()
        {   // Login 할당 후 login에서 메소드를 호출할 수 있도록 메소드를 넘겨줌
            logic = new Logic();
            logic.processEnableChanged += executeButtonEnableChanged;
            logic.outputReceived += outputRecieved;
        }

        private void initTimer()
        {
            runningCheck = new Timer();
            runningCheck.Tick += runningCheck_Tick;
            runningCheck.Interval = 400;
        }

        private void runningCheck_Tick(object sender, EventArgs e)
        {   // process가 돌아가는지 확인

            if (isLeftStarted)
            {
                executeButtonEnableChanged(0, logic.isProcessRunning(0));
            }

            if (isRightStarted)
            {
                executeButtonEnableChanged(1, logic.isProcessRunning(1));
            }
        }


        private void textBoxInputLeft_KeyDown(object sender, KeyEventArgs e)
        {   // enter를 눌렀을 경우 0번 프로그램에 Text를 입력
            if (e.KeyCode == Keys.Enter)
            {
                logic.input(0, textBoxInputLeft.Text);
                textBoxInputLeft.Text = "";
            }
        }

        private void textBoxInputRight_KeyDown(object sender, KeyEventArgs e)
        {   // enter를 눌렀을 경우 1번 프로그램에 Text를 입력
            if (e.KeyCode == Keys.Enter)
            {
                logic.input(1, textBoxInputRight.Text);
                textBoxInputRight.Text = "";
            }
        }

        private void buttonLeft_Click(object sender, EventArgs e)
        {   // 키넥트 프로그램 실행
            if (data.KinectProgramPath == null || !File.Exists(data.KinectProgramPath))
            {
                MessageBox.Show(this, "키넥트 프로그램이 설정돼있지 않거나 파일이 존재하지 않습니다. 프로그램을 선택해주세요");
                OpenFileDialog dialog = new OpenFileDialog();
                dialog.Filter = "exe|*.exe";
                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    data.KinectProgramPath = dialog.FileName;  // UserData에 키넥트 경로 지정
                }
                else return;
            }

            logic.execute(0, data.KinectProgramPath, "");
            textBoxOutputLeft.Text = "";
            isLeftStarted = true;
            runningCheck.Start();
        }

        private void buttonRight_Click(object sender, EventArgs e)
        {   // 파이썬 프로그램 실행
            bool pythonChoose = false;

            if (data.pythonPath == null || !File.Exists(data.pythonPath))
            {
                MessageBox.Show(this, "파이썬 경로가 설정돼있지 않거나 파일이 존재하지 않습니다. 파이썬 프로그램을 선택해주세요 (Python Version 3.5.x)");
                OpenFileDialog dialog2 = new OpenFileDialog();
                dialog2.Filter = "python exe|*.exe";
                if (dialog2.ShowDialog() == DialogResult.OK)
                {
                    data.pythonPath = dialog2.FileName;
                    data.save();
                    pythonChoose = true;
                }
                else return;
            }

            if (pythonChoose)
                MessageBox.Show("스크립트 선택");

            OpenFileDialog dialog = new OpenFileDialog();
            dialog.Filter = "py|*.py";
            dialog.Title = "Open Python Script";
            if (dialog.ShowDialog() == DialogResult.OK)
            {   // python을 이용하여 python script를 실행. 옵션 -u를 통해 python stdin, stderr buffer를 사용하지 않도록 함
                logic.execute(1, data.pythonPath, "-u " + dialog.FileName);
                textBoxOutputRight.Text = "";
                isRightStarted = true;
                runningCheck.Start();
            }
        }

        private void Form_FormClosing(object sender, FormClosingEventArgs e)
        {
            data.save();
            logic.finalize();  // process들을 모두 종료
        }

        private void executeButtonEnableChanged(int idx, bool processOK)
        {
            switch(idx)
            {
                case 0:
                    buttonLeft.Text = processOK ? "(Running)" : "Execute";
                    textBoxInputLeft.Enabled = processOK;
                    buttonLeft.Enabled = !processOK; break;
                case 1:
                    buttonRight.Text = processOK? "(Running)" : "Execute";
                    textBoxInputRight.Enabled = processOK;
                    buttonRight.Enabled = !processOK; break;
            }

            setLabelStatus(idx, processOK ? ProcessStatus.Ready : ProcessStatus.Dead);  // process의 상태에 따라 label을 업데이트 시킴
        }

        // called from other thread
        private void outputRecieved(int idx, string data)
        {
            data += Environment.NewLine;
            
            switch (idx)
            {
                case -1:
                    setControl(labelMain, setMainText, data);
                    break;
                case 0:
                    setControl(textBoxOutputLeft, textBoxOutputLeft.AppendText, data);
                    break;
                case 1:
                    setControl(textBoxOutputRight, textBoxOutputRight.AppendText, data);
                    break;
            }
        }

        private void setMainText(string s)
        {
            labelMain.Text = s;
        }

        // 컨트롤 세이프 콜
        public delegate void Function(string x);
        private void setControl(Control control, Function call, string arg)
        {
            if (control.InvokeRequired)
            {   // 다른 스레드에 있을 경우 대리자를 이용하여 함수를 실행
                control.Invoke(call, arg);
            }
            else
                call(arg);
        }

        private void buttonCloseAll_Click(object sender, EventArgs e)
        {
            logic.finalize();
            initLogic();
        }

        private void setLabelStatus(int idx, ProcessStatus status)
        {
            Label[] dstList = { labelStatusLeft, labelStatusRight };
            Color foreColor = Color.Black;
            Color backColor = Color.FromKnownColor(KnownColor.Control);
            string text = "";

            switch(status)
            {
                case ProcessStatus.None:
                    text = "None";
                    break;
                case ProcessStatus.Ready:
                    text = "Ready";
                    foreColor = Color.White;
                    backColor = Color.Green;
                    break;
                case ProcessStatus.Dead:
                    text = "Dead";
                    foreColor = Color.White;
                    backColor = Color.Red;
                    break;
            }

            dstList[idx].Text = text;
            dstList[idx].ForeColor = foreColor;
            dstList[idx].BackColor = backColor;
        }

        private void buttonSet_Click(object sender, EventArgs e)
        {
            data.setFromPrompt();
        }
    }
}