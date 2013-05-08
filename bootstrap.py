import subprocess
from edu.harvard.e185.word_count_visualizer import WordCountVisualizer


def main():
    visualizer = WordCountVisualizer()
    visualizer.bootstrap()
    packages = [
        'pycassa'
    ]

    map(lambda x: subprocess.check_call(['pip', 'install', x]), packages)


if __name__ == '__main__':
    main()
