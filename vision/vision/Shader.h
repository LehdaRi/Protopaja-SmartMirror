#pragma once


#include <string>
#include <GL/glew.h>


namespace Vision {

	class Shader {
	public:
		Shader(const std::string& vsFileName, const std::string& fsFileName);
		~Shader(void);

		Shader(const Shader&) = delete;
		Shader(Shader&&) = delete;
		Shader& operator=(const Shader&) = delete;
		Shader& operator=(Shader&&) = delete;

		GLuint getId(void) const;
		void use(void);

	private:
		GLuint programId_;
		GLuint uniformPosition_MVP_;
		GLuint uniformPosition_Color_;
	};

}