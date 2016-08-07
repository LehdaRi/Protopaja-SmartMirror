#pragma once


#include "Cam.h"
#include "Shader.h"
#include "Texture.h"
#include "Kinect.h"
#include "Event.h"
#include "FaceRecognizer.h"
#include "CNNDataBase.h"
#include "CNNTrainer.h"

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

		void draw(void);

		bool pollEvent(Event& event);

		void startFaceCapture(void);
		void stopFaceCapture(void);
		void setActiveFace(int activeFace);

		void resetDatabase(void);
		void trainNetwork(void);

		void updateShader(Env& env);

		void addEvent(int type, int data);

	private:
		//	load config file
		void loadConfigurationFile(void);

		struct ConfigData {
			int64_t	noCamsFaceDetectionBufferSize;
			int64_t	camsFaceDetectionBufferSize;
			double	faceDetectionLowerThreshold;
			double	faceDetectionUpperThreshold;
			double	knownFacesCompensationFactor;
			int64_t	maxEventInterval;
		} _configData;

		//	status
		std::atomic<bool>		_terminating;
		std::atomic<bool>		_training;

		//	environment
		std::unique_ptr<Env>	_env;
		std::mutex				_initializationMutex;
		
		//	threads for cams
		std::thread				_camThread1;
		std::thread				_camThread2;

		//	events
		std::deque<Event>		_eventQueue;
		std::mutex				_eventMutex;

		//	database
		CNNDataBase				_dataBase;

		//	network trainer
		CNNTrainer				_trainer;

		//	face data
		struct FaceData {
			uint64_t	nFaces;
			uint64_t	faceId;
		};
		std::deque<FaceData>	_faceHistory;
		uint64_t				_maxFaceHistorySize;
		FaceData				_status;
		uint64_t				_eventIntervalCounter;
		inline FaceData faceHistoryFilter(void);
	};

}