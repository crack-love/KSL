using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.Serialization.Formatters.Binary;
using System.Windows.Forms;
using Microsoft.VisualBasic;

namespace Project_Interface2
{
    [Serializable] // UserData를 직렬화 가능하도록 함
    class UserData
    {
        [NonSerialized] // FILE_PATH는 저장할 필요없음으로 직렬화하는데 제외
        const string FILE_PATH = "userdata.dat";

        public string pythonPath = null;
        public string KinectProgramPath = null;
        
        void copy(UserData data)
        {
            pythonPath = data.pythonPath;
            KinectProgramPath = data.KinectProgramPath;
        }

        internal void setFromPrompt()
        {   // prompt를 통해 python 경로, kinectProgram 경로를 입력받아 변수에 저장
            string res = Interaction.InputBox("Python path", "plz input", pythonPath);
            if (res.Length > 0) pythonPath = res;

            res = Interaction.InputBox("Kinect Program Path", "plz input", KinectProgramPath);
            if (res.Length > 0) KinectProgramPath = res;
        }

        public void load()
        {   // FILE_PATH에 저장된 직렬화된 UserData를 역직렬화 하여 불러옴
            try
            {
                using (FileStream fs = new FileStream(FILE_PATH, FileMode.Open))
                {
                    BinaryFormatter formatter = new BinaryFormatter();
                    UserData data = (UserData)formatter.Deserialize(fs);
                    fs.Close();

                    copy(data);
                }
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message + " 파일을 새로 만듭니다.");
            }
        }

        public void save()
        {   // 객체를 직렬화하여 FILE_PATH에 저장
            try
            {
                FileStream fs = new FileStream(FILE_PATH, FileMode.OpenOrCreate);

                BinaryFormatter formatter = new BinaryFormatter();
                formatter.Serialize(fs, this);
                fs.Close();
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message);
            }
        }
    }
}