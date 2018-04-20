#pragma once

#include <iostream>

#include "defines.hpp"
#include "kinectProgram.h"

class MainTransaction
{
public:
	void run();

private:
	void initialize();
	void chooseMenu();

	void modeOutput();
	void modePredict();
	void modeLearning();
};