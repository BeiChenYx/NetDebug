#ifndef SHADER_H
#define SHADER_H

#include <QDebug>
#include <QOpenGLShader>
#include <QOpenGLShaderProgram>


class Shader
{
public:
    Shader(const QString &vertexSourcePath, const QString &fragmentSourcePath);
    ~Shader(){}

    void use(){
        shaderProgram.bind();
    }

public:
    QOpenGLShaderProgram shaderProgram;
};

#endif // SHADER_H
