#ifndef QTRIANGLE_H
#define QTRIANGLE_H

// 使用Qt风格完成三角形绘制
#include <QOpenGLWidget>
#include <QOpenGLShader>
#include <QOpenGLShaderProgram>
#include <QOpenGLFunctions>
#include <QOpenGLFunctions_3_3_Core>
#include <QDebug>
#include <QVector>
#include <QVector3D>

class QTriangle : public QOpenGLWidget, protected QOpenGLFunctions
{
public:
    QTriangle();
    ~QTriangle();

protected:
    virtual void initializeGL();
    virtual void resizeGL(int w, int h);
    virtual void paintGL();

private:
    QOpenGLShaderProgram shaderProgram;
    QVector<QVector3D> vertices;
};

#endif // QTRIANGLE_H
