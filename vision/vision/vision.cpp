// vision.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "vision.h"

#include <SFML/Window.hpp>
#include <iostream>


using namespace std;


extern "C" {

	VISION_HANDLE launchVision(bool useCams, bool useWindow) {
		return new(std::nothrow) Vision::Vision(useCams, useWindow);
	}

	void terminateVision(VISION_HANDLE vision) {
		delete (Vision::Vision*)vision;
	}

	bool pollEvent(VISION_HANDLE vision, Event* event) {
		try {
			Vision::Vision* v = reinterpret_cast<Vision::Vision*>(vision);
			return v->pollEvent(event);
		}
		catch (...) {
			return false;
		}
	}

	void startFaceCapture(VISION_HANDLE vision) {
		try {
			Vision::Vision* v = reinterpret_cast<Vision::Vision*>(vision);
			v->startFaceCapture();
		}
		catch (...) {
			fprintf(stderr, "Vision library error: invalid vision handle\n");
		}
	}

	void stopFaceCapture(VISION_HANDLE vision) {
		try {
			Vision::Vision* v = reinterpret_cast<Vision::Vision*>(vision);
			v->stopFaceCapture();
		}
		catch (...) {
			fprintf(stderr, "Vision library error: invalid vision handle\n");
		}
	}

	void setActiveFace(VISION_HANDLE vision, int activeFace) {
		try {
			Vision::Vision* v = reinterpret_cast<Vision::Vision*>(vision);
			v->setActiveFace(activeFace);
		}
		catch (...) {
			fprintf(stderr, "Vision library error: invalid vision handle\n");
		}
	}

	void resetDatabase(VISION_HANDLE vision) {
		try {
			Vision::Vision* v = reinterpret_cast<Vision::Vision*>(vision);
			v->resetDatabase();
		}
		catch (...) {
			fprintf(stderr, "Vision library error: invalid vision handle\n");
		}
	}

	void trainNetwork(VISION_HANDLE vision) {
		try {
			Vision::Vision* v = reinterpret_cast<Vision::Vision*>(vision);
			v->trainNetwork();
		}
		catch (...) {
			fprintf(stderr, "Vision library error: invalid vision handle\n");
		}
	}

}

Vision::Vision::Vision(bool useCams, bool useWindow) :
	_device			(),
	_mainThread		(&Device::mainLoop, &_device, useCams, useWindow)
{}

Vision::Vision::~Vision(void) {
	_device.terminate();
	_mainThread.join();
}

bool Vision::Vision::pollEvent(Event* event) {
	if (event) {
		return _device.pollEvent(*event);
	}
	return false;
}

void Vision::Vision::startFaceCapture(void) {
	_device.startFaceCapture();
}

void Vision::Vision::stopFaceCapture(void) {
	_device.stopFaceCapture();
}

void Vision::Vision::setActiveFace(int activeFace) {
	_device.setActiveFace(activeFace);
}

void Vision::Vision::resetDatabase(void) {
	_device.resetDatabase();
}

void Vision::Vision::trainNetwork(void) {
	_device.trainNetwork();
}