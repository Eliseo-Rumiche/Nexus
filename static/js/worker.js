let cardColor = config.colors.white;
let headingColor = config.colors.headingColor;
let axisColor = config.colors.axisColor;
let borderColor = config.colors.borderColor;

const chartOrderStatistics = document.querySelector("#attendanceDetailChart"),
  orderChartConfig = {
    chart: {
      height: 165,
      width: 130,
      type: "donut",
    },
    labels: labels_chart,
    series: series_chart,
    colors: [
      config.colors.success,
      config.colors.danger,
      config.colors.info,
      config.colors.secondary,
    ],
    stroke: {
      width: 5,
      colors: cardColor,
    },
    dataLabels: {
      enabled: false,
      formatter: function (val, opt) {
        return parseInt(val) + "%";
      },
    },
    legend: {
      show: false,
    },
    grid: {
      padding: {
        top: 0,
        bottom: 0,
        right: 15,
      },
    },
    plotOptions: {
      pie: {
        donut: {
          size: "75%",
          labels: {
            show: true,
            value: {
              fontSize: "1.5rem",
              fontFamily: "Public Sans",
              color: headingColor,
              offsetY: -15,
              formatter: function (val) {
                return parseInt(val) + "%";
              },
            },
            name: {
              offsetY: 20,
              fontFamily: "Public Sans",
            },
            total: {
              show: true,
              fontSize: "0.8125rem",
              color: axisColor,
              label: "Asistencias",
              formatter: function (w) {
                return "100%";
              },
            },
          },
        },
      },
    },
  };
if (
  typeof chartOrderStatistics !== undefined &&
  chartOrderStatistics !== null
) {
  const statisticsChart = new ApexCharts(
    chartOrderStatistics,
    orderChartConfig
  );
  statisticsChart.render();
}
