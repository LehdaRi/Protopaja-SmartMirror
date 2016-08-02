#include "stdafx.h"
#include "FaceCNN.h"
#include <SFML/Graphics.hpp>


using namespace Vision;
using namespace tiny_cnn;
using namespace tiny_cnn::layers;
using namespace tiny_cnn::activation;


FaceCNN::FaceCNN(const std::string& fileName) :
	_input(64*64*3)
{
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

	std::ifstream ifs(fileName);
	if (ifs.is_open()) {
		ifs >> _network;
		printf("Network loaded\n");
	}
}

vec_t FaceCNN::operator()(cv::Mat& input) {
	uchar* p;
	for (auto y = 0u; y < 64; ++y) {
		p = input.ptr<uchar>(y);
		for (auto x = 0u; x < 64; ++x) {

			_input[4096 * 0 + 64 * y + x] = p[x * 3 + 2] / 255.0f;
			_input[4096 * 1 + 64 * y + x] = p[x * 3 + 1] / 255.0f;
			_input[4096 * 2 + 64 * y + x] = p[x * 3 + 0] / 255.0f;

			//img.setPixel(x, y, sf::Color(p[x * 3 + 2], p[x * 3 + 1], p[x * 3 + 0]));
		}
	}

	//img.saveToFile("res/debug.png");

	return _network.predict(_input);
}