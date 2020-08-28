#ifndef MYOPENGLWIDGET_H
#define MYOPENGLWIDGET_H

#include <QWidget>
#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QOpenGLShaderProgram>
#include <QOpenGLBuffer>


class MyOpenGLWidget : public QOpenGLWidget, protected QOpenGLFunctions
{
    Q_OBJECT

public:
    MyOpenGLWidget(QWidget *parent = nullptr);
    ~MyOpenGLWidget();

protected:
    // QGLWidget提供了3个方便的虚函数，重新实现就行
    void initializeGL(); // 该韩式只在第一次调用resizeGL()或paintGL()前被调用一次
    void resizeGL(int w, int h);
    void paintGL();

private:
    QOpenGLShaderProgram *m_pProgram;
    QOpenGLBuffer vbo;
};

#endif // MYOPENGLWIDGET_H
