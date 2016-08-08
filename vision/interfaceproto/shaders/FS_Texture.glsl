/**
    FS_Texture.glsl

    @version    0.1
    @author     Miika 'LehdaRi' Lehtimäki
    @date       2015-04-18
**/


#version 330 core


#define PI 3.14159265359


in vec2 UV;

out vec4 color;

uniform sampler2D camTex1;
uniform sampler2D camTex2;
uniform sampler2D depthTex;
uniform sampler2D colorTex;

const float dx = 1.0/512.0;
const float dy = 1.0/424.0;

const float sx = 1.0/0.68;

void main() {
    color = vec4(0.0, 0.0, 0.0, 1.0);
	
    if (UV.y < 0.5) {
		if (UV.x < 0.5)
			color = vec4(texture(camTex1, vec2(UV.x*2, UV.y*2)).rgb, 1.0);
		else
			color = vec4(texture(camTex2, vec2(UV.x*2-1, UV.y*2)).rgb, 1.0);
    }
	else {
		if (UV.x < 0.5)
			color = vec4(texture(colorTex, vec2(1-UV.x*2, UV.y*2-1)).rgb, 1.0);
		else {
			float c = 0.0f;
			for (int x=-1; x<2; ++x) {
				for (int y=-1; y<2; ++y) {
					c = max(c, texture(depthTex, vec2(0.5-sx*(2*UV.x-1.5) + x*dx, 2*UV.y-1 + y*dy)).r);
				}
			}
			c *= 12;
			color = vec4(c, c, c, 0.0);
		}
	}
}
