#include <QDebug>
#include "myopenglwidget.h"

MyOpenGLWidget::MyOpenGLWidget(QWidget *parent)
    : QOpenGLWidget(parent)
{
}

MyOpenGLWidget::~MyOpenGLWidget()
{

}

void MyOpenGLWidget::initializeGL()
{
    this->initializeOpenGLFunctions();

    QOpenGLShader *vshader = new QOpenGLShader(QOpenGLShader::Vertex, this);
    const char *vsrc =
                "#version 330                              \n"
                "in vec4 vPosition;                        \n"
                "in vec4 vColor;                           \n"
                "out vec4 color;                           \n"
                "uniform mat4 matrix;                      \n"
                "void main() {                             \n"
                "   color = vColor;                        \n"
                "   gl_Position = matrix * vPosition;      \n"
                "}                                         \n";
    vshader->compileSourceCode(vsrc);

    QOpenGLShader *fshader = new QOpenGLShader(QOpenGLShader::Fragment, this);
    const char *fsrc =
                "#version 330                               \n"
                "in vec4 color;                             \n"
                "out vec4 fColor;                           \n"
                "void main() {                              \n"
                "   fColor = color;                         \n"
                "}                                          \n";
    fshader->compileSourceCode(fsrc);
    m_pProgram = new QOpenGLShaderProgram();
    m_pProgram->addShader(vshader);
    m_pProgram->addShader(fshader);
    m_pProgram->link();
    m_pProgram->bind();
}

void MyOpenGLWidget::resizeGL(int w, int h)
{
    qDebug() << "resizeGL";
}

void MyOpenGLWidget::paintGL()
{
    qDebug() << "paintGL";
    int w = width();
    int h = height();
    int side = qMin(w, h);
    glViewport((w - side) / 2, (h - side) / 2, side, side);

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    GLfloat vertices[2][4][3] = {
        {{-0.8f, 0.8f, 0.8f}, {-0.8f, -0.8f, 0.8f}, {0.8f, -0.8f, 0.8f}, {0.8f, 0.8f, 0.8f}},
        {{0.8f, 0.8f, 0.8f}, {0.8f, -0.8f, 0.8f}, {0.8f, -0.8f, -0.8f}, {0.8f, 0.8f, -0.8f}}
    };

    vbo.create();
    vbo.bind();
    vbo.allocate(vertices, 48 * sizeof(GLfloat));

    auto vPosition = m_pProgram->attributeLocation("vPosition");
    m_pProgram->setAttributeBuffer(vPosition, GL_FLOAT, 0, 3, 0);
//    glVertexAttribPointer(vPosition, 2, GL_FLOAT, GL_FALSE, 0, vertices);
    glEnableVertexAttribArray(static_cast<GLuint>(vPosition));

    GLfloat colors[2][4][3] = {
        {{1.0f, 0.0f, 0.0f}, {0.0f, 1.0f, 0.0f}, {0.0f, 0.0f, 1.0f}, {1.0f, 1.0f, 1.0f}},
        {{1.0f, 0.0f, 0.0f}, {0.0f, 1.0f, 0.0f}, {0.0f, 0.0f, 1.0f}, {1.0f, 1.0f, 1.0f}}
    };
    vbo.write(24 * sizeof(GLfloat), colors, 24 * sizeof(GLfloat));
    auto vColor = m_pProgram->attributeLocation("vColor");
    m_pProgram->setAttributeBuffer(vColor, GL_FLOAT, 24 * sizeof(GLfloat), 3, 0);
    glEnableVertexAttribArray(static_cast<GLuint>(vColor));

    QMatrix4x4 matrix;
    matrix.perspective(45.0f, static_cast<GLfloat>(w)/static_cast<GLfloat>(h), 0.1f, 100.0f);
    matrix.translate(0, 0, -3);
    matrix.rotate(-60, 0, 1, 0);
    matrix.rotate(-30, 1, 0, 0);
    matrix.rotate(-90, 0, 0, 1);
    m_pProgram->setUniformValue("matrix", matrix);

    for(int i=0; i<2; ++i){
        glDrawArrays(GL_TRIANGLE_FAN, i*4, 4);
    }

}
