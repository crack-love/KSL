#pragma once

// == mojo ====================================================================
//
//    Copyright (c) gnawice@gnawice.com. All rights reserved.
//	  See LICENSE in root folder
//
//    Permission is hereby granted, free of charge, to any person obtaining a
//    copy of this software and associated documentation files(the "Software"),
//    to deal in the Software without restriction, including without 
//    limitation the rights to use, copy, modify, merge, publish, distribute,
//    sublicense, and/or sell copies of the Software, and to permit persons to
//    whom the Software is furnished to do so, subject to the following 
//    conditions :
//
//    The above copyright notice and this permission notice shall be included
//    in all copies or substantial portions of the Software.
//
//    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
//    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
//    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
//    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
//    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
//    OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
//    THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
// ============================================================================
//    network.h: The main artificial neural network graph for mojo
// ==================================================================== mojo ==

#include <string>
#include <iostream> // cout
#include <fstream>
#include <sstream>
#include <map>
#include <vector>

#include "defines.h"
#include "mojo_layer.h"
#include "mojo_solver.h"
#include "mojo_activation.h"
#include "mojo_cost.h"

// hack for VS2010 to handle c++11 for(:)
/*
#if (_MSC_VER  == 1600)
	#ifndef __for__
	#define __for__ for each
	#define __in__ in
	#endif
#else
	#ifndef __for__
	#define __for__ for
	#define __in__ :
	#endif
#endif*/



#if defined(MOJO_CV2) || defined(MOJO_CV3)

#ifdef MOJO_CV2
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/contrib/contrib.hpp"

#pragma comment(lib, "opencv_core249")
#pragma comment(lib, "opencv_highgui249")
#pragma comment(lib, "opencv_imgproc249")
#pragma comment(lib, "opencv_contrib249")
#else  //#ifdef MOJO_CV3
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#pragma comment(lib, "opencv_world310")
#endif
#endif




namespace mojo
{

#if defined(MOJO_CV2) || defined(MOJO_CV3)
// forward declare these for data augmentation
cv::Mat matrix2cv(const mojo::matrix &m, bool uc8 = false);
mojo::matrix cv2matrix(cv::Mat &m);
mojo::matrix transform(const mojo::matrix in, const int x_center, const int y_center, int out_dim, float theta = 0, float scale = 1.f);
#endif


	// sleep needed for threading
#ifdef _WIN32
#include <windows.h>
	void mojo_sleep(unsigned milliseconds) { Sleep(milliseconds); }
#else
#include <unistd.h>
	void mojo_sleep(unsigned milliseconds) { usleep(milliseconds * 1000); }
#endif

#ifdef MOJO_PROFILE_LAYERS
#ifdef _WIN32
	//* used for profiling layers
	double PCFreq = 0.0;
	__int64 CounterStart = 0;

	void StartCounter()
	{
		LARGE_INTEGER li;
		if (!QueryPerformanceFrequency(&li)) return;
		PCFreq = double(li.QuadPart) / 1000.0;
		QueryPerformanceCounter(&li);
		CounterStart = li.QuadPart;
	}
	double GetCounter()
	{
		LARGE_INTEGER li;
		QueryPerformanceCounter(&li);
		return double(li.QuadPart - CounterStart) / PCFreq;
	}
#else
	void StartCounter(){}
	double GetCounter(){return 0;}
#endif
	
#endif
	//*/



// returns Energy (euclidian distance / 2) and max index
float match_labels(const float *out, const float *target, const int size, int *best_index = NULL)
{
	float E = 0;
	int max_j = 0;
	for (int j = 0; j<size; j++)
	{
		E += (out[j] - target[j])*(out[j] - target[j]);
		if (out[max_j]<out[j]) max_j = j;
	}
	if (best_index) *best_index = max_j;
	E *= 0.5;
	return E;
}
// returns index of highest value (argmax)
int arg_max(const float *out, const int size)
{
	int max_j = 0;
	for (int j = 0; j<size; j++) 
		if (out[max_j]<out[j])  
		{max_j = j; }//std::cout <<j<<",";}
	return max_j;
}

class network;
}
