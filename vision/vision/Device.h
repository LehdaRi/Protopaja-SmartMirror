#pragma once


#include "Cam.h"
#include "Shader.h"
#include "Texture.h"
#include "Kinect.h"
#include "Event.h"
#include "FaceRecognizer.h"

#include <memory>
#include <atomic>
#include <mutex>
#include <deque>
#include <thread>


#define QUAD(xPos, yPos, xSize, ySize) xPos, yPos, 0.0f,\
                                       xPos+xSize, yPos, 0.0f,\
                                       xPos, yPos+ySize, 0.0f,\
                                       xPos, yPos+ySize, 0.0f,\
                                       xPos+xSize, yPos, 0.0f,\
                                       xPos+xSize, yPos+ySize, 0.0f

extern "C" {

	struct Event;

}


namespace Vision {

	class Device {
	private:
		struct Env {
			std::unique_ptr<Kinect>			kinect;
			std::unique_ptr<FaceRecognizer>	kinectFaceRecognizer;

			bool usingCams;
			std::unique_ptr<Cam>			cam1;
			std::unique_ptr<Cam>			cam2;
			std::unique_ptr<FaceRecognizer>	camFaceRecognizer1;
			std::unique_ptr<FaceRecognizer>	camFaceRecognizer2;

			bool usingWindow;
			std::unique_ptr<Shader>		shader;
			std::unique_ptr<Texture>	depthTexture;
			std::unique_ptr<Texture>	colorTexture;
			std::unique_ptr<Texture>	camTexture1;
			std::unique_ptr<Texture>	camTexture2;

			GLuint		vertexArrayId;
			GLuint		vertexBufferId;

			Env(bool useCams, bool useWindow,
			    uint32_t camWidth	= 1920,
			    uint32_t camHeight	= 1080);
		};

	public:
		Device(void);

		int mainLoop(bool useCams = true, bool useWindow = true);
		void terminate(void);

		void draw(Env& env);

		bool pollEvent(Event& event);

		void updateShader(Env& env);

	private:
		//	status
		std::atomic<bool>	_terminating;
		
		//	threads for cams
		std::thread			_camThread1;
		std::thread			_camThread2;

		//	events
		std::deque<Event>	_eventQueue;
		std::mutex			_eventMutex;
		void addEvent(int type, int data);
	};

}