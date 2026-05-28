from desktop.windows import MainWindow
import core.listeners


def main():
    app = MainWindow()
    print("Starting desktop launcher!")
    app.mainloop()


if __name__ == "__main__":
    main()
