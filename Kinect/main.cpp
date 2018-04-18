#pragma once

#include <iostream>
#include <windows.h>
#include "app.h"
#include "LabelMapper.h"
#include "..\Network\code_mojo\\mojo.h"

using namespace std;

//#define OUTPUT_LABEL "안녕하세요"
#define OUTPUT_LABEL "바다"

int inputMode(ostream &o, istream &i);
void modeOutput();
void modePredict();
void modeLearning();

int main(int argc, char* argv[])
{
	switch (inputMode(cout, cin))
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

	system("pause");
	return 0;
}

int inputMode(ostream &o, istream &i)
{
	int res; 

	if (o)
	{
		for (int i = 0; i < KINECT_MODE_SIZE; ++i)
		{
			o << i << " : " << to_string((KINECT_MODE)i) << endl;
		}
		o << "Mode : ";
	}

	i >> res;
	return res;
}

void modeOutput()
{
	Kinect k(KINECT_MODE_OUTPUT);
	string label;

	while (true)
	{
		k.run_one_cycle();
		k.setLabel(OUTPUT_LABEL);

		const int key = cv::waitKey(10);
		if (key == VK_ESCAPE) {
			break;
		}
	}
}

void modePredict()
{
	float* framedata;
	mojo::network cnn;
	
	//cnn load
	cnn.read("test3.model");
	framedata = new float[256 * 24 * 2];

	try {
		Kinect kinect(KINECT_MODE_OUTPUT);
		kinect.setDataBuffer(framedata);
		kinect.setLabel("안녕하세요");

		// Main Loop
		while (true) {

			kinect.run_one_cycle();

			if (kinect.isDataReady())
			{
				kinect.setPredict(cnn.predict_class(kinect.getData()));
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

void modeLearning()
{

}