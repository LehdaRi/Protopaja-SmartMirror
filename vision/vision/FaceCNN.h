#pragma once


#include <tiny_cnn.h>
#include <opencv2\opencv.hpp>


namespace Vision {

	class FaceCNN {
	public:
		FaceCNN(const std::string& fileName);

		tiny_cnn::vec_t operator()(cv::Mat& input);

	private:
		tiny_cnn::network<tiny_cnn::sequential>	_network;
		tiny_cnn::vec_t							_input;
	};

};