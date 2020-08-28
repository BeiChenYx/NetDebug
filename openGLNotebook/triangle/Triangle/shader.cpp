#include "shader.h"

Shader::Shader(const QString &vertexSourcePath, const QString &fragmentSourcePath)
{
    // 创建顶点着色器, 并编译
    QOpenGLShader vertexShader(QOpenGLShader::Vertex);
    bool success = vertexShader.compileSourceFile(vertexSourcePath);
    if(!success){
        qDebug() << "ERROR::SHADER::VERTEX::COMPILATION_FAILED";
        qDebug() << vertexShader.log();
    }

    // 创建片段着色器，并编译
    QOpenGLShader fragmentShader(QOpenGLShader::Fragment);
    success = fragmentShader.compileSourceFile(fragmentSourcePath);
    if(!success){
        qDebug() << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED";
        qDebug() << fragmentShader.log();
    }

    // 添加着色器并链接
    shaderProgram.addShader(&vertexShader);
    shaderProgram.addShader(&fragmentShader);
    success = shaderProgram.link();
    if(!success){
        qDebug() << "ERROR::SHADER::PROGAM::LINKING_FAILED";
        qDebug() << shaderProgram.log();
    }
    if(!shaderProgram.bind()){
        qDebug() << "ERROR::SHADER::PROGAM::BIND_FAILED";
        qDebug() << shaderProgram.log();
    }
}
