#include "myopenglwidget.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MyOpenGLWidget w;
    w.show();

    return a.exec();
}
