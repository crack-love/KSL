#pragma once

#include <Kinect.h>
#include <sstream>
#include <array>
#include <string>
#include <vector>
using namespace std;

#include "SPoint.h"
#include "defines.hpp"

// 어떤 부위(손) 기준 distance 계산할 것인지는 defines.hpp에 정의돼있다
// todo : JointType -> Spoint

class Frame
{
private:
	vector<double> distanceL = vector<double>(SPOINT_SIZE);
	vector<double> distanceR = vector<double>(SPOINT_SIZE);
	bool lHandActivated = false;
	bool rHandActivated = false;
	TIMESPAN lastFrameRelativeTime;

public:
	Frame();

	void memorize(CameraSpacePoint lHandPos, CameraSpacePoint rHandPos, array<SPoint, SPOINT_SIZE> sarr, bool la, bool ra, TIMESPAN endtime);

	// for status distance showing
	array<string, Show_Status_DistanceFrame_Size> toString();

	// ForFile
	string toString(int noting);

	TIMESPAN getTime();

	void LerpMe(float p, const Frame &right);

	bool getHAL();
	bool getHAR();
	double getDistanceL(int i);
	double getDistanceR(int i);

	void getData(float* dst);
	
private:


};