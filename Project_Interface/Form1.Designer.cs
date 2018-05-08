namespace Project_Interface2
{
    partial class Form
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
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.tableLayoutPanel3 = new System.Windows.Forms.TableLayoutPanel();
            this.buttonCloseAll = new System.Windows.Forms.Button();
            this.buttonSet = new System.Windows.Forms.Button();
            this.tableLayoutPanel2 = new System.Windows.Forms.TableLayoutPanel();
            this.buttonRight = new System.Windows.Forms.Button();
            this.buttonLeft = new System.Windows.Forms.Button();
            this.textBoxInputLeft = new System.Windows.Forms.TextBox();
            this.textBoxInputRight = new System.Windows.Forms.TextBox();
            this.textBoxOutputRight = new System.Windows.Forms.TextBox();
            this.labelStatusRight = new System.Windows.Forms.Label();
            this.textBoxOutputLeft = new System.Windows.Forms.TextBox();
            this.labelStatusLeft = new System.Windows.Forms.Label();
            this.labelMain = new System.Windows.Forms.Label();
            this.tableLayoutPanel1.SuspendLayout();
            this.tableLayoutPanel3.SuspendLayout();
            this.tableLayoutPanel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel3, 0, 2);
            this.tableLayoutPanel1.Controls.Add(this.tableLayoutPanel2, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.labelMain, 0, 0);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 3;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 30F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 70F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(794, 501);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // tableLayoutPanel3
            // 
            this.tableLayoutPanel3.ColumnCount = 2;
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel3.Controls.Add(this.buttonCloseAll, 0, 0);
            this.tableLayoutPanel3.Controls.Add(this.buttonSet, 1, 0);
            this.tableLayoutPanel3.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel3.Location = new System.Drawing.Point(0, 475);
            this.tableLayoutPanel3.Margin = new System.Windows.Forms.Padding(0);
            this.tableLayoutPanel3.Name = "tableLayoutPanel3";
            this.tableLayoutPanel3.RowCount = 1;
            this.tableLayoutPanel3.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel3.Size = new System.Drawing.Size(794, 26);
            this.tableLayoutPanel3.TabIndex = 1;
            // 
            // buttonCloseAll
            // 
            this.buttonCloseAll.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.buttonCloseAll.Dock = System.Windows.Forms.DockStyle.Fill;
            this.buttonCloseAll.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonCloseAll.Location = new System.Drawing.Point(0, 0);
            this.buttonCloseAll.Margin = new System.Windows.Forms.Padding(0);
            this.buttonCloseAll.Name = "buttonCloseAll";
            this.buttonCloseAll.Size = new System.Drawing.Size(397, 26);
            this.buttonCloseAll.TabIndex = 2;
            this.buttonCloseAll.TabStop = false;
            this.buttonCloseAll.Text = "Close All (ESC)";
            this.buttonCloseAll.UseVisualStyleBackColor = true;
            this.buttonCloseAll.Click += new System.EventHandler(this.buttonCloseAll_Click);
            // 
            // buttonSet
            // 
            this.buttonSet.Dock = System.Windows.Forms.DockStyle.Fill;
            this.buttonSet.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonSet.Location = new System.Drawing.Point(397, 0);
            this.buttonSet.Margin = new System.Windows.Forms.Padding(0);
            this.buttonSet.Name = "buttonSet";
            this.buttonSet.Size = new System.Drawing.Size(397, 26);
            this.buttonSet.TabIndex = 3;
            this.buttonSet.Text = "Set";
            this.buttonSet.UseVisualStyleBackColor = true;
            this.buttonSet.Click += new System.EventHandler(this.buttonSet_Click);
            // 
            // tableLayoutPanel2
            // 
            this.tableLayoutPanel2.ColumnCount = 2;
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel2.Controls.Add(this.buttonRight, 1, 3);
            this.tableLayoutPanel2.Controls.Add(this.buttonLeft, 0, 3);
            this.tableLayoutPanel2.Controls.Add(this.textBoxInputLeft, 0, 2);
            this.tableLayoutPanel2.Controls.Add(this.textBoxInputRight, 1, 2);
            this.tableLayoutPanel2.Controls.Add(this.textBoxOutputRight, 1, 1);
            this.tableLayoutPanel2.Controls.Add(this.labelStatusRight, 1, 0);
            this.tableLayoutPanel2.Controls.Add(this.textBoxOutputLeft, 0, 1);
            this.tableLayoutPanel2.Controls.Add(this.labelStatusLeft, 0, 0);
            this.tableLayoutPanel2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel2.Location = new System.Drawing.Point(0, 142);
            this.tableLayoutPanel2.Margin = new System.Windows.Forms.Padding(0);
            this.tableLayoutPanel2.Name = "tableLayoutPanel2";
            this.tableLayoutPanel2.RowCount = 4;
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel2.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
            this.tableLayoutPanel2.Size = new System.Drawing.Size(794, 333);
            this.tableLayoutPanel2.TabIndex = 0;
            // 
            // buttonRight
            // 
            this.buttonRight.Dock = System.Windows.Forms.DockStyle.Fill;
            this.buttonRight.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonRight.Location = new System.Drawing.Point(397, 308);
            this.buttonRight.Margin = new System.Windows.Forms.Padding(0);
            this.buttonRight.Name = "buttonRight";
            this.buttonRight.Size = new System.Drawing.Size(397, 25);
            this.buttonRight.TabIndex = 5;
            this.buttonRight.Text = "Execute";
            this.buttonRight.UseVisualStyleBackColor = true;
            this.buttonRight.Click += new System.EventHandler(this.buttonRight_Click);
            // 
            // buttonLeft
            // 
            this.buttonLeft.Dock = System.Windows.Forms.DockStyle.Fill;
            this.buttonLeft.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonLeft.Location = new System.Drawing.Point(0, 308);
            this.buttonLeft.Margin = new System.Windows.Forms.Padding(0);
            this.buttonLeft.Name = "buttonLeft";
            this.buttonLeft.Size = new System.Drawing.Size(397, 25);
            this.buttonLeft.TabIndex = 4;
            this.buttonLeft.Text = "Execute";
            this.buttonLeft.UseVisualStyleBackColor = true;
            this.buttonLeft.Click += new System.EventHandler(this.buttonLeft_Click);
            // 
            // textBoxInputLeft
            // 
            this.textBoxInputLeft.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxInputLeft.Location = new System.Drawing.Point(0, 283);
            this.textBoxInputLeft.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxInputLeft.Multiline = true;
            this.textBoxInputLeft.Name = "textBoxInputLeft";
            this.textBoxInputLeft.Size = new System.Drawing.Size(397, 25);
            this.textBoxInputLeft.TabIndex = 2;
            this.textBoxInputLeft.Text = "textBoxInputLeft";
            this.textBoxInputLeft.KeyDown += new System.Windows.Forms.KeyEventHandler(this.textBoxInputLeft_KeyDown);
            // 
            // textBoxInputRight
            // 
            this.textBoxInputRight.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxInputRight.Location = new System.Drawing.Point(397, 283);
            this.textBoxInputRight.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxInputRight.Multiline = true;
            this.textBoxInputRight.Name = "textBoxInputRight";
            this.textBoxInputRight.Size = new System.Drawing.Size(397, 25);
            this.textBoxInputRight.TabIndex = 3;
            this.textBoxInputRight.Text = "textBoxInputRight";
            this.textBoxInputRight.KeyDown += new System.Windows.Forms.KeyEventHandler(this.textBoxInputRight_KeyDown);
            // 
            // textBoxOutputRight
            // 
            this.textBoxOutputRight.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxOutputRight.Font = new System.Drawing.Font("돋움체", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.textBoxOutputRight.Location = new System.Drawing.Point(397, 20);
            this.textBoxOutputRight.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxOutputRight.Multiline = true;
            this.textBoxOutputRight.Name = "textBoxOutputRight";
            this.textBoxOutputRight.ReadOnly = true;
            this.textBoxOutputRight.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.textBoxOutputRight.Size = new System.Drawing.Size(397, 263);
            this.textBoxOutputRight.TabIndex = 7;
            this.textBoxOutputRight.TabStop = false;
            this.textBoxOutputRight.Text = "textBoxOutputRight";
            // 
            // labelStatusRight
            // 
            this.labelStatusRight.AutoSize = true;
            this.labelStatusRight.BackColor = System.Drawing.SystemColors.Control;
            this.labelStatusRight.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.labelStatusRight.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelStatusRight.Location = new System.Drawing.Point(397, 0);
            this.labelStatusRight.Margin = new System.Windows.Forms.Padding(0);
            this.labelStatusRight.Name = "labelStatusRight";
            this.labelStatusRight.Size = new System.Drawing.Size(397, 20);
            this.labelStatusRight.TabIndex = 9;
            this.labelStatusRight.Text = "labelStatusRight";
            this.labelStatusRight.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // textBoxOutputLeft
            // 
            this.textBoxOutputLeft.Dock = System.Windows.Forms.DockStyle.Fill;
            this.textBoxOutputLeft.Font = new System.Drawing.Font("돋움체", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.textBoxOutputLeft.Location = new System.Drawing.Point(0, 20);
            this.textBoxOutputLeft.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxOutputLeft.Multiline = true;
            this.textBoxOutputLeft.Name = "textBoxOutputLeft";
            this.textBoxOutputLeft.ReadOnly = true;
            this.textBoxOutputLeft.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.textBoxOutputLeft.Size = new System.Drawing.Size(397, 263);
            this.textBoxOutputLeft.TabIndex = 7;
            this.textBoxOutputLeft.TabStop = false;
            this.textBoxOutputLeft.Text = "textBoxOutputLeft";
            // 
            // labelStatusLeft
            // 
            this.labelStatusLeft.AutoSize = true;
            this.labelStatusLeft.BackColor = System.Drawing.SystemColors.Control;
            this.labelStatusLeft.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.labelStatusLeft.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelStatusLeft.Location = new System.Drawing.Point(0, 0);
            this.labelStatusLeft.Margin = new System.Windows.Forms.Padding(0);
            this.labelStatusLeft.Name = "labelStatusLeft";
            this.labelStatusLeft.Size = new System.Drawing.Size(397, 20);
            this.labelStatusLeft.TabIndex = 8;
            this.labelStatusLeft.Text = "labelStatusLeft";
            this.labelStatusLeft.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelMain
            // 
            this.labelMain.AutoSize = true;
            this.labelMain.BackColor = System.Drawing.Color.White;
            this.labelMain.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelMain.Font = new System.Drawing.Font("굴림", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            this.labelMain.Location = new System.Drawing.Point(3, 0);
            this.labelMain.Name = "labelMain";
            this.labelMain.Size = new System.Drawing.Size(788, 142);
            this.labelMain.TabIndex = 1;
            this.labelMain.Text = "labelMain";
            this.labelMain.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // Form
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.buttonCloseAll;
            this.ClientSize = new System.Drawing.Size(794, 501);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Name = "Form";
            this.Text = "Predic_demo";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form_FormClosing);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.tableLayoutPanel3.ResumeLayout(false);
            this.tableLayoutPanel2.ResumeLayout(false);
            this.tableLayoutPanel2.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel2;
        private System.Windows.Forms.TextBox textBoxInputLeft;
        private System.Windows.Forms.TextBox textBoxInputRight;
        private System.Windows.Forms.Button buttonLeft;
        private System.Windows.Forms.Button buttonRight;
        private System.Windows.Forms.TextBox textBoxOutputRight;
        private System.Windows.Forms.TextBox textBoxOutputLeft;
        private System.Windows.Forms.Label labelMain;
        private System.Windows.Forms.Button buttonCloseAll;
        private System.Windows.Forms.Label labelStatusLeft;
        private System.Windows.Forms.Label labelStatusRight;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel3;
        private System.Windows.Forms.Button buttonSet;
    }
}

