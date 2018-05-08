#pragma once

#include <iostream>

#include "common/defines.hpp"
#include "kinectProgram.h"

class MainTransaction
{
private:
	Kinect k;

public:
	void run();

private:
	void initialize();
	void chooseMenu();

	void modeOutput();
	void modePredict();
	void modeLearning();
};