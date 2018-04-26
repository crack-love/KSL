#pragma once

#include "MainTransaction.h"

void MainTransaction::run()
{
	initialize();

	// loop in which menu
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

	switch (INPUT(int, "MODE") - 1)
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

	default:
		break;
	}
}


void MainTransaction::modeOutput()
{
	Kinect k(KINECT_MODE_OUTPUT);
	int label = INPUT(int, "LABEL");
	k.setLabel(label);

	while (true)
	{
		k.run_one_cycle();

		const int key = cv::waitKey(10);
		if (key == VK_ESCAPE) {
			break;
		}
	}
}

// not avaliable  
// not avaliable
void MainTransaction::modePredict()
{
	//float* framedata;
	//mojo::network cnn;

	//cnn load
	//cnn.read("test3.model");
	//framedata = new float[256 * 24 * 2];

	try {
		Kinect kinect(KINECT_MODE_PREDICT);
		//kinect.setDataBuffer(framedata);
		kinect.setLabel(1);

		// Main Loop
		while (true) {

			if (kinect.isComplete())
				kinect.run_one_cycle();

			if (kinect.isDataReady())
			{
				// kinect.setPredict(cnn.predict_class(kinect.getData()));
				//memset(framedata, 0, 256 * 24 * 2);
			}

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