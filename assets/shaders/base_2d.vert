#version 330 core 
layout (location = 0) in vec3 aPosition; 
layout (location = 1) in vec2 aTexCoords;

out vec2 TexCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main(void) { 
    gl_Position = model * vec4(aPosition, 1.0);
    TexCoords = aTexCoords;
}