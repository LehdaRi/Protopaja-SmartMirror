#pragma once


#include "FaceCNN.h"

#include <opencv2/objdetect/objdetect.hpp>


namespace Vision {

	class FaceRecognizer {
	public:
		FaceRecognizer(double minFeatureSize = 100);

		void setMinFeatureSize(double minFeatureSize);

		void detectFaces(cv::Mat& frame);

	private:
		cv::Size				_minFeatureSize;

		cv::CascadeClassifier	_faceCascade;
		cv::Mat					_grayFrame;

		std::vector<cv::Rect>	_faceRects;
		std::vector<cv::Mat>	_faceMats;

		FaceCNN					_faceCNN;
	};

}