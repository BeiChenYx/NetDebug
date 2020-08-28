#ifndef HELLOTRIANGLE_H
#define HELLOTRIANGLE_H

#include <QWidget>
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QOpenGLExtraFunctions>
#include <QOpenGLShaderProgram>
#include <QOpenGLBuffer>
#include <QOpenGLVertexArrayObject>
#include <QOpenGLTexture>
#include <QImage>
#include <QMatrix4x4>
#include <QTimer>


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
    QOpenGLTexture texture;
    QOpenGLTexture texture1;

    QTimer timer;
};

#endif // HELLOTRIANGLE_H
