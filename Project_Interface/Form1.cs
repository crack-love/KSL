using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_Interface
{
    public partial class FormMain : Form
    {
        const int port = 14358;
        const int port1 = 14359;
        const int port2 = 14360;

        //const string programCameraPath = "Project_Kinect_Debug.exe";
        //const string programServerPath = "do_PredictServer.py";

        Process programCamera;
        Process programServer;

        Socket socket1;
        Socket socket2;

        public FormMain()
        {
            InitializeComponent();
        }

        private void FormMain_Load(object sender, EventArgs e)
        {
            initiate();
            //startThisServer();
            //timer1.Start();
            string path = getFilePath();

            programCamera = execute(path);
        }

        void initiate()
        {
            this.Text += (" - " + port.ToString());
            labelMain.Text = "";
            labelName1.Text = "Camera Program";
            labelName2.Text = "Server Program";
            labelStatus1.Text = "";
            labelStatus2.Text = "";
            labelPath1.Text = "";// programCameraPath;
            labelPath2.Text = "";// programServerPath;
            labelPort1.Text = port1.ToString();
            labelPort2.Text = port2.ToString();
            buttonExecute2.Enabled = false;
        }

        void cameraProgramCallback(object sender, DataReceivedEventArgs e)
        {
            labelMain.Text = e.Data;
        }

        private void Read(StreamReader reader)
        {
            new Thread(() =>
            {
                while (true)
                {
                    int current;
                    while ((current = reader.Read()) >= 0)
                    {
                        labelMain.Text += (char)current;
                    }
                }
            }).Start();
        }

        private void buttonExecute1_Click(object sender, EventArgs e)
        {
            string path = getFilePath();

            programCamera = execute(path);
            //programCamera.OutputDataReceived += cameraProgramCallback;
            //programCamera.StandardInput.WriteLine("Hello");
            //programCamera.StandardInput.write
            //Read(programCamera.StandardOutput);

            /*try
            {
                //programCamera = Process.Start(labelPath1.Text);
                Process.Start(labelPath1.Text);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
                setFilePath(labelPath1);
                try
                {
                    programCamera = Process.Start(labelPath1.Text);
                }
                catch (Exception) { }
            }

            if (programCamera != null)
            {
                //socket1 = AsynchronousClient.Connect("locanhost", port1);
            }*/
        }

        private void buttonExecute2_Click(object sender, EventArgs e)
        {/*
            try
            {
                programServer = cmdExecute();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
                setFilePath(labelPath2);
                try
                {
                    programServer = cmdExecute();
                }
                catch (Exception) { }
            }

            if (programCamera != null)
            {
                //socket2 = AsynchronousClient.Connect("locanhost", port2);
            }/*/
        }

        Process execute(string path)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            Process process = new Process();

            startInfo.FileName = path;
            //startInfo.CreateNoWindow = false;
            startInfo.UseShellExecute = false;

            // Process에게서 데이터 받기
            startInfo.RedirectStandardOutput = true;
            startInfo.RedirectStandardInput = true;
            startInfo.RedirectStandardError = true;

            process.StartInfo = startInfo;
            process.Start();

            //process.StandardInput.Write(@"python " + programServerPath + Environment.NewLine);
            process.StandardInput.WriteLine("HIHIHI\r\n");
            process.WaitForExit(10000);
            return process;
        }

        void clearProcessRedirect(Process p)
        {
            if (p.StandardInput != null) p.StandardInput.Close();
            if (p.StandardOutput != null) p.StandardOutput.Close();
            if (p.StandardError != null) p.StandardError.Close();
        }

        string getFilePath()
        {

            OpenFileDialog fd = new OpenFileDialog();
            //fd.Filter = "Executable File|.exe";

            if (fd.ShowDialog() == DialogResult.OK)
            {
                return fd.FileName;
                //label.Text = fd.FileName;
            }

            return "";
        }

        private void startThisServer()
        {
            AsynchronousClient.Received += recv;
            AsynchronousClient.RecievingLoop(port);
        }

        private void FormMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            AsynchronousClient.receiving = false;
            AsynchronousClient.listenDone.Set();

            if (socket1 != null) AsynchronousClient.closeSocket(socket1);
            if (socket2 != null) AsynchronousClient.closeSocket(socket2);


            if (programCamera != null) clearProcessRedirect(programCamera);
            if (programServer != null) clearProcessRedirect(programServer);

            if (programCamera != null) programCamera.Kill();
            if (programServer != null) programServer.Kill();
        }

        private void recv(string arg)
        {
            if (arg.StartsWith("[REQUEST]"))
            {
                removePrefixPostfix(arg, "[REQUEST]", "<EOF>");

                labelMain.Text = "데이터 도착, 결과 확인 중...";

                if (!AsynchronousClient.socketConnected(socket2))
                {
                    AsynchronousClient.Send(socket2, arg);
                }
            }
            else if (arg.StartsWith("[RESULT]"))
            {
                removePrefixPostfix(arg, "[RESULT]", "<EOF>");
                
                labelMain.Text = arg;
            }
        }

        private string removePrefixPostfix(string str, string prefix, string postfix)
        {
            string sub = str.Substring(prefix.Length);
            sub = sub.Substring(0, sub.LastIndexOf(postfix));

            return sub;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (programCamera == null)
            {
                labelStatus1.Text = "Closed";
                labelStatus1.ForeColor = Color.Black;
            }
            if (programServer == null)
            {
                labelStatus2.Text = "Closed";
                labelStatus1.ForeColor = Color.Black;
            }

            if (programCamera != null && AsynchronousClient.socketConnectedPoll(socket1))
            {
                labelStatus1.Text = "Connecting ...";
                labelStatus1.ForeColor = Color.Red;
                socket1 = AsynchronousClient.Connect("localhost", port1);
            }
            else if (programCamera != null)
            {
                labelStatus1.Text = "Connected";
                labelStatus1.ForeColor = Color.Green;
            }

            if (programServer != null && AsynchronousClient.socketConnectedPoll(socket2))
            {
                labelStatus2.Text = "Connecting ...";
                labelStatus2.ForeColor = Color.Red;
                socket2 = AsynchronousClient.Connect("localhost", port2);
            }
            else if (programServer != null)
            {
                labelStatus2.Text = "Connected";
                labelStatus2.ForeColor = Color.Green;
            }
        }
    }
}
