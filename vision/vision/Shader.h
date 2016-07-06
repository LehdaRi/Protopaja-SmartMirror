#pragma once


#include <string>
#include <GL/glew.h>


namespace Vision {

	class Shader {
	public:
		Shader(const std::string& vsFileName, const std::string& fsFileName);
		~Shader(void);

		Shader(const Shader&) = delete;
		Shader(Shader&&);
		Shader& operator=(const Shader&) = delete;
		Shader& operator=(Shader&&);

		GLuint getId(void) const;
		void use(void);

	private:
		GLuint programId_;
	};

}