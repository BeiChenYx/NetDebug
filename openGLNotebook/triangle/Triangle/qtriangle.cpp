#include "qtriangle.h"

// 定义顶点着色器
const static char *vertexShaderSource =
        "#version 330 core\n"
        "layout(location = 0) in vec3 aPos;\n"
        "void main(){\n"
        "  gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
        "}\n\0";

// 定义片段着色器
const static char *fragmentShaderSource =
        "#version 330 core\n"
        "out vec4 FragColor;\n"
        "void main(){\n"
        "  FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);\n"
        "}\n\0";


QTriangle::QTriangle()
{

}

QTriangle::~QTriangle()
{

}

void QTriangle::initializeGL()
{
    // 这个init(()函数至关重要,如果继承QOpenGLFunctions，必须使用之歌初始化函数
    this->initializeOpenGLFunctions();

    QOpenGLShader vertexShader(QOpenGLShader::Vertex);
    bool success = vertexShader.compileSourceCode(vertexShaderSource);
    if(!success){
        qDebug() << "ERROR:SHADER::VERTEX::COMPILATION_FAILED";
        return;
    }

    QOpenGLShader fragmentShader(QOpenGLShader::Fragment);
    success = vertexShader.compileSourceCode(fragmentShaderSource);
    if(!success){
        qDebug() << "ERROR:SHADER::FRAGMENT::COMPILATION_FAILED";
        return;
    }

    shaderProgram.addShader(&vertexShader);
    shaderProgram.addShader(&fragmentShader);
    success = shaderProgram.link();
    if(!success){
        qDebug() << "ERROR:SHADER::LINKING::LINKING_FAILED";
        return;
    }
    success = shaderProgram.bind();
    if(!success){
        qDebug() << "ERROR:SHADER::BIND::BIND_FAILED";
    }

    // VAO, VBO数据部分
    vertices.append(QVector3D(-0.5, -0.5, 0.0));
    vertices.append(QVector3D(0.5, -0.5, 0.0));
    vertices.append(QVector3D(0.0, 0.5, 0.0));
}

void QTriangle::resizeGL(int w, int h)
{
    glViewport(0, 0, w, h);
}

void QTriangle::paintGL()
{
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // 等价 glUseProgram(shaderProgram)
    shaderProgram.bindAttributeLocation("aPos", 0);
    shaderProgram.enableAttributeArray(0);
    shaderProgram.setAttributeArray(0, vertices.data());
    glDrawArrays(GL_TRIANGLES, 0, vertices.size());
}



