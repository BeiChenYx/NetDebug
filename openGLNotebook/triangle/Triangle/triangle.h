#ifndef TRIANGLE_H
#define TRIANGLE_H

#include <QWidget>
#include <QOpenGLWidget>
#include <QOpenGLExtraFunctions>
#include <QDebug>


class Triangle : public QOpenGLWidget, protected QOpenGLExtraFunctions
{
    Q_OBJECT

public:
    explicit Triangle();
    ~Triangle();

protected:
    virtual void initializeGL();
    virtual void resizeGL(int w, int h);
    virtual void paintGL();

private:
    GLuint shaderProgram;
};

#endif // TRIANGLE_H
