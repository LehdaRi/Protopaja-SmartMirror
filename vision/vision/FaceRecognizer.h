#pragma once


#include "FaceCNN.h"

#include <opencv2/objdetect/objdetect.hpp>


namespace Vision {

	class FaceRecognizer {
	public:
		FaceRecognizer(double minFeatureSize = 100, double captureDiffTreshold = 50.0);

		void setMinFeatureSize(double minFeatureSize);

		void detectFaces(cv::Mat& frame, uint64_t& nFaces, uint64_t& faceId);

		void startFaceCapture(void);
		void stopFaceCapture(void);
		bool newFaceCaptured(void);
		cv::Mat& lastCapturedFace(void);

	private:
		cv::Size				_minFeatureSize;

		cv::CascadeClassifier	_faceCascade;
		cv::Mat					_grayFrame;

		std::vector<cv::Rect>	_faceRects;
		std::vector<cv::Mat>	_faceMats;

		static FaceCNN			_faceCNN;

		bool					_faceCaptureActive;
		bool					_newFaceCaptured;
		double					_captureDiffThreshold;
		cv::Mat					_lastCapturedFace;

		inline double faceDiff(cv::Mat& newFrame);
	};

}