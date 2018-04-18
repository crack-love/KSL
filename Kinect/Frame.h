#pragma once

#include "Include.h"
#include "SPoint.h"

// 손은 HIP ?
// 2채널(왼/오)

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