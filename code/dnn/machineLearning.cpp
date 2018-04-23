#include "machineLearning.h"
#include "defines.h"

machineLearning::machineLearning()
{

}

void machineLearning::run()
{
	initialize();

	load();

	train();

	save();
}

void machineLearning::initialize()
{
	std::srand(unsigned(std::time(0)));

	cnn = mojo::network("adam"); // "sgd", "rmsprop", "adagrad", "adam"

	log.set_note(cnn.get_configuration());
	log.set_table_header("epoch\ttest accuracy(%)\testimated accuracy(%)\tepoch time(s)\ttotal time(s)\tlearn rate\tmodel");
}

void machineLearning::initializeNetwork()
{
	using namespace mojo;

	cnn.enable_external_threads();
	cnn.set_mini_batch_size(mini_batch_size);
	cnn.set_smart_training(true);
	cnn.set_learning_rate(initial_learning_rate);

	//cnn.set_random_augmentation(2, 2, 0, 0, mojo::edge); // augment data random shifts

	/////////////////////////////////////////////////////////////////////////////////////////////////////*
	// input				<width> <height> <channels>
	//						Currently only square inputs are supported if you intend to do convolutions.
	//
	// convolution			<kernel size> <out channels> <stride/step size> <activation>
	//						Only square kernels are supported for now with step/stride=1
	//						Optimized and SSE implementations exist for 2x2, 3x3 and 5x5 convolutions.

	// softmax				<nodes>
	//
	// max_pool				<size> <stride>
	//						No additional padding is performed on the layers, so if you try to pool a
	//						15x15 layer by a factor of 2, you will end up with a 7x7 layer.
	//
	// semi_stochastic_pool	<size> <stride>
	//
	// mfm					<maps to pool>
	//						Max Feature Map (MFM)
	//
	// fully_connected		<nodes> <activation>
	//
	// dropout				<fraction to drop>
	//
	// deepcnet				<output channels> <activation>
	//
	// concatenate			<feature map size> <pad_type>
	//
	// resize				<feature map size> <pad_type>
	//
	/////////////////////////////////////////////////////////////////////////////////////////////////////*/

	cnn.push_back("I1", "input 76 76 1");				// 24 x 256 x 2
	cnn.push_back("C2", "convolution 3 3 18 2 relu");	// 24 x (241-15)/2 + 1 = 24 * 114				
	cnn.push_back("C3", "convolution 3 3 22 2 relu");	// 21 x (114-24)/5 + 1 = 24 * 19
	cnn.push_back("FC1", "softmax 2");
	cnn.connect_all();
	// connect() to manually

}

void machineLearning::load()
{
	loadImage();

	loadModel();
}

void machineLearning::loadImage()
{

	vector<string> files;
	
	listFolder(data_path_train, &files, true);
	loadFile(&files, &data_train);

	listFolder(data_path_test, &files, true);
	loadFile(&files, &data_train);
}

void machineLearning::loadModel()
{
	if (cnn.read(data_path_model + "model"))
	{
		#ifdef PRINT_DETAIL
		std::cout << "Mojo CNN Configuration:" << std::endl;
		std::cout << cnn.get_configuration() << std::endl << std::endl;
		#endif
	}
}

void machineLearning::listFolder(string folderPath, _Out_ vector<string> *fileList, bool clearList)
{
	_finddata_t fileDescripter;
	long long handle;

	handle = _findfirst(folderPath.c_str(), &fileDescripter);
	if (handle < 0) return; // fail

	if (clearList) fileList->clear();

	do
	{
		fileList->push_back(fileDescripter.name);

	} while (_findnext(handle, &fileDescripter) == 0);

	_findclose(handle);
}

void machineLearning::loadFile(_In_ vector<string> *list, _Out_ vector<DATA> *datas)
{
	string timelog;
	int label;
	int frameSize;
	int valueSize;
	int channelSize;
	double temp;

	for (int i = 0; i < list->size(); ++i)
	{
		ifstream is(list->at(i).c_str(), std::ios::in | std::ios::binary);

		while (is.good())
		{
			is >> timelog >> label >> frameSize >> valueSize >> channelSize;
			FAIL_STOP(channelSize != 1, "muilty channel is not ready");

			datas->push_back(DATA());
			datas->back().second = label;

			for (int i = 0; i < frameSize; ++i)
				for (int j = 0; j < valueSize; ++j)
					for (int k = 0; k < channelSize; ++k)
					{
						is >> temp;
						datas->back().first.push_back((float)temp);
					}


			while (is.peek() == '\n' || is.peek() == '\r')
			{
				is.get();
			}
		}
	}
}

void machineLearning::train()
{

	#ifdef PRINT_DETAIL
		std::cout << "==  Network Configuration  ====================================================" << std::endl;
		std::cout << cnn.get_configuration() << std::endl;
	#endif

	// setup timer/progress for overall training
	mojo::progress overall_progress(-1, "  overall:\t\t");
	overall_progress.draw_header("Epoch  " + std::to_string((long long)cnn.get_epoch() + 1), true);

	float singleElapsedTime = 0;

	while (1)
	{
		train_single_epoch(singleElapsedTime);

		// accurity
		float train_accuracy = test(data_train);
		float accuracy = test(data_test);

		std::string model_file = data_path_snapshot + "tmp_" + std::to_string((long long)cnn.get_epoch()) + ".txt";
		save(model_file);

		#ifdef PRINT_DETAIL
			cout << "  train accuracy:\t" << train_accuracy << "% (" << 100.f - train_accuracy << "% error)      " << std::endl;
			cout << "  test accuracy:\t" << accuracy << "% (" << 100.f - accuracy << "% error)      " << std::endl;
			cout << "  saved model:\t\t" << model_file << endl << endl;
		#else
			cout << cnn.get_epoch() << " - " << train_accuracy << " " << accuracy << endl;
		#endif

		#ifdef WRITE_LOG
			string log_out;
			log_out += float2str(singleElapsedTime) + "\t";
			log_out += float2str(overall_progress.elapsed_seconds()) + "\t";
			log_out += float2str(cnn.get_learning_rate()) + "\t";
			log_out += model_file;
			log.add_table_row(cnn.estimated_accuracy, accuracy, log_out);
			log.write(data_path_snapshot + "log.htm");
		#endif

		// can't seem to improve
		if (cnn.elvis_left_the_building())
		{
			std::cout << "Elvis just left the building. No further improvement in training found." << endl;
			std::cout << "Stopping.." << std::endl;
			break;
		}
	}
}

void machineLearning::train_single_epoch(_Out_ float &time)
{
	// setup timer / progress for this one epoch
	mojo::progress progress((int)data_train.size(), "  training:\t\t");

	cnn.start_epoch("cross_entropy"); // Currently supported are "mse" and "cross_entropy".

	#pragma omp parallel for schedule(dynamic)
	for (int k = 0; k<data_train.size(); k++)
	{
		cnn.train_class(data_train[k].first.data(), data_train[k].second);
		if (k % 100 == 0) progress.draw_progress(k);
	}

	cnn.end_epoch();

	//cnn.set_learning_rate(0.5f*cnn.get_learning_rate());

	float dt = progress.elapsed_seconds();

	#ifdef PRINT_DETAIL
		std::cout << "  training time:\t" << dt << " seconds on " << cnn.get_thread_count() << " threads" << std::endl;
		std::cout << "  mini batch:\t\t" << mini_batch_size << "                               " << std::endl;
		std::cout << "  model updates:\t" << cnn.train_updates << " (" << (int)(100.f*(1. - (float)cnn.train_skipped / cnn.train_samples)) << "% of records)" << std::endl;
		std::cout << "  estimated accuracy:\t" << cnn.estimated_accuracy << "%" << std::endl;
	#endif

}

float machineLearning::test(_In_ vector<DATA> &data)
{
	int out_size = cnn.out_size();
	int correct_predictions = 0;
	float accuracy = -1;

	// use progress object for simple timing and status updating
	mojo::progress progress((int)data.size(), "  testing : ");

	const int record_cnt = (int)data.size();

	// when MOJO_OMP is defined, we use standard "omp parallel for" loop, 
	// the number of threads determined by network.enable_external_threads() call
	// dynamic schedule just helps the progress class to work correcly
	#pragma omp parallel for reduction(+:correct_predictions) schedule(dynamic)
	for (int k = 0; k<record_cnt; k++)
	{
		// predict_class returnes the output index of the highest response
		const int prediction = cnn.predict_class(data[k].first.data());
		if (prediction == data[k].second) correct_predictions++;
		if (k % 100 == 0) progress.draw_progress(k);
	}

	accuracy = (float)correct_predictions / record_cnt * 100.f;

	#ifdef PRINT_DETAIL
		float dt = progress.elapsed_seconds();
		std::cout << "  test time: " << dt << " seconds" << std::endl;
		std::cout << "  records: " << data.size() << std::endl;
		std::cout << "  speed: " << (float)record_cnt / dt << " records/second" << std::endl;
		std::cout << "  accuracy: " << accuracy << "%" << std::endl;
	#endif

	return accuracy;
}

void machineLearning::save()
{
	string ag = data_path_model;
	save(ag);
}

void machineLearning::save(_In_ string & fn)
{
	cnn.write(fn, false, false);
}

/*

int main()
{
	// == parse data
	// array to hold image data (note that mojo does not require use of std::vector)
	std::vector<std::vector<float>> test_images;
	// array to hold image labels 
	std::vector<int> test_labels;
	// calls MNIST::parse_test_data  or  CIFAR10::parse_test_data depending on 'using'
	if (!parse_test_data(data_path, test_images, test_labels)) { std::cerr << "error: could not parse data.\n"; return 1; }

	// == setup the network  
	mojo::network cnn;

	// here we need to prepare mojo cnn to store data from multiple threads
	// !! enable_external_threads must be set prior to loading or creating a model !!
	cnn.enable_external_threads();

	// load model
	if (!cnn.read(model_file)) { std::cerr << "error: could not read model.\n"; return 1; }
	std::cout << "Mojo CNN Configuration:" << std::endl;
	std::cout << cnn.get_configuration() << std::endl << std::endl;

	// == run the test
	std::cout << "Testing " << data_name() << ":" << std::endl;
	// this function will loop through all images, call predict, and print out stats
	test(cnn, test_images, test_labels);

	std::cout << std::endl;
	return 0;
}
*/