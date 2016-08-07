#include "stdafx.h"
#include "FaceRecognizer.h"

#include <opencv2/imgproc/imgproc.hpp>
#include <chrono>
#include <iostream>


using namespace Vision;


FaceCNN FaceRecognizer::_faceCNN("res/cnn/faces.cnn");


FaceRecognizer::FaceRecognizer(double minFeatureSize, double captureDiffTreshold) :
	_minFeatureSize			(minFeatureSize, minFeatureSize),
	_faceCaptureActive		(false),
	_newFaceCaptured		(false),
	_captureDiffThreshold	(captureDiffTreshold),
	_lastCapturedFace		(64, 64, CV_8UC3)
{
	if (!_faceCascade.load("cascades/haarcascade_frontalface_alt.xml"))
		fprintf(stderr, "Error loading \"cascades/haarcascade_frontalface_alt.xml\"\n");
}

void FaceRecognizer::setMinFeatureSize(double minFeatureSize) {
	_minFeatureSize = cv::Size(minFeatureSize, minFeatureSize);
	printf("minFeatureSize: %0.2f", minFeatureSize);
}

void FaceRecognizer::detectFaces(cv::Mat& frame, uint64_t& nFaces, uint64_t& faceId) {
	if (frame.empty()) {
		printf("Frame empty");
		return;
	}

	cv::cvtColor(frame, _grayFrame, CV_BGR2GRAY);
	cv::equalizeHist(_grayFrame, _grayFrame);

	//	BEGIN OF TEMP
	/*std::chrono::time_point<std::chrono::system_clock> start, end;
	start = std::chrono::system_clock::now();
	*///	END OF TEMP

	//	Detect faces
	_faceCascade.detectMultiScale(frame, _faceRects, 1.1, 6, 0 | CV_HAAR_SCALE_IMAGE, _minFeatureSize);
	
	nFaces = _faceRects.size();
	if (_faceMats.size() < _faceRects.size())
		_faceMats.resize(_faceRects.size(), cv::Mat(64, 64, CV_8UC3));

	for (auto i = 0u; i < _faceRects.size(); ++i) {
		cv::rectangle(frame, _faceRects[i], cv::Scalar(0, 0, 255), 3);
		cv::resize(frame(_faceRects[i]), _faceMats[i], cv::Size(64, 64));
	}

	faceId = 0;
	if (_faceRects.size() == 1) {

		if (_faceCaptureActive && faceDiff(_faceMats.at(0)) > _captureDiffThreshold) {
			_lastCapturedFace = _faceMats.at(0).clone();
			_newFaceCaptured = true;
		}
		
		auto& p = _faceCNN(_faceMats.at(0));

		//printf("%0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f\n", p[0], p[1], p[2], p[3], p[4], p[5]);
		
		for (auto i = 0u; i < 6; ++i)
			if (p[i] > p[faceId])
				faceId = i;
	}

	//	BEGIN OF TEMP
	/*
	printf("nFaces: %u\n", _faces.size());

	end = std::chrono::system_clock::now();
	std::chrono::duration<double> time = end - start;
	std::cout << "duration: " << time.count() << std::endl;
	*///	END OF TEMP

}

void Vision::FaceRecognizer::startFaceCapture(void) {
	_faceCaptureActive = true;
}

void Vision::FaceRecognizer::stopFaceCapture(void) {
	_faceCaptureActive = false;
}

bool Vision::FaceRecognizer::newFaceCaptured(void) {
	bool r = _newFaceCaptured;
	_newFaceCaptured = false;
	return r;
}

cv::Mat& FaceRecognizer::lastCapturedFace(void) {
	if (_faceMats.size() > 0)
		return _faceMats[0];
	else
		return cv::Mat(64, 64, CV_8UC3);
}

double FaceRecognizer::faceDiff(cv::Mat& newFrame) {
	double diff = 0.0;

	uchar *p1, *p2;
	for (auto y = 0u; y < 64; ++y) {
		p1 = _lastCapturedFace.ptr<uchar>(y);
		p2 = newFrame.ptr<uchar>(y);
		for (auto x = 0u; x < 64; ++x) {
			diff += abs(p1[x * 3 + 0] - p2[x * 3 + 0]);
			diff += abs(p1[x * 3 + 1] - p2[x * 3 + 1]);
			diff += abs(p1[x * 3 + 2] - p2[x * 3 + 2]);
		}
	}

	diff *= 0.000244140625; //	divided by 64*64

	return diff;
}