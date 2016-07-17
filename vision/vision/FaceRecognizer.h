#pragma once


#include <opencv2/objdetect/objdetect.hpp>


namespace Vision {

	class FaceRecognizer {
	public:
		FaceRecognizer(void);

		void detectFaces(cv::Mat& frame);

	private:
		cv::CascadeClassifier	_faceCascade;
		cv::Mat					_grayFrame;

		std::vector<cv::Rect>	_faces;
	};

}