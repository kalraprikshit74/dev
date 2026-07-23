<template>
  <div class="widget-container">
    <h2 class="dashboard-title">Change Action Dashboard</h2>  
    
    <!-- Filter Bars -->
    <div class="filters-section"> 
      <div class="select-item">
        <span class="select-label">Start Date:</span>
        <input 
          type="Date"
          :key="renderKey"  
          v-model="startDate"
          class="custom-input-style" 
        />
        <span class="select-label">End Date:</span>
        <input 
          type="Date"
          :key="renderKey"
          v-model="endDate"
          class="custom-input-style" 
        />
        <span class="select-label">Group By:</span>
        <select 
          v-model="groupby" 
          class="custom-input-style"
        >
          <option value="current">State</option>
          <option value="severity">Severity</option>

        </select>
        <v-btn
          class="text-none action-btn blue-btn"
          variant="flat"
          size="small"
          @click="submitAction"
        >
          Submit
        </v-btn>
        <v-btn
          class="text-none action-btn blue-btn"
          variant="flat"
          size="small"
          @click = "clearDates"
        >
          Clear
        </v-btn>
      </div>
    </div>

    <!-- Flexible Dashboard Content Area -->
    <div class="dashboard-flex-layout">
      
      <!-- Donut Chart Block -->
      <div class="chart-card">
        <div class="chart-container">
          <div class="svg-wrapper">
            <svg viewBox="0 0 200 200" width="100%" height="100%">
              <!-- Donut Segments -->
              <path
                v-for="(segment, index) in segments"
                :key="index"
                :d="segment.pathData"
                :fill="segment.color"
                stroke="#ffffff"
                stroke-width="1.5"
                class="clickable-segment"
                @click="fetchTableData(segment.label)"
              />

              <!-- Percentage Labels -->
              <text
                v-for="(segment, index) in segments"
                :key="'label-' + index"
                :x="segment.labelX"
                :y="segment.labelY"
                fill="#ffffff"
                font-size="9"
                font-weight="bold"
                text-anchor="middle"
                dominant-baseline="central"
                class="label-shadow pointer-events-none"
              >
                {{ segment.percentage }}%
              </text>

              <!-- Center Text (Total) -->
              <text x="100" y="90" text-anchor="middle" fill="#333333" font-size="12">Total</text>
              <text x="100" y="115" text-anchor="middle" fill="#333333" font-size="20" font-weight="bold">
                {{ totalValue }}
              </text>
            </svg>
          </div>

          <!-- Legend -->
          <div class="legend">
            <div v-for="(item, index) in chartData" :key="index" class="legend-item">
              <span class="legend-color" :style="{ backgroundColor: item.color }"></span>
              <span class="legend-label">{{ item.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table Block -->
      <div class="table-card">
        <div class="table-container">
          <table class="custom-table">
            <thead>
              <tr>
                <th colspan="3">Change Action - Details</th>
              </tr>
              <tr>
                <th>
                  <div class="header-content">
                    <span class="header-label">Owner</span>
                  </div>
                </th>
                <th>
                  <div class="header-content">
                    <span class="header-label">Name</span>
                  </div>
                </th>
                <th>
                  <div class="header-content">
                    <span class="header-label">Current</span>
                  </div>
                </th>
                <th>
                  <div class="header-content">
                    <span class="header-label">Type</span>
                  </div>
                </th>
                <th>
                  <div class="header-content">
                    <span class="header-label">Revision</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in tableData" :key="idx">
                <td>{{ row.owner }}</td>
                <td>
                  <span class="status-badge" >
                    {{ row.name }}
                  </span>
                </td>
                <td class="date-cell">{{ row.current }}</td>
                <td class="date-cell">{{ row.type }}</td>
                <td class="date-cell">{{ row.revision }}</td>

              </tr>
              <tr v-if="tableData.length === 0">
                <td colspan="3" class="empty-table-state">No matching dashboard records found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { groupBy } from 'lodash';
import { ref, computed, onMounted } from 'vue';
const startDate = ref('');
const endDate = ref('');
const renderKey = ref(0);
const url = ref('');
const groupby = ref(['state'])

const chartData = ref([]);

const tableData = ref([]);

const getStatusColor = (statusLabel) => {
  const match = chartData.value.find(item => item.label.toLowerCase() === statusLabel.toLowerCase());
  return match ? match.color : '#718096';
};

const clearDates = () => {
  startDate.value = '';
  endDate.value = '';
  renderKey.value += 1;
};

const getServiceURL = async () => {
  return new Promise((resolve, reject) => {
    requirejs(["DS/i3DXCompassServices/i3DXCompassServices"], (services) => {
      services.getServiceUrl({
        serviceName: "3DSpace",
        platformId: widget.getValue("x3dPlatformId"),
        onComplete(data) {
          resolve(data);
        },
        onFailure(error) {
          console.error(`Error: ${JSON.stringify(error)}`); // Replaced legacy LOG
          reject(error);
        },
      });
    });
  });
};

/**
 * Sends an authenticated request via Dassault Systèmes WAFData
 * @param {string} endpoint - The API endpoint suffix (e.g., '/resources/data')
 * @param {string} methodType - HTTP Method (e.g., 'GET', 'POST')
 */
const sendSimpleRequest = async (endpoint, methodType) => {
  return new Promise((resolve, reject) => {
    requirejs(["DS/WAFData/WAFData"], (WAFData) => {
      const apiUrl = `${url.value}${endpoint}`;
      WAFData.authenticatedRequest(apiUrl, {
        method: methodType,
        timeout: 600000,
        headers: {
          "Content-Type": "application/json"
        },
        crossOrigin: true,
        type: "json",
        onComplete(dataResp) {
          resolve(dataResp);
        },
        onFailure(error) {
          reject(JSON.stringify(error));
        },
      });
    });
  });
};
const submitAction = async () =>{

  try {
const [year, month, day] = startDate.value.split('-');
startDate.value = `${month}-${day}-${year}`;

const [endYear, endMonth, endDay] = endDate.value.split('-');
endDate.value = `${endMonth}-${endDay}-${endYear}`;
    url.value = await getServiceURL();
    console.log("MKK Service URL initialized:", url.value);
    chartData.value = await sendSimpleRequest(`/CustomService/ca/getCAData?startDate=${startDate.value}&endDate=${endDate.value}&groupBy=${groupby.value}`);
  } catch (error) {
    console.error("Failed to initialize Service URL on mount:", error);
  }
}
const ChartSelectionRequest = async (endpoint, methodType) => {
  return new Promise((resolve, reject) => {
    requirejs(["DS/WAFData/WAFData"], (WAFData) => {
      const apiUrl = `${url.value}${endpoint}`;
      console.log("requirejs loaded WAFData successfully. Target URL is:", apiUrl);
      WAFData.authenticatedRequest(apiUrl, {
        method: methodType,
        timeout: 600000,
        headers: {
          "Content-Type": "application/json"
        },
        crossOrigin: true,
        type: "json",
        onComplete(dataResp) {
          console.log(" WAFData request completed successfully!", dataResp);
          resolve(dataResp);
        },
        onFailure(error) {
          console.error(" WAFData request FAILED on the server!", error);
          reject(JSON.stringify(error));
        },
      });
    });
  });
};
const fetchTableData = async (segmentlabel) => {
  try {
    // 2. Await the promise returned by your utility function
    const response = await ChartSelectionRequest(`/CustomService/ca/getCAS?startDate=${startDate.value}&endDate=${endDate.value}&groupBy=${groupby.value}&groupByValue=${segmentlabel}`);
    tableData.value = response; 
    }
    catch (error) {
      console.error("Authenticated network request failed:", error);
  }
};
const totalValue = computed(() => {
  return chartData.value.reduce((sum, item) => sum + item.value, 0);
});

const segments = computed(() => {
  let currentAngle = -90; 
  const centerX = 100;
  const centerY = 100;
  const outerRadius = 90;
  const innerRadius = 50;
  const labelRadius = 70;


  if (totalValue.value === 0) return [];

  return chartData.value.map(item => {
    const percentage = ((item.value / totalValue.value) * 100).toFixed(1);
    const angleDelta = (item.value / totalValue.value) * 360;
    
    const startAngle = currentAngle;
    const endAngle = currentAngle + angleDelta;
    currentAngle = endAngle;

    const getCoordinates = (radius, angleInDegrees) => {
      const angleInRadians = ((angleInDegrees - 90) * Math.PI) / 180.0;
      return {
        x: centerX + radius * Math.cos(angleInRadians),
        y: centerY + radius * Math.sin(angleInRadians)
      };
    };

    const startOuter = getCoordinates(outerRadius, startAngle);
    const endOuter = getCoordinates(outerRadius, endAngle);
    const startInner = getCoordinates(innerRadius, startAngle);
    const endInner = getCoordinates(innerRadius, endAngle);
    
    const largeArcFlag = angleDelta > 180 ? 1 : 0;

    const pathData = [
      `M ${startOuter.x} ${startOuter.y}`,
      `A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${endOuter.x} ${endOuter.y}`,
      `L ${endInner.x} ${endInner.y}`,
      `A ${innerRadius} ${innerRadius} 0 ${largeArcFlag} 0 ${startInner.x} ${startInner.y}`,
      'Z'
    ].join(' ');

    const midAngle = startAngle + angleDelta / 2;
    const labelCoords = getCoordinates(labelRadius, midAngle);
    const label = item.label;
    return {
      pathData,
      color: item.color,
      percentage,
      labelX: labelCoords.x,
      labelY: labelCoords.y,
      label: label
    };
  });
 });

</script>

<style scoped>
.widget-container {
  width: 100%;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: #f7fafc;
  padding: 16px;
}

.dashboard-title {
  margin-top: 0;
  margin-bottom: 16px;
  color: #1a202c;
  font-weight: 600;
  font-size: 20px;
}

.filters-section, .select-group {
  margin-bottom: 12px;
  background-color: #ffffff;
  padding: 12px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.select-item {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.select-label {
  font-size: 13px;
  font-weight: 500;
  color: #4a5568;
}

.custom-input-style {
  padding: 4px 8px;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  font-size: 13px;
  color: #2d3748;
  background-color: #fff;
  outline: none;
}

/* Flexible content area using flex wrap instead of strict media queries */
.dashboard-flex-layout {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 16px;
  width: 100%;
}

.chart-card {
  flex: 1 1 280px;
  max-width: 100%;
  background-color: #ffffff;
  border-radius: 6px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.table-card {
  flex: 2 1 450px;
  min-width: 0; 
  background-color: #ffffff;
  border-radius: 6px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.chart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 240px;
  margin: 0 auto;
}

.svg-wrapper {
  width: 100%;
  aspect-ratio: 1 / 1;
}

.label-shadow {
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
}

.legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #4a5568;
}

.legend-color {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 4px;
  display: inline-block;
}

.action-btn.blue-btn {
  background-color: #0076df !important;
  color: #ffffff !important;
  border-radius: 4px !important;
  font-weight: 500 !important;
  font-size: 12px !important;
  padding: 0 12px !important;
  height: 28px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: none !important;
  text-transform: none !important;
}

.action-btn.blue-btn:hover {
  background-color: #0060b9 !important;
}

.status-badge {
  display: inline-block;
  padding: 2px 6px;
  font-size: 10px;
  font-weight: 600;
  border: 1px solid;
  border-radius: 12px;
  text-transform: uppercase;
}

.empty-table-state {
  text-align: center;
  color: #718096;
  padding: 24px !important;
  font-style: italic;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.custom-table th {
  background-color: #f7fafc;
  color: #2d3748;
  font-weight: 600;
  font-size: 13px;
  padding: 10px 12px;
  border-bottom: 2px solid #edf2f7;
  border-right: 1px solid #edf2f7;
}

.custom-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #edf2f7;
  border-right: 1px solid #edf2f7;
  color: #2c3e50;
  font-size: 12px;
  line-height: 1.4;
}

.custom-table th:last-child,
.custom-table td:last-child {
  border-right: none;
}

.date-cell {
  white-space: pre-line;
}

.header-content {
  display: flex;
  align-items: center;
}

.header-label {
  display: inline-flex;
  align-items: center;
}
.pointer-events-none {
  pointer-events: none;
}
.clickable-segment {
  cursor: pointer;
}
</style>