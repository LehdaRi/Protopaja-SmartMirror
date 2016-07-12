#include "stdafx.h"
#include "Device.h"

#include <SFML/Window.hpp>


using namespace Vision;


Device::Env::Env(void) :
	shader			("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl"),
	vertexArrayId	(0),
	vertexBufferId	(0),
	camTexture1		(1920, 1080),
	camTexture2		(1920, 1080),
	depthTexture	(512, 424),
	colorTexture	(1920, 1080),
	cam1			(0, 1920, 1080, 30.0),
	cam2			(1, 1920, 1080, 30.0)
{}

Device::Device(void) :
	_terminating(false)
{}

int Device::mainLoop(bool useWindow) {
	//	init window
	sf::Window window(sf::VideoMode(1440, 810), "Vision", sf::Style::Default,
	                  sf::ContextSettings{ 24, 8, 4, 3, 0 });
	window.setFramerateLimit(30);
	window.setActive();
	/*
	//	init glew
	if (glewInit() != GLEW_OK) {
		fprintf(stderr, "Unable to init GLEW");
		return -1;
	}

	//	init enviroment
	Env env;
	
	//	init canvas
	const GLfloat quads[] = {
		QUAD(-1.0f, -1.0f, 2.0f, 2.0f)
	};

	glGenVertexArrays(1, &env.vertexArrayId);
	glBindVertexArray(env.vertexArrayId);

	glGenBuffers(1, &env.vertexBufferId);
	glBindBuffer(GL_ARRAY_BUFFER, env.vertexBufferId);
	glBufferData(GL_ARRAY_BUFFER, sizeof(quads), quads, GL_STATIC_DRAW);

	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, env.vertexBufferId);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

	glBindVertexArray(0);
	*/

	while (window.isOpen())
	{
		// Event processing
		sf::Event event;
		while (window.pollEvent(event))
		{
			// Request for closing the window
			if (event.type == sf::Event::Closed)
				window.close();
			else if (event.type == sf::Event::KeyPressed) {
				switch (event.key.code) {
				case sf::Keyboard::A:
					//updateShader(env);
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

		//draw(env);

		window.display();

		if (_terminating)
			window.close();
	}

	return 0;
}

void Device::terminate(void) {
	_terminating = true;
}

bool Device::pollEvent(Event& event) {
	std::lock_guard<std::mutex> lock(_eventMutex);
	
	if (_eventQueue.size() == 0)
		return false;

	event = _eventQueue.front();
	_eventQueue.pop_front();
	return true;
}

void Device::draw(Env& env) {
	//	update textures
	env.cam1.read();
	env.cam2.read();

	env.camTexture1.updateFromCam(env.cam1);
	env.camTexture2.updateFromCam(env.cam2);

	env.shader.use();
	env.kinect(env.depthTexture, env.colorTexture);

	glBindVertexArray(env.vertexArrayId);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, (GLuint)env.camTexture1);
	glUniform1i(glGetUniformLocation(env.shader.getId(), "camTex1"), 0);
	glActiveTexture(GL_TEXTURE1);
	glBindTexture(GL_TEXTURE_2D, (GLuint)env.camTexture2);
	glUniform1i(glGetUniformLocation(env.shader.getId(), "camTex2"), 1);
	glActiveTexture(GL_TEXTURE2);
	glBindTexture(GL_TEXTURE_2D, (GLuint)env.depthTexture);
	glUniform1i(glGetUniformLocation(env.shader.getId(), "depthTex"), 2);
	glActiveTexture(GL_TEXTURE3);
	glBindTexture(GL_TEXTURE_2D, (GLuint)env.colorTexture);
	glUniform1i(glGetUniformLocation(env.shader.getId(), "colorTex"), 3);
	glDrawArrays(GL_TRIANGLES, 0, 6);

	glBindVertexArray(0);
	glBindTexture(GL_TEXTURE_2D, 0);
}

void Device::updateShader(Env& env) {
	env.shader = Shader("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl");
}

void Device::addEvent(int type, int data) {
	std::lock_guard<std::mutex> lock(_eventMutex);
	_eventQueue.emplace_back(Event{ type, data });
}