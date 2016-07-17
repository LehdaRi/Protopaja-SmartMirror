#include "stdafx.h"
#include "vision.h"

#include <SFML/Window.hpp>


using namespace Vision;


Device::Env::Env(bool useCams, bool useWindow) :
	usingWindow		(useWindow),
	shader			(useWindow ? new Shader("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl") : nullptr),
	camTexture1		(useWindow ? new Texture(1920, 1080) : nullptr),
	camTexture2		(useWindow ? new Texture(1920, 1080) : nullptr),
	depthTexture	(useWindow ? new Texture(512, 424) : nullptr),
	colorTexture	(useWindow ? new Texture(1920, 1080) : nullptr),
	vertexArrayId	(0),
	vertexBufferId	(0),
	usingCams		(useCams),
	cam1			(useCams ? new Cam(0, 1920, 1080, 30.0) : nullptr),
	cam2			(useCams ? new Cam(1, 1920, 1080, 30.0) : nullptr),
	kinect			(new Kinect())
{}

Device::Device(void) :
	_terminating(false)
{}

int Device::mainLoop(bool useCams, bool useWindow) {
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
	std::unique_ptr<Env> env(new Env(useCams, useWindow));

	if (useWindow) {
		//	init canvas
		const GLfloat quads[] = {
			QUAD(-1.0f, -1.0f, 2.0f, 2.0f)
		};

		glGenVertexArrays(1, &env->vertexArrayId);
		glBindVertexArray(env->vertexArrayId);

		glGenBuffers(1, &env->vertexBufferId);
		glBindBuffer(GL_ARRAY_BUFFER, env->vertexBufferId);
		glBufferData(GL_ARRAY_BUFFER, sizeof(quads), quads, GL_STATIC_DRAW);

		glEnableVertexAttribArray(0);
		glBindBuffer(GL_ARRAY_BUFFER, env->vertexBufferId);
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

		glBindVertexArray(0);
	}

	if (useCams) {
		_camThread1 = std::thread(&Cam::loop, env->cam1.get());
		_camThread2 = std::thread(&Cam::loop, env->cam2.get());
	}
	
	//	BEGIN OF TEMP
	/*int64_t loopCounter = 0;
	std::chrono::duration<double> loopTimeSum(0.0);
	std::chrono::duration<double> loopTimeMin(100000000.0);
	std::chrono::duration<double> loopTimeMax(0.0);*/
	//	END OF TEMP

	if (useWindow) {
		while (window->isOpen())
		{
			//	BEGIN OF TEMP
			/*std::chrono::time_point<std::chrono::system_clock> start, end;
			start = std::chrono::system_clock::now();
			*/
			//	END OF TEMP

			// Event processing
			sf::Event event;
			while (window->pollEvent(event))
			{
				// Request for closing the window
				if (event.type == sf::Event::Closed)
					addEvent(4, 0);
				else if (event.type == sf::Event::KeyPressed) {
					switch (event.key.code) {
					case sf::Keyboard::A:
						updateShader(*env);
						break;
					case sf::Keyboard::Q:
						addEvent(4, 0);
						break;
					case sf::Keyboard::W:
						addEvent(1, 0);
						break;
					case sf::Keyboard::E:
						addEvent(1, 1);
						break;
					case sf::Keyboard::R:
						addEvent(2, 0);
						break;
					case sf::Keyboard::T:
						addEvent(2, 1);
						break;
					case sf::Keyboard::Y:
						addEvent(3, 0);
						break;
					case sf::Keyboard::U:
						addEvent(3, 1);
						break;
					}
				}
			}

			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
			
			(*env->kinect)(env->depthTexture.get(), env->colorTexture.get());

			env->cam1->detectFaces(_faceRecognizer);
			env->cam2->detectFaces(_faceRecognizer);

			draw(*env);

			if (env->usingCams) {
				env->cam1->read();
				env->cam2->read();
			}
			
			window->display();

			if (_terminating) {
				if (useCams) {
					env->cam1->terminate();
					env->cam2->terminate();
					_camThread1.join();
					_camThread2.join();
					printf("Cam threads joined\n");
				}
				window->close();
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
	}
	else {

	}

	return 0;
}

void Device::terminate(void) {
	_terminating = true;
}

void Device::draw(Env& env) {
	//	update textures
	if (env.usingCams) {
		env.cam1->writeToTexture(*env.camTexture1);
		env.cam2->writeToTexture(*env.camTexture2);
	}

	env.shader->use();

	glBindVertexArray(env.vertexArrayId);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, (GLuint)*env.camTexture1);
	glUniform1i(glGetUniformLocation(env.shader->getId(), "camTex1"), 0);
	glActiveTexture(GL_TEXTURE1);
	glBindTexture(GL_TEXTURE_2D, (GLuint)*env.camTexture2);
	glUniform1i(glGetUniformLocation(env.shader->getId(), "camTex2"), 1);
	glActiveTexture(GL_TEXTURE2);
	glBindTexture(GL_TEXTURE_2D, (GLuint)*env.depthTexture);
	glUniform1i(glGetUniformLocation(env.shader->getId(), "depthTex"), 2);
	glActiveTexture(GL_TEXTURE3);
	glBindTexture(GL_TEXTURE_2D, (GLuint)*env.colorTexture);
	glUniform1i(glGetUniformLocation(env.shader->getId(), "colorTex"), 3);
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

void Device::updateShader(Env& env) {
	env.shader.reset(new Shader("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl"));
}

void Device::addEvent(int type, int data) {
	std::lock_guard<std::mutex> lock(_eventMutex);
	_eventQueue.emplace_back(Event{ type, data });
}