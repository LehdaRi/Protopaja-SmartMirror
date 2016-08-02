#pragma once


#include <tiny_cnn.h>


namespace Vision {
	
	class CNNTrainer {
	public:
		CNNTrainer(void);

		void loadDataSet(uint64_t startId, uint64_t endId);

		void train(void);
		void test(void);
	
	private:
		tiny_cnn::network<tiny_cnn::sequential>	_network;

		std::vector<tiny_cnn::vec_t>			_images;
		std::vector<tiny_cnn::vec_t>			_labels;
	};

}