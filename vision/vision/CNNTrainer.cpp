#include "stdafx.h"
#include "CNNTrainer.h"
#include "CNNDataBase.h"

#include <SFML/Graphics.hpp>
#include <sstream>


using namespace Vision;
using namespace tiny_cnn;
using namespace tiny_cnn::layers;
using namespace tiny_cnn::activation;


CNNTrainer::CNNTrainer(CNNDataBase& dataBase) :
	_dataBase(dataBase)
{}

void CNNTrainer::train(void) {
	loadDataSet(0, 3);

	adam optimizer;

	const int nMinibatches = 8;
	const int nEpochs = 6;
	const double learning_rate = 0.05f;// 0.03f;

	auto on_enumerate_minibatch = [&]() {};

	auto on_enumerate_epoch = [&]() {
		static uint32_t epochId = 0;
		printf("Training epoch %u/%u\n", epochId++, nEpochs);
	};

	optimizer.alpha *= static_cast<tiny_cnn::float_t>(sqrt(nMinibatches) * learning_rate);
	_network._network.fit<mse>(optimizer, _images, _labels, nMinibatches, nEpochs,
	                  on_enumerate_minibatch, on_enumerate_epoch);

	printf("Training complete\n");
	std::ofstream ofs("res/cnn/faces.cnn");
	ofs << _network._network;

	printf("Network saved to res/cnn/faces.cnn\n");
}

void CNNTrainer::test(void) {
	/*printf("Loading network from res/cnn/faces.cnn\n");
	std::ifstream ifs("res/cnn/faces.cnn");
	if (ifs.is_open()) {
		ifs >> _network._network;
		printf("Network loaded\n");
	}*/

	_network = FaceCNN("res/cnn/faces.cnn");

	loadDataSet(0, 1);

	std::default_random_engine r(715517);
	for (auto i = 0u; i < 40; ++i) {
		uint64_t id = r() % _images.size();
		auto& img = _images[id];
		auto& label = _labels[id];

		auto prediction = _network._network.predict(img);
		printf("Correct label: %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, prediction: %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f ",
			label[0], label[1], label[2], label[3], label[4], label[5],
			prediction[0], prediction[1], prediction[2], prediction[3], prediction[4], prediction[5]);
		
		int maxIdLabel = 0;
		int maxIdPrediction = 0;
		for (auto j = 0u; j < 6; ++j) {
			if (label[j] > label[maxIdLabel])
				maxIdLabel = j;
			if (prediction[j] > prediction[maxIdPrediction])
				maxIdPrediction = j;
		}
		printf("%s\n", maxIdLabel == maxIdPrediction ? "correct" : "incorrect");
	}

}

void CNNTrainer::loadDataSet(uint64_t startId, uint64_t endId) {
	static std::default_random_engine r(71551);

	uint64_t nImages = 0;
	for (auto j = 0; j < 6; ++j) {
		int n = (std::min(_dataBase._dataBase.at(j).size(), endId) - startId);
		nImages += n < 0 ? 0 : n;
	}
	nImages *= 256;

	_images.clear();
	_labels.clear();
	_images.resize(nImages, vec_t(64 * 64 * 3));
	_labels.resize(nImages, vec_t(6));

	std::vector<bool> used(nImages, false);
	uint64_t nUsed = 0;

	for (auto j = 0; j < 6; ++j) {
		auto dbv = _dataBase._dataBase.at(j);

		vec_t label = { j == 0 ? 1.0f : 0.0f,
			j == 1 ? 1.0f : 0.0f,
			j == 2 ? 1.0f : 0.0f,
			j == 3 ? 1.0f : 0.0f,
			j == 4 ? 1.0f : 0.0f,
			j == 5 ? 1.0f : 0.0f };

		for (auto i = startId; i < std::min(dbv.size(), endId); ++i) {
			auto& img = dbv[i];
			
			for (auto iy = 0u; iy < 16; ++iy) {
				for (auto ix = 0u; ix < 16; ++ix) {
					uint64_t id = 0;
					if (nUsed < (used.size() / 8) * 7) {
						while (used[id])
							id = r() % used.size();
					}
					else
						while (used[id]) ++id;

					used[id] = true;
					++nUsed;

					auto& v = _images[id];

					for (auto y = 0u; y < 64; ++y) {
						for (auto x = 0u; x < 64; ++x) {
							auto& pix = img.getPixel(ix * 64 + x, iy * 64 + y);

							v[4096 * 0 + 64 * y + x] = pix.r / 255.0f;
							v[4096 * 1 + 64 * y + x] = pix.g / 255.0f;
							v[4096 * 2 + 64 * y + x] = pix.b / 255.0f;
						}
					}
					_labels[id] = label;
				}
			}
		}
	}
}