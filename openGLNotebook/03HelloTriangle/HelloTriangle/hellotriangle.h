#ifndef HELLOTRIANGLE_H
#define HELLOTRIANGLE_H

#include <QWidget>
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QOpenGLExtraFunctions>
#include <QOpenGLShaderProgram>
#include <QOpenGLBuffer>
#include <QOpenGLVertexArrayObject>



class HelloTriangle : public QOpenGLWidget, protected QOpenGLExtraFunctions
{
    Q_OBJECT

public:
    HelloTriangle(QWidget *parent = nullptr);
    ~HelloTriangle();

protected:
    void initializeGL();
    void resizeGL(int w, int h);
    void paintGL();

private:
    QVector<float> vertices;
    QVector<unsigned int> indices;
    QOpenGLShaderProgram shaderProgram;
    QOpenGLBuffer VBO;
    QOpenGLBuffer IBO;
    QOpenGLVertexArrayObject VAO;
};

#endif // HELLOTRIANGLE_H
