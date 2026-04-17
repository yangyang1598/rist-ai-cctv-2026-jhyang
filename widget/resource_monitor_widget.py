import sys
import psutil
import GPUtil
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar, QGridLayout)
from PySide6.QtCore import QTimer, QDateTime, Qt
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtGui import QPainter, QColor
import datetime



class ResourceMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resource Monitor")
        self.resize(1200, 900)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        # CPU
        self.cpu_label = QLabel("CPU Usage: 0%")
        self.cpu_bar = QProgressBar()
        self.grid.addWidget(self.cpu_label, 0, 0)
        self.grid.addWidget(self.cpu_bar, 0, 1)

        # RAM
        self.ram_label = QLabel("RAM Usage: 0/0 GB")
        self.ram_bar = QProgressBar()
        self.grid.addWidget(self.ram_label, 1, 0)
        self.grid.addWidget(self.ram_bar, 1, 1)

        self.gpus = GPUtil.getGPUs()
        self.gpu_labels, self.gpu_bars, self.gpu_vram_labels = [], [], []
        for idx, gpu in enumerate(self.gpus):
            gpu_label = QLabel(f"GPU {idx} Usage: 0%")
            gpu_bar = QProgressBar()
            vram_label = QLabel(f"VRAM Usage: 0/0 GB")
            self.grid.addWidget(gpu_label, 2 + idx * 2, 0)
            self.grid.addWidget(gpu_bar, 2 + idx * 2, 1)
            self.grid.addWidget(vram_label, 3 + idx * 2, 0, 1, 2)
            self.gpu_labels.append(gpu_label)
            self.gpu_bars.append(gpu_bar)
            self.gpu_vram_labels.append(vram_label)

        # Create CPU + GPU chart (% Y-axis)
        self.cpu_gpu_chart = QChart()
        self.cpu_gpu_chart.setTitle("CPU + GPU Usage (%)")
        self.cpu_gpu_chart.legend().setVisible(True)
        self.cpu_series = QLineSeries(name="CPU")
        self.cpu_series.setColor(QColor("red"))
        self.gpu_series = []
        self.cpu_gpu_chart.addSeries(self.cpu_series)

        gpu_colors = ["blue", "green", "orange", "purple"]
        for idx in range(len(self.gpus)):
            series_gpu = QLineSeries(name=f"GPU {idx}")
            series_gpu.setColor(QColor(gpu_colors[idx % len(gpu_colors)]))
            self.cpu_gpu_chart.addSeries(series_gpu)
            self.gpu_series.append(series_gpu)

        self.setup_chart(self.cpu_gpu_chart, 0, "%", self.cpu_series, *self.gpu_series)
        self.layout.addWidget(QChartView(self.cpu_gpu_chart))

        # RAM chart (GB)
        self.ram_chart = QChart()
        self.ram_chart.setTitle("RAM Usage (GB)")
        self.ram_chart.legend().setVisible(True)
        self.ram_series = QLineSeries(name="RAM")
        self.ram_series.setColor(QColor("darkred"))
        self.ram_chart.addSeries(self.ram_series)
        self.setup_chart(self.ram_chart, 1, "GB", self.ram_series)
        self.layout.addWidget(QChartView(self.ram_chart))

        # VRAM chart (GB)
        self.vram_chart = QChart()
        self.vram_chart.setTitle("VRAM Usage (GB)")
        self.vram_chart.legend().setVisible(True)
        self.vram_series = []
        for idx in range(len(self.gpus)):
            series_vram = QLineSeries(name=f"VRAM {idx}")
            series_vram.setColor(QColor(gpu_colors[idx % len(gpu_colors)]))
            self.vram_chart.addSeries(series_vram)
            self.vram_series.append(series_vram)
        self.setup_chart(self.vram_chart, 1, "GB", *self.vram_series)
        self.layout.addWidget(QChartView(self.vram_chart))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def setup_chart(self, chart, value_type=0, unit="%", *series_list):
        time_axis = QDateTimeAxis()
        time_axis.setFormat("hh:mm:ss")
        time_axis.setTitleText("Time")
        chart.addAxis(time_axis, Qt.AlignBottom)

        value_axis = QValueAxis()
        if value_type == 0:
            value_axis.setRange(0, 100)
        else:
            value_axis.setRange(0, 16)  # Default max GB
        value_axis.setTitleText(f"Usage ({unit})")
        chart.addAxis(value_axis, Qt.AlignLeft)

        for series in series_list:
            series.attachAxis(time_axis)
            series.attachAxis(value_axis)

    def update_stats(self):
        now = QDateTime.currentDateTime()
        timestamp = now.toMSecsSinceEpoch()

        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU Usage: {cpu_percent}%")
        self.cpu_bar.setValue(int(cpu_percent))
        self.cpu_series.append(timestamp, cpu_percent)

        mem = psutil.virtual_memory()
        ram_gb = mem.used / (1024 ** 3)
        total_gb = mem.total / (1024 ** 3)
        self.ram_label.setText(f"RAM Usage: {ram_gb:.2f}/{total_gb:.2f} GB")
        self.ram_bar.setValue(int(mem.percent))
        self.ram_series.append(timestamp, ram_gb)

        max_vram_gb = 0

        self.gpus = GPUtil.getGPUs()
        for idx, gpu in enumerate(self.gpus):
            load_percent = gpu.load * 100
            vram_used = gpu.memoryUsed / 1024  # Convert MB to GB
            vram_total = gpu.memoryTotal / 1024  # Convert MB to GB
            max_vram_gb = max(max_vram_gb, vram_total)

            self.gpu_labels[idx].setText(f"GPU {idx} Usage: {load_percent:.1f}%")
            self.gpu_bars[idx].setValue(int(load_percent))
            self.gpu_vram_labels[idx].setText(f"VRAM Usage: {vram_used:.1f}/{vram_total:.1f} GB")

            self.gpu_series[idx].append(timestamp, load_percent)
            self.vram_series[idx].append(timestamp, vram_used)

        self.trim_series(self.cpu_series)
        self.trim_series(self.ram_series)
        for s in self.gpu_series + self.vram_series:
            self.trim_series(s)

        for chart in [self.cpu_gpu_chart, self.ram_chart, self.vram_chart]:
            chart.axisX().setRange(now.addSecs(-60), now)

        # Update Y-axis range for RAM and VRAM chart
        ram_axis = self.ram_chart.axisY()
        vram_axis = self.vram_chart.axisY()
        if ram_axis:
            ram_axis.setRange(0, mem.total / (1024 ** 3) * 1.1)
        if vram_axis:
            vram_axis.setRange(0, max_vram_gb * 1.1)

    def trim_series(self, series, max_points=60):
        while series.count() > max_points:
            series.remove(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = ResourceMonitorWidget()
    monitor.show()
    sys.exit(app.exec())