#version 330 core
out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;
in vec2 TexCoord1;

uniform sampler2D ourTexture;
uniform sampler2D ourTexture1;

void main()
{
    FragColor = mix(texture2D(ourTexture, TexCoord), texture2D(ourTexture1, TexCoord1), 0.2);
}
