#pragma once

#include <Kinect.h>
#include <sstream>
#include <array>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;

#include "common/defines.hpp"

// 어떤 부위(손) 기준 distance 계산할 것인지는 defines.hpp에 정의돼있다
// todo : JointType -> Spoint

class ImageFrame
{
private:
	cv::Mat image;
	TIMESPAN lastFrameRelativeTime;

public:
	ImageFrame();

	void memorize(cv::Mat image, TIMESPAN endtime);

	// ForFile
	// string toString(int noting);
	void save(string filename);

	TIMESPAN getTime();

	void LerpMe(float p, const ImageFrame &right);

	void toString(stringstream &s, char delimeter);

private:
};