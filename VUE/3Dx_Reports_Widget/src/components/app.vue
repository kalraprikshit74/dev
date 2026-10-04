<template>
  <div class="app-container">
    <h2 class="dashboard-title">3DEXPERIENCE Report</h2>
    
    <!-- Top Controls Row -->
    <div class="filter-toolbar">   
      <div class="control-box">
        <label>Type</label>
        <select 
          v-model="selectedType"
        >
          <option value="VPMReference">VPMReference</option>
          <option value="Document">Document</option>
          <option value="Part">Part</option>
        </select>
      </div>

      <div class="control-box">
        <label>Year</label>
        <input 
          type="number" 
          v-model="selectedYear" 
        >
      </div>

      <div class="control-box">
        <label>Slice</label>
        <select 
          v-model="selectedSlice" 
        >
          <option value="Monthly">Monthly</option>
          <option value="Quarterly">Quarterly</option>
        </select>
      </div>

      <div class="control-box">
        <label>Group By</label>
        <select 
          v-model="selectedGroupBy" 
        >
          <option value="current">Status</option>
        </select>
      </div>

      <!-- Actions -->
      <button 
        class="action-btn blue-btn" 
        @click="fetchReport"
      >
        GENERATE REPORT
      </button>

      <button
        class="action-btn green-btn"
        @click="downloadCSV"
      >
        EXPORT TO EXCEL
      </button>
    </div>

    <!-- Data Table / Empty State Block -->
    <div v-if="Object.keys(tableData).length > 0" class="table-container scrollable-table-container">
      <table class="custom-table">
        <thead>
          <tr>
            <th><div class="header-content"><span class="header-label">{{ selectedSlice === 'Monthly' ? 'Month' : 'Quarter' }}</span>
              </div>
            </th>
            <th v-for="state in dynamicStates" :key="state">
              <div class="header-content"><span class="header-label">{{state}}</span></div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rowKey in rowLabels" :key="rowKey">
          <td class="month-col">{{ rowKey }}</td>
          
          <!-- Fetch the count for each state, defaulting to 0 -->
          <td v-for="state in dynamicStates" :key="state" :class="{ 'clickable-cell': getCount(rowKey, state) > 0 }"
              @click="handleCellClick(formatRowKey(rowKey), state)">
            {{ getCount(rowKey, state) }}
          </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-data-message">
      <p>No data available for the selected view.</p>
    </div>
    <!-- Add this right before </template> -->
<div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
  <div class="modal-content">
    
    <!-- Modal Header matching your image -->
    <div class="modal-header">
      <h3 class="modal-title">Detail Report</h3>
      <div class="modal-actions">
        <button class="btn-export" @click="exportDetailsToExcel">
          EXPORT DETAILS TO EXCEL
        </button>
        <button class="btn-close" @click="closeModal">×</button>
      </div>
    </div>

    <div class="modal-body">
      <table class="detail-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Type</th>
            <th>Revision</th>
            <th>Physical ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in CellData" :key="index">
            <td>{{ item.name }}</td>
            <td>{{ item.description }}</td>
            <td>{{ item.type }}</td>
            <td>{{ item.revision }}</td>
            <td>{{ item.physicalid }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
  </div>
</div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue';

// State refs for your controls
const url = ref('');
const tableData = ref({});
const CellData = ref([])
const isModalOpen = ref(false);
// 2. Static array to guarantee all months appear as rows
const allMonths = [
  "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
  "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
];
const allQuarters = ["Q1", "Q2", "Q3", "Q4"];
const rowLabels = computed(() => {
  return selectedSlice.value === 'Quarterly' ? allQuarters : allMonths;
});
const dynamicStates = computed(() => {
  const stateSet = new Set();
    console.log(`TAbleData: ${tableData.value}`);
  Object.values(tableData.value).forEach(periodData => {
    console.log(`PeriodData: ${periodData.value}`);
    Object.keys(periodData).forEach(state => {
      console.log(`state: ${state}`);
      stateSet.add(state);
    });
  });
  
  return Array.from(stateSet); // Returns: ['IN_WORK', 'Exists', 'FROZEN']
});
function formatRowKey(rowKey) {
  const monthIndex = allMonths.indexOf(rowKey);
  if (monthIndex !== -1) {
    return monthIndex + 1; // Returns 1-12 for months
  }
  return rowKey;
}
const getCount = (rowKey, state) => {
  console.log("Looking for rowKey:", rowKey);
  console.log("What is inside tableData?:", tableData.value);
  console.log("What is inside tableData?:", state);
  // If the month exists in our data and has the state, return the count. Otherwise, 0.
  return tableData.value[rowKey]?.[state] || 0;
};
// Form models
const selectedType = ref('VPMReference');
const selectedYear = ref(2025);
const selectedSlice = ref('Monthly','Quaterly');
const selectedGroupBy = ref('current');

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
          console.error(`Error: ${JSON.stringify(error)}`);
          reject(error);
        },
      });
    });
  });
};

const sendSimpleRequest = async (endpoint, methodType) => {
  return new Promise((resolve, reject) => {
    requirejs(["DS/WAFData/WAFData"], (WAFData) => {
      const apiUrl = `${url.value}${endpoint}`;
      console.log(`API URL: ${apiUrl}`);
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

onMounted(async () => {
});
const fetchReport = async () => {
  try {
    url.value = await getServiceURL();
    console.log("MKK Service URL initialized:", url.value);
    const responseData = await sendSimpleRequest(`/CustomService/custom/getReportData?type=${selectedType.value}&year=${selectedYear.value}&groupBy=${selectedGroupBy.value}&slice=${selectedSlice.value}`, "GET");
    tableData.value = responseData || {};
    console.log(`responseData: ${responseData}`);
      console.log(`tableDAta: ${tableData.value}`);
  } catch (error) {
    console.error("Failed to initialize Service URL on mount:", error);
  }
};
const CellSelectionRequest = async (endpoint, methodType) => {
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
const handleCellClick = async (rowValue,state) => {
  try {
    isModalOpen.value = true;
    // 2. Await the promise returned by your utility function
    const response = await CellSelectionRequest(`/CustomService/custom/getCellData?type=${selectedType.value}&year=${selectedYear.value}&groupBy=${selectedGroupBy.value}&slice=${selectedSlice.value}&month=${rowValue}&groupval=${state}`); 
    // 3. Update your local state with the returned data
    CellData.value = response; 
  } catch (error) {
    console.error("Authenticated network request failed:", error);
  }
};
const closeModal = () => {
  isModalOpen.value = false;
  modalData.value = []; 
};

const downloadCSV = () => {
  // 1. Guard clause: Stop if there is NO data
  const data = tableData.value || {};
  if (Object.keys(data).length === 0) return;

  // 2. Build the Headers row
  // Example: ["Month", "IN_WORK", "Exists", "FROZEN"]
  const firstColHeader = selectedSlice.value === 'Monthly' ? 'Month' : 'Quarter';
  const headers = [firstColHeader, ...dynamicStates.value];

  // 3. Build the Data rows
  const rows = rowLabels.value.map(rowKey => {
    // Start the row with the Month/Quarter name
    const rowValues = [rowKey];
    
    // Get the exact count for each state column
    dynamicStates.value.forEach(state => {
      rowValues.push(getCount(rowKey, state));
    });

    // Apply the CSV formatting rules you provided
    return rowValues.map(value => {
      const stringified = String(value === null || value === undefined ? '' : value).replace(/"/g, '""');
      return stringified.includes(',') ? `"${stringified}"` : stringified;
    }).join(',');
  });

  // 4. Combine headers and rows into a single string with line breaks
  const csvContent = [headers.join(','), ...rows].join('\n');

  // 5. Trigger the actual file download in the browser
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', `${selectedSlice.value}_report.csv`); // names file "month_report.csv"
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
const exportDetailsToExcel = () => {
  if (CellData.value.length === 0) return;

  // 1. Extract headers dynamically from the first item keys
  const headers = Object.keys(CellData.value[0]);
  
  // 2. Map row data and handle instances where comma values might break formatting
  const rows = CellData.value.map(row => 
    headers.map(fieldName => {
      const value = row[fieldName] === null || row[fieldName] === undefined ? '' : row[fieldName];
      // Escape inner quotes and wrap text in double quotes if commas exist
      const stringified = String(value).replace(/"/g, '""');
      return stringified.includes(',') ? `"${stringified}"` : stringified;
    }).join(',')
  );

  // 3. Combine header and rows into a single string separated by newlines
  const csvContent = [headers.join(','), ...rows].join('\r\n');

  // 4. Create a Blob and trigger an automated download link
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  
  link.setAttribute('href', url);
  link.setAttribute('download', 'exported_data.csv');
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style scoped>
*{
  font-size: 15px;
 }
.app-container {
  padding: 24px;
  max-width: 100%;
  margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.dashboard-title {
  margin-bottom: 24px;
  color: #222;
  font-weight: 700;
  font-size: 24px;
}

/* Toolbar styling mapped to the image */
.filter-toolbar {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}
/* --- Modal Overlay --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensures it sits above everything */
}

/* --- Modal Container --- */
.modal-content {
  background-color: #fff;
  width: 90%;
  max-width: 1000px;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  font-family: sans-serif;
}

/* --- Modal Header --- */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: normal;
  color: #333;
}

.modal-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* --- Green Export Button --- */
.btn-export {
  background-color: #5cb85c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 3px;
  font-weight: bold;
  font-size: 12px;
  cursor: pointer;
  letter-spacing: 0.5px;
}

.btn-export:hover {
  background-color: #4cae4c;
}

/* --- Round Close Button --- */
.btn-close {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #555;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.btn-close:hover {
  background-color: #f9f9f9;
}

/* --- Detail Table (Inside Modal) --- */
.modal-body {
  padding: 20px;
  overflow-x: auto;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.detail-table th, .detail-table td {
  border: 1px solid #ddd;
  padding: 12px 16px;
  text-align: left;
}

.detail-table th {
  background-color: #ffffff;
  font-weight: normal;
  color: #333;
}

/* Gray input boxes with top labels */
.control-box {
  display: flex;
  flex-direction: column;
  background-color: #f7f7f7;
  border-bottom: 2px solid #e0e0e0;
  padding: 6px 12px;
  border-radius: 4px 4px 0 0;
  min-width: 150px;
}
.control-box:hover{
  border-bottom: #000000;
  background-color:  #d4d4d4;
}


.control-box label {
  font-size: 12px;
  color: #777;
  margin-bottom: 2px;
}
/* 3. New styling to make active cells look clickable */
.clickable-cell {
  color: #087cf8c4 !important;
  cursor: pointer;
  text-decoration: underline;
  font-weight: bold;
}

/* Optional: Make it light up differently when you hover over a specific clickable cell */
.clickable-cell:hover {
  background-color: #e6f2ff !important; 
  color: #0056b3;
}
.control-box select, 
.control-box input {
  background: transparent;
  border: none;
  font-size: 15px;
  color: #333;
  outline: none;
  cursor: pointer;
  padding: 2px 0;
}

.control-box input[type="number"] {
  cursor: text;
}
.scrollable-table-container {
  max-height: 300px; /* Adjust this to your preferred table height */
  overflow: auto;    /* Enables both vertical and horizontal scrolling */
  margin: 20px 0;
  border: 1px solid #ddd;
}
.sticky-top-left {
  position: sticky;
  top: 0;
  left: 0;
  z-index: 3; /* Highest priority */
  text-align: left;
  background-color: #f4f4f4;
  box-shadow: 1px 1px 0 #ddd;
}
/* Action Buttons */
.action-btn {
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  padding: 12px 20px;
  border: none;
  cursor: pointer;
  text-transform: uppercase;
  transition: opacity 0.2s;
  height: 48px; /* Match height of input boxes */
}
.no-data-message{
  font-size: 17px;
  opacity: 0.8;
  color: #999;
  text-align: center;
}
.action-btn:hover {
  opacity: 0.9;
  box-shadow: 0px 8px 6px -6px #1565c0;
}

.blue-btn {
  background-color: #1565c0;
  color: #ffffff;
}

.green-btn {
  background-color: #a5d6a7; 
  color: #ffffff;
}

.green-btn:hover {
  opacity: 1.5;
  box-shadow: 0px 8px 6px -6px #a5d6a7;
}

/* Empty State / No Data text */
.empty-state {
  text-align: center;
  color: #999;
  font-size: 18px;
  margin-top: 40px;
}

/* Table styles (preserved but detached from toolbar) */
.table-container {
  width: 100%;
  overflow-x: auto;
  overflow: auto !important;
  border-top: 1px solid #e0e0e0;
  padding-top: 20px;
}

.custom-table {
  width: 100%;
  overflow: auto;
  overflow-x: auto;
  border-collapse: collapse;
  text-align: left;
  background-color: #ffffff;
}

.custom-table th {
  color: #000000;
  font-weight: 600;
  font-size: 17px;
  padding: 10px 10px;
  border: 2px solid #dcdcdc;
}

.custom-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  color: #2c3e50;
  font-size: 13px;
  vertical-align: top;
}
/* 
.date-cell {
  white-space: pre-line;
} */
</style>