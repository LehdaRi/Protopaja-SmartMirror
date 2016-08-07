#pragma once


#include <thread>
#include <new>

#include "Device.h"

#include "CNNTrainer.h"	//	TEMP


extern "C" {	//	primary DLL interface

	typedef void* VISION_HANDLE;

	//	returns pointer to Vision object
	VISION_HANDLE VISION_API launchVision(bool useCams, bool useWindow);

	//	terminates given Vision object
	void VISION_API terminateVision(VISION_HANDLE vision);

	//	polls event and modifies given event object
	//	returns true if new event was found, false otherwise
	bool VISION_API pollEvent(VISION_HANDLE vision, Event* event);

	//	start face capturing for database entries
	void VISION_API	startFaceCapture(VISION_HANDLE vision);

	//	stop face capturing
	void VISION_API stopFaceCapture(VISION_HANDLE vision);

	//	set active face to be captured
	//	1-5: faces to be recognized
	//	0 or >5: someone not to be recognized
	void VISION_API setActiveFace(VISION_HANDLE vision, int activeFace);

	//	reset existing database, call this when you want to
	//	re-train the vision network
	void VISION_API	resetDatabase(VISION_HANDLE vision);

	//	train neural network with captured face database,
	//	will replace the old one
	void VISION_API	trainNetwork(VISION_HANDLE vision);

}

namespace Vision
{

	class Vision {
	public:
		Vision(bool useCams, bool useWindow);
		~Vision(void);

		bool pollEvent(Event* event);

		void startFaceCapture(void);
		void stopFaceCapture(void);
		void setActiveFace(int activeFace);

		void resetDatabase(void);
		void trainNetwork(void);

	private:
		Device		_device;
		std::thread	_mainThread;
	};

}