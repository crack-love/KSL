#pragma once

#include <io.h> // folder search
#include <ctime>
#include <immintrin.h> // for correct mojo compile bug..
#include <vector> // vector
#include <utility> // pair
using namespace std;

#include "mojo_util.h"
#include "mojo_network.h"
#include "LabelMapper.h"

using DATA = pair<vector<float>,int>;

class machineLearning
{
private:
	/// »ó¼ö°ª
	const string data_path_train = "images/train/";
	const string data_path_test = "images/test/";
	const string data_path_snapshot = "models/snapshots/";
	const string data_path_model = "models/model";
	const int mini_batch_size = 16;
	const float initial_learning_rate = 0.01f;

	vector<DATA> data_train;
	vector<DATA> data_test;
	mojo::network cnn;
	mojo::html_log log;
	
public:
	machineLearning();
	
	void run();

private:
	void initialize();

	void initializeNetwork();

	void load();

	void loadImage();

	void loadModel();

	void listFolder(string folderPath, _Out_ vector<string> *fileList, bool clearList);

	void loadFile(_In_ vector<string> *list, _Out_ vector<DATA> *datas);

	void train();

	void train_single_epoch(_Out_ float &time);

	float test(_In_ vector<DATA> &data);

	void save();

	void save(_In_ string &fn);
};