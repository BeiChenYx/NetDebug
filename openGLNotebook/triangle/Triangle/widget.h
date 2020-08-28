#ifndef WIDGET_H
#define WIDGET_H

#include <QDebug>
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QOpenGLShaderProgram>
#include <QOpenGLBuffer>
//#include <QOpenGLFunctions_3_3_Core>
//#include "shader.h"

//class ITriangle : public QOpenGLWidget
class ITriangle : public QOpenGLWidget, protected QOpenGLFunctions
{
    Q_OBJECT

public:
    ITriangle(QWidget *parent = nullptr);
    ~ITriangle();

protected:
    virtual void initializeGL();
    virtual void resizeGL(int w, int h);
    virtual void paintGL();

private:
//    Shader *ourShader;
//    QOpenGLFunctions_3_3_Core *core;
    QOpenGLShaderProgram *m_pProgram;
    QOpenGLBuffer vbo;
    QOpenGLBuffer vao;
};

#endif // WIDGET_H
