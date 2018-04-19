#pragma once

#include <iostream>

#include "defines.hpp"
#include "kinectProgram.h"

void modeOutput();
void modePredict();
void modeLearning();

int main(int argc, char* argv[])
{
	show_hello();
	SHOW_ENUM(KINECT_MODE, KINECT_MODE_SIZE);

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

	system("pause");
	return 0;
}

void modeOutput()
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
void modePredict()
{
	float* framedata;
	//mojo::network cnn;
	
	//cnn load
	//cnn.read("test3.model");
	framedata = new float[256 * 24 * 2];

	try {
		Kinect kinect(KINECT_MODE_OUTPUT);
		kinect.setDataBuffer(framedata);
		kinect.setLabel("æ»≥Á«œººø‰");

		// Main Loop
		while (true) {

			kinect.run_one_cycle();

			if (kinect.isDataReady())
			{
				//kinect.setPredict(cnn.predict_class(kinect.getData()));
				memset(framedata, 0, 256 * 24 * 2);
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
void modeLearning()
{

}