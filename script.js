async function fetchData() {
  try {
    const response = await fetch("data.json");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [];
  }
}

async function initChart() {
  const rawData = await fetchData();

  if (rawData.length === 0) {
    alert("No data found. Please run 'python download_data.py' first.");
    return;
  }

  const labels = rawData.map((d) => d.date);
  const ratioData = rawData.map((d) => d.ratio);

  // Update footer date
  const lastDate = labels[labels.length - 1];
  document.getElementById("lastUpdated").textContent = lastDate;

  const ctx = document.getElementById("ratioChart").getContext("2d");

  // Gradient fill
  const gradient = ctx.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, "rgba(255, 215, 0, 0.5)"); // Gold with opacity
  gradient.addColorStop(1, "rgba(255, 215, 0, 0.0)");

  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "S&P 500 / Gold Ratio",
          data: ratioData,
          borderColor: "#ffd700",
          backgroundColor: gradient,
          borderWidth: 2,
          pointRadius: 0, // Hide points for cleaner look
          pointHoverRadius: 4,
          fill: true,
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false,
      },
      plugins: {
        zoom: {
          zoom: {
            wheel: {
              enabled: true,
            },
            pinch: {
              enabled: true,
            },
            mode: "x",
          },
          pan: {
            enabled: true,
            mode: "x",
          },
        },
        tooltip: {
          backgroundColor: "rgba(30, 30, 30, 0.9)",
          titleColor: "#fff",
          bodyColor: "#ffd700",
          borderColor: "#ffd700",
          borderWidth: 1,
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || "";
              if (label) {
                label += ": ";
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y.toFixed(2) + " oz";
              }
              return label;
            },
          },
        },
        legend: {
          labels: {
            color: "#e0e0e0",
          },
        },
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "year",
            displayFormats: {
              year: "yyyy",
            },
          },
          grid: {
            color: "#333",
          },
          ticks: {
            color: "#a0a0a0",
          },
        },
        y: {
          grid: {
            color: "#333",
          },
          ticks: {
            color: "#a0a0a0",
          },
          title: {
            display: true,
            text: "Ounces of Gold to buy S&P 500",
            color: "#a0a0a0",
          },
        },
      },
    },
  });

  document.getElementById("resetZoom").addEventListener("click", () => {
    chart.resetZoom();
  });
}

initChart();
