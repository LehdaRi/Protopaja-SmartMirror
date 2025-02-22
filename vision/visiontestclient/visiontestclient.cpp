// visiontestclient.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "vision.h"

#include <chrono>
#include <thread>


int main()
{
	using namespace std::chrono_literals;

	VISION_HANDLE vision = launchVision(true, false);

	//trainNetwork(vision);

	Event* event = new Event;
	for (bool running = true; running;) {
		while (pollEvent(vision, event)) {
			printf("Polled event with type = %u and data = %u\n", event->type, event->data);
			if (event->type == 10)
				running = false;
		}

		std::this_thread::sleep_for(100ms);
	}

	terminateVision(vision);
}

