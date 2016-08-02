#include "stdafx.h"
#include "CNNTrainer.h"

#include <SFML/Graphics.hpp>
#include <sstream>


using namespace Vision;
using namespace tiny_cnn;
using namespace tiny_cnn::layers;
using namespace tiny_cnn::activation;


namespace {
	
	inline void copyImages(std::vector<vec_t>& images,
	                       std::vector<vec_t>& labels,
	                       std::vector<bool>& used,
	                       uint64_t& nUsed,
	                       sf::Image& img, const vec_t& label) {
		static std::default_random_engine r(71551);


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

				auto& v = images[id];

				for (auto y = 0u; y < 64; ++y) {
					for (auto x = 0u; x < 64; ++x) {
						auto& pix = img.getPixel(ix * 64 + x, iy * 64 + y);

						v[4096 * 0 + 64 * y + x] = pix.r / 255.0f;
						v[4096 * 1 + 64 * y + x] = pix.g / 255.0f;
						v[4096 * 2 + 64 * y + x] = pix.b / 255.0f;
					}
				}
				labels[id] = label;
			}
		}
	}

	inline void parseFaceDataSet(std::vector<vec_t>& images, std::vector<vec_t>& labels, uint64_t startId, uint64_t endId) {
		const uint64_t nImages = 256 * 5 * (endId - startId);
		images.clear();
		labels.clear();
		images.resize(nImages, vec_t(64*64*3));
		labels.resize(nImages, vec_t(5));

		std::vector<bool> used(nImages, false);
		uint64_t nUsed = 0;

		sf::Image img;

		for (auto i = startId; i < endId; ++i) {
			for (auto j = 0; j < 5; ++j) {
				std::stringstream ss;
				ss << "res/facedataset2/faces" << j << "_" << i << ".png";
				img.loadFromFile(ss.str());

				vec_t l = { j == 0 ? 1.0f : 0.0f,
							j == 1 ? 1.0f : 0.0f,
							j == 2 ? 1.0f : 0.0f,
							j == 3 ? 1.0f : 0.0f,
							j == 4 ? 1.0f : 0.0f };
				copyImages(images, labels, used, nUsed, img, l); \
			}
		}
	}

}


CNNTrainer::CNNTrainer(void) {
	printf("Creating network\n");

	typedef convolutional_layer<activation::identity> conv;
	typedef max_pooling_layer<relu> pool;

	const int n_fmaps = 32; ///< number of feature maps for upper layer
	const int n_fmaps2 = 64; ///< number of feature maps for lower layer
	const int n_fc = 256; ///< number of hidden units in fully-connected layer

	_network << conv(64, 64, 5, 3, n_fmaps, padding::same)
			 << pool(64, 64, n_fmaps, 2)
			 << conv(32, 32, 5, n_fmaps, n_fmaps, padding::same)
			 << pool(32, 32, n_fmaps, 2)
			 << conv(16, 16, 5, n_fmaps, n_fmaps2, padding::same)
			 << pool(16, 16, n_fmaps2, 2)
			 << fully_connected_layer<activation::identity>(8 * 8 * n_fmaps2, n_fc)
			 << fully_connected_layer<softmax>(n_fc, 5);
}

void CNNTrainer::loadDataSet(uint64_t startId, uint64_t endId) {
	printf("Loading data set from id %llu to id %llu\n", startId, endId);
	parseFaceDataSet(_images, _labels, startId, endId);
	printf("Data set loaded\n");
}

void CNNTrainer::train(void) {
	loadDataSet(1, 5);

	adam optimizer;

	const int nMinibatches = 8;
	const int nEpochs = 5;
	const double learning_rate = 0.025f;

	auto on_enumerate_minibatch = [&]() {};

	auto on_enumerate_epoch = [&]() {
		static uint32_t epochId = 0;
		printf("Training epoch %u/%u\n", epochId++, nEpochs);
	};

	optimizer.alpha *= static_cast<tiny_cnn::float_t>(sqrt(nMinibatches) * learning_rate);
	_network.fit<mse>(optimizer, _images, _labels, nMinibatches, nEpochs,
	                  on_enumerate_minibatch, on_enumerate_epoch);

	printf("Training complete\n");
	std::ofstream ofs("res/cnn/faces.cnn");
	ofs << _network;

	printf("Network saved to res/cnn/faces.cnn\n");
}

void CNNTrainer::test(void) {
	printf("Loading network from res/cnn/faces.cnn\n");
	std::ifstream ifs("res/cnn/faces.cnn");
	if (ifs.is_open()) {
		ifs >> _network;
		printf("Network loaded\n");
	}

	loadDataSet(0, 1);

	std::default_random_engine r(715517);
	for (auto i = 0u; i < 40; ++i) {
		uint64_t id = r() % _images.size();
		auto& img = _images[id];
		auto& label = _labels[id];

		auto prediction = _network.predict(img);
		printf("Correct label: %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, prediction: %0.2f, %0.2f, %0.2f, %0.2f, %0.2f ",
			label[0], label[1], label[2], label[3], label[4], prediction[0], prediction[1], prediction[2], prediction[3], prediction[4]);
		
		int maxIdLabel = 0;
		int maxIdPrediction = 0;
		for (auto j = 0u; j < 5; ++j) {
			if (label[j] > label[maxIdLabel])
				maxIdLabel = j;
			if (prediction[j] > prediction[maxIdPrediction])
				maxIdPrediction = j;
		}
		printf("%s\n", maxIdLabel == maxIdPrediction ? "correct" : "incorrect");
	}

	/*float correctness = 0.0f;
	for (auto i = 0u; i < 1000; ++i) {
		uint64_t id = r() % _images.size();
		auto& img = _images[id];
		auto& label = _labels[id];

		auto prediction = _network.predict(img);

		if ((label[0] < label[1]) == (prediction[0] < prediction[1]))
			correctness += 0.1f;
	}
	printf("correctness: %0.2f%%\n", correctness);*/
}