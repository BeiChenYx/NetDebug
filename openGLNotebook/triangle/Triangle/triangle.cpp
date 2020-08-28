#include "triangle.h"

// VBO: 顶点缓冲对象，VAO: 顶点数组对象
static GLuint VBO, VAO;
// 定义顶点着色器
const static char *vertexShaderSource =
        "#version 330 core\n"
        "layout(location = 0) in vec3 aPos;\n"
        "void main(){\n"
        "  gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
        "}\n\0";

// 定义片段着色器
const static char *fragmentShaderSource =
        "#version 330 core\n"
        "out vec4 FragColor;\n"
        "void main(){\n"
        "  FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);\n"
        "}\n\0";


Triangle::Triangle()
{
}

Triangle::~Triangle()
{
}

void Triangle::initializeGL()
{
    // 着色器部分
    this->initializeOpenGLFunctions();
    // 创建顶点着色器, GL_VERTEX_SHADER: 指定创建顶点着色器
    uint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    // 把vertexShader着色器附加到着色器对象上
    glShaderSource(vertexShader, 1, &vertexShaderSource, nullptr);
    // 编译着色器
    glCompileShader(vertexShader);

    // 检测在调用glCompileShader后编译是否成功，并在失败时输出错误
    int success;
    QByteArray infoLog(512, char());
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if(!success){
        glGetShaderInfoLog(vertexShader, 512, nullptr, infoLog.data());
        qDebug() << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << QString(infoLog);
    }

    // 创建，配置，编译片段着色器
    uint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, nullptr);
    glCompileShader(fragmentShader);

    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
    if(!success){
        glGetShaderInfoLog(fragmentShader, 512, nullptr, infoLog.data());
        qDebug() << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << QString(infoLog);
    }

    // 创建着色器程序
    shaderProgram = glCreateProgram();
    // 将顶点着色器附加到着色器程序
    glAttachShader(shaderProgram, vertexShader);
    // 将片段着色器附加到着色器程序
    glAttachShader(shaderProgram, fragmentShader);
    // 链接着色器程序
    glLinkProgram(shaderProgram);

    // 检测着色器程序链接是否失败
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if(!success){
        glGetShaderInfoLog(shaderProgram, 512, nullptr, infoLog.data());
        qDebug() << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << QString(infoLog);
    }
    // 把着色器对象链接到着色器程序对象后，不再使用后，可以删除着色器对象
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    // VAO, VBO 数据部分
    GLfloat vertices[]{
        -0.5f, -0.5f, 0.0f, // Left
        0.5f, -0.5f, 0.0f,  // right
        0.0f, 0.5f, 0.0f,    // top
    };

    // 创建一个VAO
    glGenVertexArrays(1, &VAO);
    // 创建一个VBO
    glGenBuffers(1, &VBO);
    // 绑定VAO
    glBindVertexArray(VAO);
    // 复制顶点数组到缓冲中供OpenGL使用
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    // 设置顶点属性指针
    glVertexAttribPointer(0, 3, GL_FLOAT,GL_FALSE, 3 * sizeof(GLfloat), nullptr);
    glEnableVertexAttribArray(0);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
}

void Triangle::resizeGL(int w, int h)
{
    // 设置OpenGL视口大小, 参数 x, y, with, height
    glViewport(0, 0, w, h);
}

void Triangle::paintGL()
{
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // 激活着色器程序
    glUseProgram(shaderProgram);
    glBindVertexArray(VAO);
    glDrawArrays(GL_TRIANGLES, 0, 3);
    glUseProgram(0);
}



