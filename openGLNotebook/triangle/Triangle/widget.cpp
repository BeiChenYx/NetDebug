#include "widget.h"

//static GLuint VBO, VAO;
ITriangle::ITriangle(QWidget *parent)
    : QOpenGLWidget(parent)
{

}
ITriangle::~ITriangle()
{

}


void ITriangle::initializeGL()
{
    // 获取上下文
//    core = QOpenGLContext::currentContext()->versionFunctions<QOpenGLFunctions_3_3_Core>();
//    ourShader = new Shader(":/shader/vertexshadersource.vert", ":/shader/fragmentshadersource.frag");

//    GLfloat vertices[] = {
//        0.5f, -0.5f, 0.0f,  1.0f, 0.0f, 0.0f,
//        -0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,
//        0.0f, 0.5f, 0.0f,  0.0f, 0.0f, 1.0f,
//    };

//    core->glGenVertexArrays(1, &VBO);
//    core->glGenBuffers(1, &VBO);
//    core->glBindVertexArray(VAO);
//    // 绑定顶点缓冲对象
//    core->glBindBuffer(GL_ARRAY_BUFFER, VBO);
//    // 把顶点缓冲对象复制到显存中
//    core->glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
//    // 设置顶点属性指针，告诉GPU如何解析顶点数据
//    core->glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), nullptr);
//    // 指定启用顶点数据
//    core->glEnableVertexAttribArray(0);
//    core->glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), reinterpret_cast<GLvoid*>(3 * sizeof(GLfloat)));
//    core->glEnableVertexAttribArray(1);

//    core->glBindBuffer(GL_ARRAY_BUFFER, 0);
//    core->glBindVertexArray(0);

//    core->glClearColor(0.2f, 0.3f, 0.3f, 1.0f);

    this->initializeOpenGLFunctions();
    // 创建顶点着色器, 并编译
    QOpenGLShader vertexShader(QOpenGLShader::Vertex);
    bool success = vertexShader.compileSourceFile(":/shader/vertexshadersource.vert");
    if(!success){
        qDebug() << "ERROR::SHADER::VERTEX::COMPILATION_FAILED";
        qDebug() << vertexShader.log();
    }

    // 创建片段着色器，并编译
    QOpenGLShader fragmentShader(QOpenGLShader::Fragment);
    success = fragmentShader.compileSourceFile(":/shader/fragmentshadersource.frag");
    if(!success){
        qDebug() << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED";
        qDebug() << fragmentShader.log();
    }

    // 添加着色器并链接
    m_pProgram = new QOpenGLShaderProgram();
    m_pProgram->addShader(&vertexShader);
    m_pProgram->addShader(&fragmentShader);
    success = m_pProgram->link();
    if(!success){
        qDebug() << "ERROR::SHADER::PROGAM::LINKING_FAILED";
        qDebug() << m_pProgram->log();
    }
    if(!m_pProgram->bind()){
        qDebug() << "ERROR::SHADER::PROGAM::BIND_FAILED";
        qDebug() << m_pProgram->log();
    }
}

void ITriangle::resizeGL(int w, int h)
{
//    core->glViewport(0, 0, w, h);
}

void ITriangle::paintGL()
{
//    core->glClear(GL_COLOR_BUFFER_BIT);

//    ourShader->use();
//    core->glBindVertexArray(VAO);
//    core->glDrawArrays(GL_TRIANGLES, 0, 3);

    GLfloat vertices[] = {
        0.5f, -0.5f, 0.0f,
        -0.5f, -0.5f, 0.0f,
        0.0f, 0.5f, 0.0f,
    };
    vbo.create();
    vbo.bind();
    vbo.allocate(vertices, 9 * sizeof(GLfloat));
    auto aPos = m_pProgram->attributeLocation("aPos");
    m_pProgram->setAttributeBuffer(aPos, GL_FLOAT, 9 * sizeof(GLfloat), 2, 0);
    glEnableVertexAttribArray(static_cast<GLuint>(aPos));

    glDrawArrays(GL_TRIANGLES, 0, 3);
}

