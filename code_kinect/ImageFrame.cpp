#include "ImageFrame.h"

ImageFrame::ImageFrame()
{
}

void ImageFrame::memorize(cv::Mat image, TIMESPAN endtime)
{
	this->image = image;
	this->lastFrameRelativeTime = endtime;
}

string ImageFrame::toString(int nothing)
{
	stringstream sstream;

	/*
	int dim = image.dims;
	for (int i = 0; i < dim; ++i)
	{
		if (i) std::cout << " X ";
		std::cout << image.size[i];
	}
	*/

	
	int rows = image.rows;
	int cols = image.cols;
	// cout << rows << " " << cols << endl;
	for (int y = 0; y < rows; ++y)
		for (int x = 0; x < cols; ++x)
		{
			cout << image.at<cv::Vec4b>(y, x)[0] << " ";
			sstream << image.at<cv::Vec4b>(y, x)[0] << " ";
		}

	/*
	for (int y = 0; y < rows; ++y)
		for (int x = 0; x < cols; ++x)
		{
			sstream << image.at<cv::Vec3d>(y, x)[1] << " ";
		}

	for (int y = 0; y < rows; ++y)
		for (int x = 0; x < cols; ++x)
		{
			sstream << image.at<cv::Vec3d>(y, x)[2] << " ";
		}
		*/

	return sstream.str();
}


TIMESPAN ImageFrame::getTime()
{
	return this->lastFrameRelativeTime;
}

void ImageFrame::LerpMe(float p, const ImageFrame & right)
{
	cv::addWeighted(image, 1.0 - p, right.image, p, 0.0, image);
}
