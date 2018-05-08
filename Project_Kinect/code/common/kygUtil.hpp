#pragma once

#include <cmath>
#include <iostream>
#include <cstdlib> // system
#include <chrono>
#include <time.h> // localtime_s
#include <string>
using namespace std;

	// 솔루션, 프로젝트 네임 출력
	// deprecated
	static void show_hello()
	{
		cout << "$(SolutionName) - $(ProjectName)" << endl;
	}

	// if fail, system("pause"), throw runtim-err
	inline void fail_than_stop(int t, string m)
	{
		if (t <= 0)
		{
			std::cerr << "CRITICAL FAIL, STOP PROGRAM : " << m << std::endl;
			system("pause");

			throw std::runtime_error(m);
		}
	}

	// InputType은 oerator >> 오버로딩 필요
	template <class InputType>
	static InputType input_something(istream &i, ostream &o, string m)
	{
		InputType res;

		o << string(35, '-') << endl;
		o << m << "? " << endl;
		i >> res;

		return res;
	}

	// EnumType은 to_string 오버로딩 필요
	template <class EnumType>
	static void show_enumeration(ostream &o, int size, int padding)
	{
		for (int i = 0; i < size; ++i)
		{
			o << (i + padding) << " - " << to_string((EnumType)i) << endl;
		}
	}

	// Safe Release
	template<class T>
	inline void SafeRelease(T*& rel)
	{
		if (rel != NULL)
		{
			rel->Release();
			rel = NULL;
		}
	}

	// point has x, y
	template <class Point2D>
	inline double distance3d(Point2D a, Point2D b)
	{
		return sqrt(pow(a.X - b.X, 2.0) + pow(a.Y - b.Y, 2.0) + pow(a.Z - b.Z, 2.0));
	}

	inline float Lerp(float p, float x, float y)
	{
		if (x > y)
		{
			float temp = x;
			x = y;
			y = temp;
		}

		return  x + (y - x) * p;
	}

	inline bool LerpBool(float p, bool x, bool y)
	{
		return p > .5f ? y : x;
	}


	// 현재시간을 string type으로 return하는 함수  
	// "%Y-%m-%d_%H%M%S"
	static string currentDateTime()
	{
		auto now = chrono::system_clock::now();
		auto formatedTime = chrono::system_clock::to_time_t(now);
		tm localizedTime;
		static char buf[80];

		localtime_s(&localizedTime, &formatedTime);
		strftime(buf, sizeof(buf), "%Y-%m-%d_%H%M%S", &localizedTime);

		return buf;
	}

	/*
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
*/