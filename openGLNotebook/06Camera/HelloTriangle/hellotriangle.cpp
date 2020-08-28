#include <QTime>
#include <QtMath>
#include "hellotriangle.h"

HelloTriangle::HelloTriangle(QWidget *parent)
    : QOpenGLWidget(parent),
      VBO(QOpenGLBuffer::VertexBuffer),
      IBO(QOpenGLBuffer::IndexBuffer),
      texture(QOpenGLTexture::Target2D),
      texture1(QOpenGLTexture::Target2D),
      yaw(0.0),
      pitch(0.0),
      sensitivity(0.01),
      cameraPos(0.0f, 4.0f, 3.0f),
      cameraTarget(0.0f, 0.0f, 0.0f),
      cameraDirection(cameraPos - cameraTarget),
      cameraRight(QVector3D::crossProduct({0.0f, 1.0f, 0.0f}, cameraDirection)),
      cameraUp(QVector3D::crossProduct(cameraDirection, cameraRight))
{
    vertices = {
        // 位置                // 纹理坐标
        // 正面
        0.5f, 0.5f, -0.5f,     1.0f, 0.0f,     1.0f, 1.0f, // 右上
        0.5f, -0.5f, -0.5f,    0.0f, 0.0f,     1.0f, 0.0f, // 右下
        -0.5f, -0.5f, -0.5f,   0.0f, 1.0f,     0.0f, 0.0f, // 左下
        -0.5f, 0.5f, -0.5f,    1.0f, 1.0f,     0.0f, 1.0f, // 左上

        // 右面
        0.5f, 0.5f, 0.5f,   1.0f, 0.0f,   1.0f, 1.0f,
        0.5f, -0.5f, 0.5f,  0.0f, 0.0f,   1.0f, 0.0f,
        0.5f, -0.5f, -0.5f,   0.0f, 1.0f,     0.0f, 0.0f,
        0.5f, 0.5f, -0.5f,    1.0f, 1.0f,     0.0f, 1.0f,

        // 后面
        0.5f,  0.5f, 0.5f,    1.0f, 0.0f,     1.0f, 1.0f,
        0.5f, -0.5f, 0.5f,    0.0f, 0.0f,     1.0f, 0.0f,
        -0.5f, -0.5f,0.5f,   0.0f, 1.0f,     0.0f, 0.0f,
        -0.5f, 0.5f, 0.5f,    1.0f, 1.0f,     0.0f, 1.0f,

        // 左面
        -0.5f, 0.5f, 0.5f,     1.0f, 0.0f,     1.0f, 1.0f,
        -0.5f, -0.5f,0.5f,    0.0f, 0.0f,     1.0f, 0.0f,
        -0.5f, -0.5f, -0.5f,   0.0f, 1.0f,     0.0f, 0.0f,
        -0.5f, 0.5f, -0.5f,    1.0f, 1.0f,     0.0f, 1.0f,

        // 上面
        0.5f, 0.5f, 0.5f,     1.0f, 0.0f,     1.0f, 1.0f,
        0.5f, 0.5f, -0.5f,     0.0f, 0.0f,     1.0f, 0.0f,
        -0.5f, 0.5f, -0.5f,     0.0f, 1.0f,     0.0f, 0.0f,
        -0.5f, 0.5f,0.5f,    1.0f, 1.0f,     0.0f, 1.0f,

        // 下面
        0.5f, -0.5f,  -0.5f,     1.0f, 0.0f,     1.0f, 1.0f,
        0.5f, -0.5f,  0.5f,    0.0f, 0.0f,     1.0f, 0.0f,
        -0.5f, -0.5f, 0.5f,    0.0f, 1.0f,     0.0f, 0.0f,
        -0.5f, -0.5f, -0.5f,     1.0f, 1.0f,     0.0f, 1.0f,
    };

    for (unsigned int i=0; i<6; ++i) {
        indices.append(0 + 4 * i);
        indices.append(1 + 4 * i);
        indices.append(3 + 4 * i);
        indices.append(1 + 4 * i);
        indices.append(2 + 4 * i);
        indices.append(3 + 4 * i);
    }
}

HelloTriangle::~HelloTriangle()
{
    this->makeCurrent();
    texture.destroy();
    texture1.destroy();
    this->doneCurrent();
}

void HelloTriangle::initializeGL()
{
    this->initializeOpenGLFunctions();
    // 添加并编译顶点着色器
    if(!shaderProgram.addShaderFromSourceFile(QOpenGLShader::Vertex, ":/triangle_vertex.vert")){
        qDebug() << shaderProgram.log();
    }
    // 添加并编译片段着色器
    if(!shaderProgram.addShaderFromSourceFile(QOpenGLShader::Fragment, ":/triangle_fragment.frag")){
        qDebug() << shaderProgram.log();
    }
    // 链接着色器
    if(!shaderProgram.link()){
        qDebug() << shaderProgram.log();
    }

    // 绑定VAO(不存在时创建), 离开作用域自动解绑
    QOpenGLVertexArrayObject::Binder{&VAO};
    // 创建VBO对象
    VBO.create();
    // 将VBO绑定到当前的顶点缓冲对象中
    VBO.bind();
    // 将顶点数据分配到VBO中，第一个参数为数据指针，第二个参数为数据的字节长度
    VBO.allocate(vertices.data(), static_cast<int>(sizeof(float)) * vertices.size());

    texture.create();
    texture.setData(QImage(":/container.jpg").mirrored());
    texture.setMinMagFilters(QOpenGLTexture::LinearMipMapLinear, QOpenGLTexture::Linear);
    texture.setWrapMode(QOpenGLTexture::DirectionS, QOpenGLTexture::Repeat);
    texture.setWrapMode(QOpenGLTexture::DirectionT, QOpenGLTexture::Repeat);

    texture1.create();
    texture1.setData(QImage(":/awesomeface.png").mirrored());
    texture1.setMinMagFilters(QOpenGLTexture::LinearMipMapLinear, QOpenGLTexture::Linear);
    texture1.setWrapMode(QOpenGLTexture::DirectionS, QOpenGLTexture::Repeat);
    texture1.setWrapMode(QOpenGLTexture::DirectionT, QOpenGLTexture::Repeat);


    IBO.create();
    IBO.bind();
    IBO.allocate(indices.data(), static_cast<int>(sizeof(unsigned int)) * indices.size());

    // 链接顶点属性，告诉OpenGL如何解析顶点数据
    // 获取到顶点着色器的变量, 这种方式比直接记住layout(location = 0) 中的 0 比较好
    int aPos = shaderProgram.attributeLocation("aPos");
    // 第一个参数指定要配置的顶点属性，第二个参数指定数据类型
    shaderProgram.setAttributeBuffer(aPos, GL_FLOAT, 0, 3, sizeof(GLfloat) * 7);
    // 启用点点属性
    shaderProgram.enableAttributeArray(aPos);

    shaderProgram.setAttributeBuffer("aTexCoord", GL_FLOAT, sizeof(GLfloat) * 3, 2, sizeof(GLfloat) * 7);
    shaderProgram.enableAttributeArray("aTexCoord");

    shaderProgram.setAttributeBuffer("aTexCoord1", GL_FLOAT, sizeof(GLfloat) * 5, 2, sizeof(GLfloat) * 7);
    shaderProgram.enableAttributeArray("aTexCoord1");


    // 查询顶点属性允许的个数
    this->glEnable(GL_DEPTH_TEST);
}

void HelloTriangle::resizeGL(int w, int h)
{
    this->glViewport(0, 0, w, h);
}

void HelloTriangle::paintGL()
{
    // 设置清屏颜色
    glClearColor(0.1f, 0.5f, 0.7f, 1.0f);
    // 清除颜色缓冲
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    QMatrix4x4 model;
//    model.rotate(30.0f, QVector3D(1.0f, 0.0f, 0.0f));
    model.rotate(-45.0f, QVector3D(0.0f, 1.0f, 0.0f));
    shaderProgram.setUniformValue("model", model);

    QMatrix4x4 view;
    view.translate(0.0f, 0.0f, -10.0f);
//    view.lookAt(cameraPos, cameraTarget, cameraUp);
    view.lookAt(cameraPos, cameraPos + cameraDirection, cameraUp);
    shaderProgram.setUniformValue("view", view);

    QMatrix4x4 projection;
    projection.perspective(45.0f, this->width() / this->height(), 0.1f, 100.0f);
    shaderProgram.setUniformValue("projection", projection);

    // 使用shaderProgram的着色程序
    shaderProgram.bind();

    texture.bind(0);
    shaderProgram.setUniformValue("ourTexture", 0);
    texture1.bind(1);
    shaderProgram.setUniformValue("ourTexture1", 1);

    QOpenGLVertexArrayObject::Binder{&VAO};

    this->glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, nullptr);
}

void HelloTriangle::mouseMoveEvent(QMouseEvent *event)
{
    auto pos = event->pos();
    double xoffset = pos.x() - prePos.x();
    double yoffset = pos.y() - prePos.y();
    xoffset *= sensitivity;
    yoffset *= sensitivity;
    yaw += xoffset;
    pitch += yoffset;
    if(pressButton == Qt::LeftButton){
        cameraDirection.setX(static_cast<float>(-yaw));
//        cameraDirection.setX(static_cast<float>(qCos(yaw) * qCos(pitch)));
    }else if(pressButton == Qt::RightButton){
        cameraDirection.setY(static_cast<float>(-pitch));
//        cameraDirection.setY(static_cast<float>(qSin(pitch)));
    }
//    cameraDirection.setZ(static_cast<float>(qSin(yaw) * qCos(pitch)));
    this->update();
    prePos = event->pos();
}

void HelloTriangle::mousePressEvent(QMouseEvent *event)
{
    pressButton = event->button();
    prePos = event->pos();
}

void HelloTriangle::mouseReleaseEvent(QMouseEvent *)
{
    pressButton = Qt::NoButton;
    prePos = geometry().center();
}

