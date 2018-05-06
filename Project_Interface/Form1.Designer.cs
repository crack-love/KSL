namespace Project_Interface
{
    partial class FormMain
    {
        /// <summary>
        /// 필수 디자이너 변수입니다.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 사용 중인 모든 리소스를 정리합니다.
        /// </summary>
        /// <param name="disposing">관리되는 리소스를 삭제해야 하면 true이고, 그렇지 않으면 false입니다.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 디자이너에서 생성한 코드

        /// <summary>
        /// 디자이너 지원에 필요한 메서드입니다. 
        /// 이 메서드의 내용을 코드 편집기로 수정하지 마세요.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.labelMain = new System.Windows.Forms.Label();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.labelStatus1 = new System.Windows.Forms.Label();
            this.labelStatus2 = new System.Windows.Forms.Label();
            this.labelName1 = new System.Windows.Forms.Label();
            this.labelName2 = new System.Windows.Forms.Label();
            this.buttonExecute1 = new System.Windows.Forms.Button();
            this.buttonExecute2 = new System.Windows.Forms.Button();
            this.labelPath2 = new System.Windows.Forms.Label();
            this.labelPath1 = new System.Windows.Forms.Label();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.labelPort1 = new System.Windows.Forms.Label();
            this.labelPort2 = new System.Windows.Forms.Label();
            this.tableLayoutPanel1.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.BackColor = System.Drawing.Color.White;
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Controls.Add(this.labelMain, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 1);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 2;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 60F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 40F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(478, 245);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // labelMain
            // 
            this.labelMain.AutoSize = true;
            this.labelMain.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.labelMain.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelMain.Font = new System.Drawing.Font("나눔바른고딕", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.labelMain.Location = new System.Drawing.Point(3, 0);
            this.labelMain.Name = "labelMain";
            this.labelMain.Size = new System.Drawing.Size(472, 147);
            this.labelMain.TabIndex = 0;
            this.labelMain.Text = "label1";
            this.labelMain.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.BackColor = System.Drawing.SystemColors.Control;
            this.tableLayoutPanel2.ColumnCount = 5;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
            this.tableLayoutPanel2.Controls.Add(this.labelStatus1, 1, 0);
            this.tableLayoutPanel2.Controls.Add(this.labelStatus2, 1, 1);
            this.tableLayoutPanel2.Controls.Add(this.labelName1, 0, 0);
            this.tableLayoutPanel2.Controls.Add(this.labelName2, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.buttonExecute1, 4, 0);
            this.tableLayoutPanel2.Controls.Add(this.buttonExecute2, 4, 1);
            this.tableLayoutPanel2.Controls.Add(this.labelPath2, 2, 1);
            this.tableLayoutPanel2.Controls.Add(this.labelPath1, 2, 0);
            this.tableLayoutPanel2.Controls.Add(this.labelPort1, 3, 0);
            this.tableLayoutPanel2.Controls.Add(this.labelPort2, 3, 1);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(3, 150);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 2;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(472, 92);
            this.tableLayoutPanel2.TabIndex = 1;
            // 
            // labelStatus1
            // 
            this.labelStatus1.AutoSize = true;
            this.labelStatus1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelStatus1.Location = new System.Drawing.Point(97, 0);
            this.labelStatus1.Name = "labelStatus1";
            this.labelStatus1.Size = new System.Drawing.Size(88, 46);
            this.labelStatus1.TabIndex = 1;
            this.labelStatus1.Text = "label1";
            this.labelStatus1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelStatus2
            // 
            this.labelStatus2.AutoSize = true;
            this.labelStatus2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelStatus2.Location = new System.Drawing.Point(97, 46);
            this.labelStatus2.Name = "labelStatus2";
            this.labelStatus2.Size = new System.Drawing.Size(88, 46);
            this.labelStatus2.TabIndex = 2;
            this.labelStatus2.Text = "label2";
            this.labelStatus2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelName1
            // 
            this.labelName1.AutoSize = true;
            this.labelName1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelName1.Location = new System.Drawing.Point(3, 0);
            this.labelName1.Name = "labelName1";
            this.labelName1.Size = new System.Drawing.Size(88, 46);
            this.labelName1.TabIndex = 3;
            this.labelName1.Text = "label3";
            this.labelName1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelName2
            // 
            this.labelName2.AutoSize = true;
            this.labelName2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelName2.Location = new System.Drawing.Point(3, 46);
            this.labelName2.Name = "labelName2";
            this.labelName2.Size = new System.Drawing.Size(88, 46);
            this.labelName2.TabIndex = 4;
            this.labelName2.Text = "label4";
            this.labelName2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // buttonExecute1
            // 
            this.buttonExecute1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.buttonExecute1.Location = new System.Drawing.Point(379, 3);
            this.buttonExecute1.Name = "buttonExecute1";
            this.buttonExecute1.Size = new System.Drawing.Size(90, 40);
            this.buttonExecute1.TabIndex = 0;
            this.buttonExecute1.Text = "Execute";
            this.buttonExecute1.UseVisualStyleBackColor = true;
            this.buttonExecute1.Click += new System.EventHandler(this.buttonExecute1_Click);
            // 
            // buttonExecute2
            // 
            this.buttonExecute2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.buttonExecute2.Location = new System.Drawing.Point(379, 49);
            this.buttonExecute2.Name = "buttonExecute2";
            this.buttonExecute2.Size = new System.Drawing.Size(90, 40);
            this.buttonExecute2.TabIndex = 0;
            this.buttonExecute2.Text = "Execute";
            this.buttonExecute2.UseVisualStyleBackColor = true;
            this.buttonExecute2.Click += new System.EventHandler(this.buttonExecute2_Click);
            // 
            // labelPath2
            // 
            this.labelPath2.AutoSize = true;
            this.labelPath2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelPath2.Location = new System.Drawing.Point(191, 46);
            this.labelPath2.Name = "labelPath2";
            this.labelPath2.Size = new System.Drawing.Size(88, 46);
            this.labelPath2.TabIndex = 6;
            this.labelPath2.Text = "label2";
            this.labelPath2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelPath1
            // 
            this.labelPath1.AutoSize = true;
            this.labelPath1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelPath1.Location = new System.Drawing.Point(191, 0);
            this.labelPath1.Name = "labelPath1";
            this.labelPath1.Size = new System.Drawing.Size(88, 46);
            this.labelPath1.TabIndex = 5;
            this.labelPath1.Text = "label1";
            this.labelPath1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // timer1
            // 
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // labelPort1
            // 
            this.labelPort1.AutoSize = true;
            this.labelPort1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelPort1.Location = new System.Drawing.Point(285, 0);
            this.labelPort1.Name = "labelPort1";
            this.labelPort1.Size = new System.Drawing.Size(88, 46);
            this.labelPort1.TabIndex = 7;
            this.labelPort1.Text = "label1";
            this.labelPort1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelPort2
            // 
            this.labelPort2.AutoSize = true;
            this.labelPort2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelPort2.Location = new System.Drawing.Point(285, 46);
            this.labelPort2.Name = "labelPort2";
            this.labelPort2.Size = new System.Drawing.Size(88, 46);
            this.labelPort2.TabIndex = 8;
            this.labelPort2.Text = "label2";
            this.labelPort2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(478, 245);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Name = "FormMain";
            this.Text = "KSL_Presentation";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FormMain_FormClosing);
            this.Load += new System.EventHandler(this.FormMain_Load);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.Label labelMain;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.Label labelStatus1;
        private System.Windows.Forms.Label labelStatus2;
        private System.Windows.Forms.Label labelName1;
        private System.Windows.Forms.Label labelName2;
        private System.Windows.Forms.Button buttonExecute1;
        private System.Windows.Forms.Button buttonExecute2;
        private System.Windows.Forms.Label labelPath1;
        private System.Windows.Forms.Label labelPath2;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label labelPort1;
        private System.Windows.Forms.Label labelPort2;
    }
}

