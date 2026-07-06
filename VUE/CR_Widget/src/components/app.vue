<template>
  <div class="app-container">
    <h2 class="dashboard-title">Change Request Dashboard</h2>
    <div class="filter-toolbar">   
    <div class="select-group">
        <div class="select-item">
      <span class="select-label">Project:</span>
      <select 
        v-model="tempProject" 
        class="custom-input-style"
         @change="onProjectChange"
      >
        <option 
        v-for="item in data" 
        :key="item" 
        :value="item">
        {{ item }}
        </option>
      </select>
    </div>
        
      <div class="select-item">
        <span class="select-label">Owner:</span>
        <input 
          type="text" 
          v-model="tempOwner" 
          class="custom-input-style" 
          placeholder="Enter Owner"
        />
      </div>
    </div>

      <!-- Right side actions container -->
      <div class="action-group">
        <v-btn class="text-none action-btn blue-btn"
          variant="flat" @click="clearTopFilters"
          size="small">
          Reset Filters
        </v-btn>

<!-- Working Customize Columns Dropdown -->
<div class="menu-button-wrapper" style="position: relative;">
  <button 
    type="button"
    class="text-none action-btn blue-btn"
    @click.stop="showColumnMenu = !showColumnMenu"
    style="display: inline-flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer;"
  >
    <!-- Clean inline configuration icon -->
    <span style="font-size: 14px;">⚙️</span>
    Customize Columns
  </button>

  <!-- Dropdown Menu List -->
  <div 
    v-if="showColumnMenu" 
    class="column-menu-list" 
    v-click-outside="closeColumnMenu"
    style="position: absolute; right: 0; top: 100%; margin-top: 6px; background: #ffffff; border: 1px solid #dcdfe6; border-radius: 4px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); z-index: 999; padding: 6px 0; min-width: 180px;"
  >
    <div 
      v-for="col in allColumns" 
      :key="col.key" 
      style="display: flex; align-items: center; gap: 10px; padding: 8px 16px; transition: background 0.2s;"
      class="column-item-row"
    >
      <input 
        type="checkbox" 
        :id="'col-' + col.key"
        :value="col.key" 
        v-model="visibleColumnKeys"
        style="cursor: pointer; width: 16px; height: 16px; margin: 0;"
      />
      <label 
        :for="'col-' + col.key" 
        style="cursor: pointer; font-size: 14px; color: #333333; user-select: none; flex-grow: 1; text-align: left;"
      >
        {{ col.label }}
      </label>
    </div>
  </div>
</div>

        <v-btn
          class="text-none action-btn blue-btn"
          variant="flat"
          size="small"
          @click="downloadCSV"
        >
          Export CSV
        </v-btn>
      </div>
    </div>
    
    <!-- Datatable Block (Code completely intact and untouched) -->
    <div class="table-container">
      <table class="custom-table">
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key" class="table-header">
              <div class="header-content">
                <!-- Label & Sort Controls -->
                <span class="header-label" @click="toggleSort(column.key)">
                  {{ column.label }}
                  <span class="sort-icon" :class="{ active: sortKey === column.key }">
                    <template v-if="sortKey === column.key">
                      {{ sortOrder === 'asc' ? '↑' : '↓' }}
                    </template>
                    <template v-else>↕</template>
                  </span>
                </span>

                <!-- Filter Toggle Button -->
                <button 
                  class="filter-btn" 
                  :class="{ 'filter-active': filters[column.key] }"
                  @click.stop="toggleFilterDropdown(column.key)"
                >
                  ▼
                </button>

                <!-- Inline Filter Dropdown Input -->
                <div v-if="activeFilterDropdown === column.key" class="filter-dropdown" v-click-outside="closeFilter">
                  <input 
                    v-model="filters[column.key]" 
                    :placeholder="`Filter...`"
                    class="filter-input"
                    ref="filterInput"
                    @keyup.esc="closeFilter"
                  />
                  <button v-if="filters[column.key]" @click="filters[column.key] = ''" class="clear-btn">×</button>
                </div>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in filteredAndSortedData" :key="index">
            <td v-if="visibleColumnKeys.includes('id')">{{ row.id }}</td>
            <td v-if="visibleColumnKeys.includes('title')">{{ row.title }}</td>
            <td v-if="visibleColumnKeys.includes('originated')" class="date-cell">{{ formatDate(row.originated) }}</td>
            <td v-if="visibleColumnKeys.includes('current')">
              <span class="current-badge" :class="row.current.toLowerCase()">
                {{ row.current }}
              </span>
            </td>
            <td v-if="visibleColumnKeys.includes('owner')">{{ row.owner }}</td>
          </tr>
          <tr v-if="filteredAndSortedData.length === 0">
            <td :colspan="columns.length" class="no-data">No matching records found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue';
const url = ref('');
const data = ref([]);
// 1. Master Column Blueprint Configuration
const allColumns = [
  { key: 'id', label: 'ID' },
  { key: 'title', label: 'CR Title' },
  { key: 'originated', label: 'Creation Date' },
  { key: 'current', label: 'Status' },
  { key: 'owner', label: 'Owner' }
];

// Tracking visible column keys dynamically
const visibleColumnKeys = ref(['id', 'title', 'originated', 'current','owner']);

// Computed columns feeding into the header tracking loop
const columns = computed(() => {
  return allColumns.filter(col => visibleColumnKeys.value.includes(col.key));
});

// 2. Sample Data
const CRData = ref([]);

// 3. State Management
const showColumnMenu = ref(false)
const sortKey = ref('');
const sortOrder = ref('asc'); 
const activeFilterDropdown = ref(null);
const filterInput = ref(null);
const filters = ref({
  id: '',
  title: '',
  originated: '',
  current: '',
  owner: ''
});

// Top bar models
const tempProject = ref(null);
const tempOwner = ref(null);

const clearTopFilters = () => {
  tempProject.value = null;
  tempOwner.value = null;
};

// 5. Sorting Logic
const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

// 6. Filter Dropdown Controls
const toggleFilterDropdown = async (key) => {
  if (activeFilterDropdown.value === key) {
    activeFilterDropdown.value = null;
  } else {
    activeFilterDropdown.value = key;
    await nextTick();
    if (filterInput.value && filterInput.value[0]) {
      filterInput.value[0].focus();
    }
  }
};

const closeFilter = () => {
  activeFilterDropdown.value = null;
};

// ADDED: Customize Column Menu Close Handler Logic
const closeColumnMenu = () => {
  showColumnMenu.value = false;
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

// 7. Date Formatting
const formatDate = (dateString) => {
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString;

  const options = {
    month: 'numeric',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  };
  
  return date.toLocaleString('en-US', options).replace(',', '');
};

// 8. Combined Filter & Sort Computational Engine
const filteredAndSortedData = computed(() => {
  let result = [...CRData.value];
  if (tempOwner.value) {
    result = result.filter((row) => 
      String(row.owner).toLowerCase().includes(tempOwner.value.toLowerCase())
    );
  }

  // Apply column-specific inline string filters
  Object.keys(filters.value).forEach((key) => {
    const filterValue = filters.value[key].toLowerCase().trim();
    if (filterValue) {
      result = result.filter((row) => {
        if (key === 'originated') {
          return formatDate(row[key]).toLowerCase().includes(filterValue);
        }
        return String(row[key]).toLowerCase().includes(filterValue);
      });
    }
  });

  // Apply sorting rules
  if (sortKey.value) {
    result.sort((a, b) => {
      let modifier = sortOrder.value === 'asc' ? 1 : -1;
      let valA = a[sortKey.value];
      let valB = b[sortKey.value];

      if (sortKey.value === 'originated') {
        valA = new Date(valA).getTime();
        valB = new Date(valB).getTime();
      } else {
        valA = String(valA).toLowerCase();
        valB = String(valB).toLowerCase();
      }

      if (valA < valB) return -1 * modifier;
      if (valA > valB) return 1 * modifier;
      return 0;
    });
  }

  return result;
});

// UPDATED: Added safety target exception wrapper check for .menu-button-wrapper 
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(
        el === event.target || 
        el.contains(event.target) || 
        event.target.classList.contains('filter-btn') ||
        event.target.closest('.menu-button-wrapper')
      )) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  }
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

const ProjectSelectionRequest = async (endpoint, methodType) => {
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
onMounted(async () => {
  try {
    url.value = await getServiceURL();
    console.log("MKK Service URL initialized:", url.value);
    data.value = await sendSimpleRequest("/CustomService/cr/getProjects");
    console.log("MKK Project Data:", data);
  } catch (error) {
    console.error("Failed to initialize Service URL on mount:", error);
  }
});
const onProjectChange = async () => {
  try {
    console.log(`Launching authenticated WAFData request for: ${tempProject.value}`);
    // 2. Await the promise returned by your utility function
    const response = await ProjectSelectionRequest(`/CustomService/cr/getCRS?project=${tempProject.value}`); 
    // 3. Update your local state with the returned data
    console.log("MKK WAFData response received successfully:", response);
    console.log("MKK Original CRData.value:", CRData.value);
    CRData.value = response; 
    console.log("MKK Updated CRData.value:", CRData.value);
  } catch (error) {
    console.error("Authenticated network request failed:", error);
  }
};
const downloadCSV = () => {
  if (CRData.value.length === 0) return;

  // 1. Extract headers dynamically from the first item keys
  const headers = Object.keys(CRData.value[0]);
  
  // 2. Map row data and handle instances where comma values might break formatting
  const rows = CRData.value.map(row => 
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
.app-container {
  padding: 24px;
  max-width: 100%;
  margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.dashboard-title {
  margin-bottom: 24px;
  color: #333;
  font-weight: 500;
}

/* Base structural row wrapper layout matching second layout of */
.filter-toolbar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 12px 16px;
  border-radius: 6px 6px 0 0;
  border: 1px solid #e0e0e0;
  border-bottom: none;
  width: 100%;
  box-sizing: border-box;
}

.select-group {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-shrink: 0;
}

.select-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.select-label {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  white-space: nowrap;
}

/* Anti-collapse structural rules forcing inputs to remain fully visible */
.custom-input-style {
  width: 240px !important;
  min-width: 240px !important;
  max-width: 240px !important;
  display: inline-block !important;
}

/* Actions formatting */
.action-group {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
}

.menu-button-wrapper {
  display: inline-block;
}

/* Unified clean crisp blue action buttons */
.action-btn.blue-btn {
  background-color: #0076df !important;
  color: #ffffff !important;
  border-radius: 4px !important;
  font-weight: 500 !important;
  font-size: 13px !important;
  padding: 10px !important;
  /* height: 36px !important; */
  line-height: 1 !important;
  align-items: center !important;
  text-align: center !important;
  box-shadow: none !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

.action-btn.blue-btn:hover {
  background-color: #0060b9 !important;
}

.column-menu-list {
  padding: 4px 8px;
  background-color: white;
  min-width: 180px;
}

/* Table Layout Base (Kept intact and completely unaltered) */
.table-container {
  width: 100%;
  overflow-x: auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  border-radius: 0 0 4px 4px;
  border: 1px solid #e0e0e0;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background-color: #ffffff;
}

.custom-table th {
  background-color: #f2f2f2;
  color: #000000;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 12px;
  border-bottom: 2px solid #dcdcdc;
  border-right: 1px solid #e0e0e0;
  position: relative;
  user-select: none;
}

.custom-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  border-right: 1px solid #e0e0e0;
  color: #2c3e50;
  font-size: 13px;
  line-height: 1.4;
  vertical-align: top;
}

.custom-table th:last-child,
.custom-table td:last-child {
  border-right: none;
}

.date-cell {
  white-space: pre-line;
  max-width: 130px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-label {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-grow: 1;
}

.sort-icon {
  font-size: 11px;
  color: #888;
}

.sort-icon.active {
  color: #2196F3;
  font-weight: bold;
}

.filter-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 11px;
  color: #000000;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-active {
  color: #2196F3;
}

.filter-dropdown {
  position: absolute;
  top: 100%;
  right: 4px;
  z-index: 10;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 6px;
  display: flex;
  align-items: center;
  box-shadow: 0 3px 6px rgba(0,0,0,0.12);
}

.filter-input {
  border: 1px solid #ccc;
  padding: 4px 6px;
  font-size: 12px;
  border-radius: 3px;
  outline: none;
  width: 130px;
}

.filter-input:focus {
  border-color: #2196F3;
}

.clear-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  font-size: 14px;
  margin-left: -20px;
  padding: 0 4px;
}

.no-data {
  text-align: center;
  color: #888;
  padding: 24px !important;
}

.current-badge {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}
</style>