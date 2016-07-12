// visiontestclient.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "vision.h"

#include <chrono>
#include <thread>


int main()
{
	using namespace std::chrono_literals;

	Vision::Vision vision;

	Vision::Event event;
	for (bool running = true; running;) {
		while (vision.pollEvent(&event)) {
			printf("Polled event with type = %u and data = %u\n", event.type, event.data);
			if (event.type == 4)
				running = false;
		}

		std::this_thread::sleep_for(1s);
	}
}

