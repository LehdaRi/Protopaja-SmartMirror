#pragma once


#include "FaceCNN.h"


namespace Vision {
	
	class CNNDataBase;

	class CNNTrainer {
	public:
		CNNTrainer(CNNDataBase& dataBase);

		void train(void);
		void test(void);


	
	private:
		CNNDataBase&					_dataBase;
		FaceCNN							_network;

		std::vector<tiny_cnn::vec_t>	_images;
		std::vector<tiny_cnn::vec_t>	_labels;
		
		void loadDataSet(uint64_t startId, uint64_t endId);
	};

}