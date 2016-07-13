#pragma once


#include "Cam.h"
#include "Shader.h"
#include "Texture.h"
#include "Kinect.h"
#include "Event.h"

#include <atomic>
#include <mutex>
#include <deque>


#define QUAD(xPos, yPos, xSize, ySize) xPos, yPos, 0.0f,\
                                       xPos+xSize, yPos, 0.0f,\
                                       xPos, yPos+ySize, 0.0f,\
                                       xPos, yPos+ySize, 0.0f,\
                                       xPos+xSize, yPos, 0.0f,\
                                       xPos+xSize, yPos+ySize, 0.0f


namespace Vision {

	class Event;

	class Device {
	private:
		struct Env {
			Shader		shader;
			Texture		camTexture1;
			Texture		camTexture2;
			Texture		depthTexture;
			Texture		colorTexture;

			GLuint		vertexArrayId;
			GLuint		vertexBufferId;

			Cam			cam1;
			Cam			cam2;
			Kinect		kinect;

			Env(void);
		};

	public:
		Device(void);

		int mainLoop(bool useCams = true, bool useWindow = true);
		void terminate(void);

		void update(Env& env);
		void draw(Env& env);

		bool pollEvent(Event& event);

		void updateShader(Env& env);

	private:
		std::atomic<bool>	_terminating;

		std::deque<Event>	_eventQueue;
		std::mutex			_eventMutex;

		void addEvent(int type, int data);
	};

}