#pragma once

#define _WINSOCKAPI_ 
#include "MainTransaction.h"

#include <string>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{/*
	string path = string(PATH_DATA_FOLDER) + "test.png";
	cout << path << endl;
	cv::Mat mat = cv::imread(path, CV_LOAD_IMAGE_COLOR);
	
	namedWindow("display", WINDOW_AUTOSIZE);
	imshow("display", mat);
	
	cv::Size size = mat.size();
	int total = size.width * size.height * mat.channels();
	std::cout << "Mat size = " << total << std::endl;

	std::vector<uchar> data(mat.ptr(), mat.ptr() + total);
	std::string s(data.begin(), data.end());
	std::cout << "String size = " << s.length() << std::endl;

	Mat dataMat(size, CV_8UC3);
	memcpy(dataMat.data, data.data(), data.size());
	
	namedWindow("cvt", WINDOW_AUTOSIZE);
	cv::imshow("cvt", dataMat);
	*/
	MainTransaction m;
	m.run();
	

	waitKey(0);
	return 0;
}