#pragma once


#include <thread>
#include <new>

#include "Device.h"


namespace Vision
{

	class Vision {
	public:
		Vision(bool useCams, bool useWindow);
		~Vision(void);

		//	returns true if new event was found, false otherwise
		bool pollEvent(Event* event);

	private:
		Device		_device;
		std::thread	_mainThread;
	};

}

extern "C" {

	typedef void* VISION_HANDLE;

	//	returns pointer to Vision object
	VISION_HANDLE VISION_API launchVision(bool useCams, bool useWindow);

	//	terminates given Vision object
	void VISION_API terminateVision(VISION_HANDLE vision);

	//	polls event and modifies given event object
	bool VISION_API pollEvent(VISION_HANDLE vision, Event* event);
}