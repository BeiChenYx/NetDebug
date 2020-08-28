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
#include <QMouseEvent>
#include <QPoint>


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

    void mouseMoveEvent(QMouseEvent *event);
    void mousePressEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);

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

    double yaw;
    double pitch;
    double sensitivity;

    QVector3D cameraPos;
    QVector3D cameraTarget;
    QVector3D cameraDirection;
    QVector3D cameraRight;
    QVector3D cameraUp;

    Qt::MouseButton pressButton = Qt::NoButton;
    QPoint prePos;
};

#endif // HELLOTRIANGLE_H
