#pragma once

#include "MainTransaction.h"

void MainTransaction::run()
{
	initialize();

	// loop in each menu
	chooseMenu();
}

void MainTransaction::initialize()
{
	// Load LABEL.txt
	LabelMapper::getInstance()->initialize();
}

void MainTransaction::chooseMenu()
{
	SHOW_ENUM(KINECT_MODE, KINECT_MODE_SIZE, 1);

	int menu = INPUT(int, "Mode") - 1;
	cout << ">>> " << to_string((KINECT_MODE)menu) << endl;

	k.setMode((KINECT_MODE)menu);
	switch (menu)
	{
	case KINECT_MODE_OUTPUT:
		modeOutput();
		break;

	case KINECT_MODE_PREDICT:
		modePredict();
		break;

	case KINECT_MODE_LEARNING:
		modeLearning();
		break;
	}
}


void MainTransaction::modeOutput()
{
	int label = INPUT(int, "Recording Label");
	cout << ">>> " << label << ": " << LABEL(label) << endl;
	k.setLabel(label);

	string name = INPUT(string, "Who is Recording");
	cout << ">>> " << name << endl;
	k.setWorkerName(name);

	// 시작 전 대기시간 가짐
	int waitTime = 5;
	cout << "[ESC] to End Recording" << endl;
	for (int i = 0; i < waitTime; ++i)
	{
		cout << waitTime - i << endl;
		Sleep(999);
	}

	while (true)
	{
		k.run_one_cycle();

		const int key = cv::waitKey(10);
		if (key == VK_ESCAPE) {
			break;
		}
	}
}

void MainTransaction::modePredict()
{
	try {
		// Main Loop
		while (true) {

			k.run_one_cycle();

			// Key Check
			const int key = cv::waitKey(10);
			if (key == VK_ESCAPE) {
				break;
			}
		}

	}
	catch (std::exception& ex) {
		std::cout << ex.what() << std::endl;
	}
}

// *not avaliable*  
// **********
// _not avaliable_
void MainTransaction::modeLearning()
{

}