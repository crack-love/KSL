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
    [Serializable]
    class UserData
    {
        [NonSerialized]
        const string FILE_PATH = "userdata.dat";

        public string pythonPath = null;
        public string KinectProgramPath = null;
        
        void copy(UserData data)
        {
            pythonPath = data.pythonPath;
            KinectProgramPath = data.KinectProgramPath;
        }

        internal void setFromPrompt()
        {
            string res = Interaction.InputBox("Python path", "plz input", pythonPath);
            if (res.Length > 0) pythonPath = res;

            res = Interaction.InputBox("Kinect Program Path", "plz input", KinectProgramPath);
            if (res.Length > 0) KinectProgramPath = res;
        }

        public void load()
        {
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
        {
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