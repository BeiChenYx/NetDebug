#include "triangle.h"
#include "qtriangle.h"
#include "widget.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
//    Triangle w;
//    w.show();
//    QTriangle w;
//    w.show();

    ITriangle w;
    w.show();

    return a.exec();
}
