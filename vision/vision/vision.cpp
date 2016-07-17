// vision.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "vision.h"

#include <SFML/Window.hpp>
#include <iostream>


using namespace std;


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
			return -1;
		}
	}

}