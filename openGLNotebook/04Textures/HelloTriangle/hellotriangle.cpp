#include <QTime>
#include <QtMath>
#include "hellotriangle.h"

HelloTriangle::HelloTriangle(QWidget *parent)
    : QOpenGLWidget(parent),
      VBO(QOpenGLBuffer::VertexBuffer),
      IBO(QOpenGLBuffer::IndexBuffer),
      texture(QOpenGLTexture::Target2D),
      texture1(QOpenGLTexture::Target2D)
{
    vertices = {
        // 位置                  // 颜色              // 纹理坐标
        0.5f, 0.5f, 0.0f,       1.0f, 0.0f, 0.0f,   1.0f, 0.0f,     1.0f, 1.0f,
        0.5f, -0.5f, 0.0f,      0.0f, 1.0f, 0.0f,   0.0f, 0.0f,     1.0f, 0.0f,
        -0.5f, -0.5f, 0.0f,     0.0f, 0.0f, 1.0f,   0.0f, 1.0f,     0.0f, 0.0f,
        -0.5f, 0.5f, 0.0f,      1.0f, 1.0f, 0.0f,   1.0f, 1.0f,     0.0f, 1.0f,
    };
    indices = {
        0, 1, 3,
        1, 2, 3
    };

    timer.setInterval(100);
    connect(&timer, &QTimer::timeout, this, [this](){
        this->update();
    });
    timer.start();
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
    shaderProgram.setAttributeBuffer(aPos, GL_FLOAT, 0, 3, sizeof(GLfloat) * 10);
    // 启用点点属性
    shaderProgram.enableAttributeArray(aPos);

    shaderProgram.setAttributeBuffer("aColor", GL_FLOAT, sizeof(GLfloat) * 3, 3, sizeof(GLfloat) * 10);
    shaderProgram.enableAttributeArray("aColor");

    shaderProgram.setAttributeBuffer("aTexCoord", GL_FLOAT, sizeof(GLfloat) * 6, 2, sizeof(GLfloat) * 10);
    shaderProgram.enableAttributeArray("aTexCoord");

    shaderProgram.setAttributeBuffer("aTexCoord1", GL_FLOAT, sizeof(GLfloat) * 8, 2, sizeof(GLfloat) * 10);
    shaderProgram.enableAttributeArray("aTexCoord1");


    // 查询顶点属性允许的个数
    int count = 0;
    this->glGetIntegerv(GL_MAX_VERTEX_ATTRIBS, &count);
    qDebug() << "Maximum nr of vertex attributes supported: " << count;
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
    glClear(GL_COLOR_BUFFER_BIT);

    QMatrix4x4 trans;
//    trans.translate(0.5f, 0.0f, 0.0f); // 向x轴移动0.5个单位
//    trans.rotate(90, 0.0f, 0.0f, -1.0f); // 以z轴负方向为旋转轴，ni逆时针旋转90度(等价顺时针旋转)
//    trans.scale(1.5f, 0.5f, 1.0f); // 将 x放大为原来的1.5倍，y缩放为原来的0.5
    float time = QTime::currentTime().msecsSinceStartOfDay() / 1000.0;
    trans.translate(0.0f, 0.5 * qAbs(qSin(time)), 0.0f);
    trans.scale(0.5 * qAbs(qSin(time)), 0.5 * qAbs(qSin(time)));
    trans.rotate(360 * time, 0.0f, 0.0f, -1.0f);
    shaderProgram.setUniformValue("trans", trans);



    // 使用shaderProgram的着色程序
    shaderProgram.bind();

    texture.bind(0);
    shaderProgram.setUniformValue("ourTexture", 0);
    texture1.bind(1);
    shaderProgram.setUniformValue("ourTexture1", 1);

    QOpenGLVertexArrayObject::Binder{&VAO};
    this->glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
}
