#pragma once


#include <thread>

#include "Device.h"


#ifdef NDEBUG
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif


namespace Vision
{

	class VISION_API Vision {
	public:
		Vision(void);
		~Vision(void);

		//	returns true if new event was found, false otherwise
		bool pollEvent(Event* event);

	private:
		Device		_device;
		std::thread	_mainThread;
	};
}