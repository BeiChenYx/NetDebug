#include "hellotriangle.h"

HelloTriangle::HelloTriangle(QWidget *parent)
    : QOpenGLWidget(parent),
      VBO(QOpenGLBuffer::VertexBuffer),
      IBO(QOpenGLBuffer::IndexBuffer)
{
    vertices = {
        0.5f, 0.5f, 0.0f,
        0.5f, -0.5f, 0.0f,
        -0.5f, -0.5f, 0.0f,
        -0.5f, 0.5f, 0.0f,
    };
    indices = {
        0, 1, 3,
        1, 2, 3
    };
}

HelloTriangle::~HelloTriangle()
{

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

    IBO.create();
    IBO.bind();
    IBO.allocate(indices.data(), static_cast<int>(sizeof(unsigned int)) * indices.size());

    // 链接顶点属性，告诉OpenGL如何解析顶点数据
    // 获取到顶点着色器的变量, 这种方式比直接记住layout(location = 0) 中的 0 比较好
    int aPos = shaderProgram.attributeLocation("aPos");
    // 第一个参数指定要配置的顶点属性，第二个参数指定数据类型
    shaderProgram.setAttributeBuffer(aPos, GL_FLOAT, 0, 3, sizeof(GLfloat) * 3);
    // 启用点点属性
    shaderProgram.enableAttributeArray(aPos);
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
    // 使用shaderProgram的着色程序
    shaderProgram.bind();
    QOpenGLVertexArrayObject::Binder{&VAO};
    this->glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);
}
