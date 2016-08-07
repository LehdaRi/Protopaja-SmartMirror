#include "stdafx.h"
#include "vision.h"

#include <SFML/Window.hpp>


using namespace Vision;





Device::Env::Env(bool useCams, bool useWindow, uint32_t camWidth, uint32_t camHeight) :
	kinect					(new Kinect()),
	kinectFaceRecognizer	(new FaceRecognizer(1080 * VISION_DEVICE_MINFEATURESIZESCALE)),

	usingCams				(useCams),
	cam1					(useCams ? new Cam(0, camWidth, camHeight, 30.0) : nullptr),
	cam2					(useCams ? new Cam(1, camWidth, camHeight, 30.0) : nullptr),
	camFaceRecognizer1		(useCams ? new FaceRecognizer(cam1->height() * VISION_DEVICE_MINFEATURESIZESCALE) : nullptr),
	camFaceRecognizer2		(useCams ? new FaceRecognizer(cam2->height() * VISION_DEVICE_MINFEATURESIZESCALE) : nullptr),
	
	usingWindow				(useWindow),
	shader					(useWindow ? new Shader("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl") : nullptr),
	depthTexture			(useWindow ? new Texture(512, 424) : nullptr),
	colorTexture			(useWindow ? new Texture(1920, 1080) : nullptr),
	camTexture1				(useWindow && useCams ? new Texture(cam1->width(), cam1->height()) : nullptr),
	camTexture2				(useWindow && useCams ? new Texture(cam2->width(), cam2->height()) : nullptr),
	vertexArrayId			(0),
	vertexBufferId			(0)
{}

Device::Device(void) :
	_terminating			(false),
	_training				(false),
	_env					(nullptr),
	_dataBase				("res/facedatabase/"),
	_trainer				(_dataBase),
	_maxFaceHistorySize		(10),
	_status					{0, 0},
	_eventIntervalCounter	(0)
{
	loadConfigurationFile();
}

int Device::mainLoop(bool useCams, bool useWindow) {
	_initializationMutex.lock();
	std::unique_ptr<sf::Window> window(nullptr);
	
	if (useWindow) {
		//	init window
		window.reset(new sf::Window(sf::VideoMode(1440, 810), "Vision", sf::Style::Default,
			sf::ContextSettings{ 24, 8, 4, 3, 0 }));
		//window->setFramerateLimit(60);
		window->setActive();

		//	init glew
		if (glewInit() != GLEW_OK) {
			fprintf(stderr, "Unable to init GLEW");
			return -1;
		}
	}
	
	//	init enviroment
	_env.reset(new Env(useCams, useWindow, 1920, 1080));
	_initializationMutex.unlock();

	if (useWindow) {
		//	init canvas
		const GLfloat quads[] = {
			QUAD(-1.0f, -1.0f, 2.0f, 2.0f)
		};

		glGenVertexArrays(1, &_env->vertexArrayId);
		glBindVertexArray(_env->vertexArrayId);

		glGenBuffers(1, &_env->vertexBufferId);
		glBindBuffer(GL_ARRAY_BUFFER, _env->vertexBufferId);
		glBufferData(GL_ARRAY_BUFFER, sizeof(quads), quads, GL_STATIC_DRAW);

		glEnableVertexAttribArray(0);
		glBindBuffer(GL_ARRAY_BUFFER, _env->vertexBufferId);
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

		glBindVertexArray(0);
	}

	if (useCams) {
		_camThread1 = std::thread(&Cam::loop, _env->cam1.get());
		_camThread2 = std::thread(&Cam::loop, _env->cam2.get());
		_maxFaceHistorySize = _configData.camsFaceDetectionBufferSize;
	}
	else
		_maxFaceHistorySize = _configData.noCamsFaceDetectionBufferSize;
	
	//	BEGIN OF TEMP
	/*int64_t loopCounter = 0;
	std::chrono::duration<double> loopTimeSum(0.0);
	std::chrono::duration<double> loopTimeMin(100000000.0);
	std::chrono::duration<double> loopTimeMax(0.0);*/
	//	END OF TEMP

	FaceData faceData[3];

	while (true) {
		//	BEGIN OF TEMP
		/*std::chrono::time_point<std::chrono::system_clock> start, end;
		start = std::chrono::system_clock::now();*/
		//	END OF TEMP

		if (_training) {
			//_trainer.train();
			_trainer.test();
			_training = false;
		}

		if (useWindow) {
			// Event processing
			sf::Event event;
			while (window->pollEvent(event)) {
				// Request for closing the window
				if (event.type == sf::Event::Closed)
					addEvent(10, 0);
				else if (event.type == sf::Event::KeyPressed) {
					switch (event.key.code) {
					case sf::Keyboard::A:
						updateShader(*_env);
						break;
					case sf::Keyboard::Escape:
						addEvent(10, 0);
						break;
					}
				}
			}
		}

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
			
		(*_env->kinect)(_env->depthTexture.get());
		_env->kinect->detectFaces(*_env->kinectFaceRecognizer, faceData[0].nFaces, faceData[0].faceId);
		_faceHistory.push_back(faceData[0]);

		if (_env->kinectFaceRecognizer->newFaceCaptured())
			_dataBase.addEntry(_env->kinectFaceRecognizer->lastCapturedFace(), this, &Device::addEvent);

		if (useWindow)
			_env->kinect->writeColorToTexture(*_env->colorTexture);

		if (useCams) {
			_env->cam1->detectFaces(*_env->camFaceRecognizer1, faceData[1].nFaces, faceData[1].faceId);
			_env->cam2->detectFaces(*_env->camFaceRecognizer2, faceData[2].nFaces, faceData[2].faceId);

			_faceHistory.push_back(faceData[1]);
			_faceHistory.push_back(faceData[2]);

			if (_env->camFaceRecognizer1->newFaceCaptured())
				_dataBase.addEntry(_env->camFaceRecognizer1->lastCapturedFace(), this, &Device::addEvent);
			if (_env->camFaceRecognizer2->newFaceCaptured())
				_dataBase.addEntry(_env->camFaceRecognizer2->lastCapturedFace(), this, &Device::addEvent);
		}

		while (_faceHistory.size() > _maxFaceHistorySize)
			_faceHistory.pop_front();

		faceHistoryFilter();

		if (useWindow)
			draw();

		if (_env->usingCams) {
			_env->cam1->read();
			_env->cam2->read();
		}
		
		if (useWindow)
			window->display();

		if (_terminating) {
			if (useCams) {
				_env->cam1->terminate();
				_env->cam2->terminate();
				_camThread1.join();
				_camThread2.join();
				printf("Cam threads joined\n");
			}

			if (useWindow)
				window->close();

			break;
		}


		//	BEGIN OF TEMP
		/*end = std::chrono::system_clock::now();
		std::chrono::duration<double> time = end - start;
		loopTimeSum += time;
		if (time < loopTimeMin) loopTimeMin = time;
		if (time > loopTimeMax) loopTimeMax = time;

		if (++loopCounter > 30) {
			std::cout << "Cycle average: " << loopTimeSum.count()/loopCounter << "s, min: "
					    << loopTimeMin.count() << "s, max: " << loopTimeMax.count() << "s\n";
			loopTimeSum = std::chrono::duration<double>(0.0);
			loopTimeMin = std::chrono::duration<double>(100000000.0);
			loopTimeMax = std::chrono::duration<double>(0.0);
			loopCounter = 0;
		}*/
		//	END OF TEMP
	}

	_env.reset(nullptr);
	printf("Environment released\n");

	return 0;
}

void Device::terminate(void) {
	_terminating = true;
}

void Device::draw(void) {
	_env->shader->use();
	glBindVertexArray(_env->vertexArrayId);

	if (_env->usingCams) {
		_env->cam1->writeToTexture(*_env->camTexture1);
		_env->cam2->writeToTexture(*_env->camTexture2);

		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, (GLuint)*_env->camTexture1);
		glUniform1i(glGetUniformLocation(_env->shader->getId(), "camTex1"), 0);
		glActiveTexture(GL_TEXTURE1);
		glBindTexture(GL_TEXTURE_2D, (GLuint)*_env->camTexture2);
		glUniform1i(glGetUniformLocation(_env->shader->getId(), "camTex2"), 1);
	}

	glActiveTexture(GL_TEXTURE2);
	glBindTexture(GL_TEXTURE_2D, (GLuint)*_env->depthTexture);
	glUniform1i(glGetUniformLocation(_env->shader->getId(), "depthTex"), 2);
	glActiveTexture(GL_TEXTURE3);
	glBindTexture(GL_TEXTURE_2D, (GLuint)*_env->colorTexture);
	glUniform1i(glGetUniformLocation(_env->shader->getId(), "colorTex"), 3);
	glDrawArrays(GL_TRIANGLES, 0, 6);

	glBindVertexArray(0);
	glBindTexture(GL_TEXTURE_2D, 0);
}

bool Device::pollEvent(Event& event) {
	std::lock_guard<std::mutex> lock(_eventMutex);

	if (_eventQueue.size() == 0)
		return false;

	event = _eventQueue.front();
	_eventQueue.pop_front();
	return true;
}

void Device::startFaceCapture(void) {
	std::lock_guard<std::mutex> lock(_initializationMutex);
	if (_env->usingCams) {
		_env->camFaceRecognizer1->startFaceCapture();
		_env->camFaceRecognizer2->startFaceCapture();
	}
	_env->kinectFaceRecognizer->startFaceCapture();
}

void Device::stopFaceCapture(void) {
	std::lock_guard<std::mutex> lock(_initializationMutex);
	if (_env->usingCams) {
		_env->camFaceRecognizer1->stopFaceCapture();
		_env->camFaceRecognizer2->startFaceCapture();
	}
	_env->kinectFaceRecognizer->startFaceCapture();
}

void Device::setActiveFace(int activeFace) {
	_dataBase.setActiveFace(activeFace);
}

void Device::resetDatabase(void) {
	_dataBase.resetDataBase();
}

void Device::trainNetwork(void) {
	_training = true;
}

void Device::updateShader(Env& env) {
	env.shader.reset(new Shader("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl"));
}

void Device::addEvent(int type, int data) {
	std::lock_guard<std::mutex> lock(_eventMutex);
	_eventQueue.emplace_back(Event{ type, data });
}

void Device::loadConfigurationFile(void) {
	std::ifstream	file("facedetectionconfig.txt");

	if (!file.is_open())
		fprintf(stderr, "Cannot open configuration file facedetectionconfig.txt");

	std::string		str;
	double			n;
	uint64_t		paramId = 0;

	while (file >> str >> n) {
		switch (paramId++) {
			case 0:
				_configData.noCamsFaceDetectionBufferSize = (int64_t)n;
				break;
			case 1:
				_configData.camsFaceDetectionBufferSize = (int64_t)n;
				break;
			case 2:
				_configData.faceDetectionLowerThreshold = n;
				break;
			case 3:
				_configData.faceDetectionUpperThreshold = n;
				break;
			case 4:
				_configData.knownFacesCompensationFactor = n;
				break;
			case 5:
				_configData.maxEventInterval = (int64_t)n;
				break;
		}
	}
}

inline Device::FaceData Device::faceHistoryFilter(void) {
	FaceData data;

	double		nFaces = 0.0;
	double		faceIdHistogram[6]{0.0};
	uint64_t	histogramMax = 0;

	for (auto& entry : _faceHistory) {
		nFaces += entry.nFaces;
		faceIdHistogram[entry.faceId] += 1.0;
	}
	nFaces /= _maxFaceHistorySize;

	for (auto i = 1u; i < 6; ++i) {
		faceIdHistogram[i] *= _configData.knownFacesCompensationFactor;
	}

	for (auto i = 0u; i < 6; ++i) {
		if (faceIdHistogram[i] > faceIdHistogram[histogramMax])
			histogramMax = i;
	}
	
	if (_eventIntervalCounter++ > 30) {
		if (nFaces < _configData.faceDetectionLowerThreshold) {
			if (_status.nFaces != 0) {	//	person exited from in front of the mirror
				addEvent(2, _status.faceId);
			}
			_status.faceId = 0;
			_status.nFaces = 0;
		}
		else if (nFaces >= _configData.faceDetectionLowerThreshold &&
			nFaces < _configData.faceDetectionUpperThreshold) {
			if (_status.nFaces != 0) {	//	there was multiple persons in front of the mirror
				addEvent(2, _status.faceId);
				addEvent(1, histogramMax);
			}
			else if (_status.nFaces == 0)	//	there was no person previously
				addEvent(1, histogramMax);

			_status.nFaces = 1;
			_status.faceId = histogramMax;
		}
		else if (nFaces >= _configData.faceDetectionUpperThreshold) {
			if (_status.nFaces == 0) {
				addEvent(1, 0);
				_status.nFaces = 1;
				_status.faceId = 0;
			}
			else if (_status.nFaces == 1) {
				addEvent(2, _status.faceId);
				addEvent(1, 0);
				_status.nFaces = 1;
				_status.faceId = 0;
			}
		}
		_eventIntervalCounter = 0;
	}

	/*
	printf("nFaces: %0.2f\t	Histogram:\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\n", nFaces,
		faceIdHistogram[0], faceIdHistogram[1], faceIdHistogram[2],
		faceIdHistogram[3], faceIdHistogram[4], faceIdHistogram[5]);
	*/

	return data;
}
