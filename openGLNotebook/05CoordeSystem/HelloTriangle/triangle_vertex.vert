#version 330 core
layout (location = 0) in vec3 aPos;
//layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;
layout (location = 3) in vec2 aTexCoord1;

//out vec3 ourColor;
out vec2 TexCoord;
out vec2 TexCoord1;

//uniform mat4 trans;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
//    gl_Position = vec4(aPos,  1.0);
//    gl_Position = trans * vec4(aPos,  1.0);
    gl_Position = projection * view * model * vec4(aPos,  1.0);
//    ourColor = aColor;
    TexCoord = aTexCoord;
    TexCoord1 = aTexCoord1;
}
