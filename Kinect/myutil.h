#ifndef UTIL_H
#define UTIL_H

#include "Include.h"

// Error Check Macro
#define ERROR_CHECK( ret )                                        \
    if( FAILED( ret ) ){                                          \
        std::stringstream ss;                                     \
        ss << "failed " #ret " " << std::hex << ret << std::endl; \
        throw std::runtime_error( ss.str().c_str() );             \
    }

// Safe Release
template<class T>
inline void SafeRelease( T*& rel )
{
    if( rel != NULL ){
        rel->Release();
        rel = NULL;
    }
}
/*
// C++ Style Line Types For OpenCV 2.x
#if ( CV_MAJOR_VERSION < 3 )
namespace cv{
	enum LineTypes{
		FILLED  = -1,
		LINE_4  = 4,
		LINE_8  = 8,
		LINE_AA = 16
	};
}
#endif
*/
static double myDistance3d(CameraSpacePoint a, CameraSpacePoint b)
{
	return sqrt(pow(a.X - b.X, 2.0) + pow(a.Y - b.Y, 2.0) + pow(a.Z - b.Z, 2.0));
}

static float Lerp(float p, float x, float y)
{
	if (x > y)
	{
		float temp = x;
		x = y;
		y = temp;
	}

	return  x + (y - x) * p;
}

static bool LerpBool(float p, bool x, bool y)
{
	return p > .5f ? y : x;
}


// 현재시간을 string type으로 return하는 함수
static const std::string currentDateTime() {
	time_t     now = time(0); //현재 시간을 time_t 타입으로 저장
	struct tm  tstruct;
	char       buf[80];
	tstruct = *localtime(&now);
	strftime(buf, sizeof(buf), "%Y-%m-%d.%X", &tstruct); // YYYY-MM-DD.HH:mm:ss 형태의 스트링

	return buf;
}

// 현재시간을 string type으로 return하는 함수(
static const std::string currentDateTime(int isSimple) {
	time_t     now = time(0); //현재 시간을 time_t 타입으로 저장
	struct tm  tstruct;
	char       buf[80];
	tstruct = *localtime(&now);
	strftime(buf, sizeof(buf), "%Y-%m-%d_%H%M%S", &tstruct); // YYYY-MM-DD.HH:mm:ss 형태의 스트링

	return buf;
}

static vector<vector<vector<double>>> dataRoot;
static void test()
{
	static int cnt = 0;
	string fn = "test.txt";
	ifstream is(fn.data());
	string time;
	string label;
	int frameSize;
	int dataSize;
	int channelCnt;

	if (!is.is_open())
	{
		cout << "no file " + fn << endl;
		return;
	}

	while (!is.eof())
	{
		is >> time >> label >> frameSize >> dataSize >> channelCnt;
		if (is.eof()) break;

		cout << ++cnt << " : " << time << " " << label << " " << frameSize << " " << dataSize << " " << channelCnt << endl;
		
		vector<vector<double>> data = vector<vector<double>>(frameSize);
		
		for (int i = 0; i < frameSize; ++i)
		{
			data[i].resize(dataSize * channelCnt);

			for (int j = 0; j < dataSize * channelCnt; ++j)
			{
				is >> data[i][j];
				//if (j < 6) cout << data[i][j] << " ";
			}
		}

		dataRoot.push_back(data);
	}
}



#endif // UTIL_H