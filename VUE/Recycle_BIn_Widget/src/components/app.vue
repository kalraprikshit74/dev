<template>
  <div class="app-container">
     <div class="table-card">      
      <div class="windows-container">
      <div class="action-bar">
        <button class="delete" @click="handleDelete" title="Delete">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 7h16" />
          <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2l1-12" />
          <path d="M9 7V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v3" />
          <path d="M10 11v6" />
          <path d="M14 11v6" />
        </svg>
      </button>

      <!-- Restore Button -->
      <button class="restore" @click="handleRestore" title="Restore">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 14L4 9l5-5" />
          <path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5v0a5.5 5.5 0 0 1-5.5 5.5H11" />
        </svg>
      </button>
    </div>
    </div>
          <div class="table-container" id="drop">
        <table class="custom-table">
          <thead>
            <tr>
              <th class="checkbox-col">
                <input 
                  type="checkbox" 
                  :checked="isAllSelected" 
                  @change="toggleSelectAll" 
                  class="custom-checkbox"
                />
              </th>
              <th v-for="header in headers" :key="header.key">
                <div class="header-content">
                  <span class="header-label">{{ header.label }}</span>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-for="row in tableData" :key="row.id || row.physicalid">
              <!-- Main Row -->
              <tr :class="{ 'selected-row': selectedRows.includes(row.id || row.physicalid) }">
                <!-- Row Checkbox Selection -->
                <td class="height">
                  <input 
                    type="checkbox" 
                    v-model="selectedRows" 
                    :value="row.physicalid"
                    class="custom-checkbox"
                  />
                </td>

                <!-- Dynamic columns mapping row property directly to header keys -->
                <td v-for="header in headers" :key="header.key" class="p-4">
                  <!-- Expand/Collapse Button placed in the Title column -->
                  <span v-if="header.label === 'Title'" class="expand-toggle-container">
                    <button 
                      @click.stop="toggleExpand(row)" 
                      class="toggle-btn"
                    >
                      {{ row.loading ? '...' : (row.expanded ? '-' : '+') }}
                    </button>
                  </span>

                  {{ row[header.key] !== undefined ? row[header.key] : '-' }}
                </td>
              </tr>

        <TableRow
          v-for="row in row.children"
          :key="row.physicalid"
          :row="child"
          :headers="headers"
          :depth="0"
          v-model:selected-rows="selectedRows"
          :toggle-expand="toggleExpand"
        />
          </template>
          </tbody>
        </table>
      </div>
    </div>

  </div>
    
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue';
const SecurityContext=ref('');
const url = ref('');
const headers = ref([
  { key: 'attribute[PLMEntity.V_Name]', label: 'Title' },
  { key: 'type', label: 'Type' },
  { key: 'name', label: 'Name' },
  { key: 'revision', label: 'Revision' },
  { key: 'current', label: 'Current' },

]);
const selectedRows = ref([])
const tableData = ref([])
const childrenData = ref([])

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
const sendSimpleRequest = async (url2,Type)=> {
            const apiUrl =url.value+url2;
            return new Promise((resolve, reject) => {
            requirejs( ["DS/WAFData/WAFData"], function (WAFData) {
              WAFData.authenticatedRequest(apiUrl, {
                  method: Type,
                  timeout: 600000,
                  headers: {
                    "Content-Type": "application/json",
                    SecurityContext: SecurityContext.value,
                  },
                  crossOrigin: true,
                  type: "json",
                  onComplete (dataResp) {
                    resolve(dataResp);
                  },
                  onFailure (error) {
                    reject(JSON.stringify(error));
                  },
                });
              });
            } );
          };
  onMounted(async () => {
    url.value = await getServiceURL();
    console.log("inside mounted")
    const sc = await sendSimpleRequest("/resources/pno/person/getsecuritycontext","GET");
    SecurityContext.value = sc.SecurityContext;
    console.log("after sc")

    requirejs(["DS/DataDragAndDrop/DataDragAndDrop"],
      function (DataDragAndDrop) {
      let elem = document.getElementById("drop");
      console.log("called drop")
    DataDragAndDrop.droppable(elem, {
      drop: function(data) {
        console.log("Raw drop data:", data);

        let parsedPayload;
        try {
          // Safeguard: Handles cases where data is either a string or already an object
          parsedPayload = typeof data === 'string' ? JSON.parse(data) : data;
        } catch (e) {
          console.error("Failed to parse dropped data:", e);
          return;
        }
          
        // 2. Validate the 3DXContent protocol structure
        if (parsedPayload && parsedPayload.protocol === '3DXContent' && parsedPayload.data && parsedPayload.data.items) {
          const ids = [];
          // 3. Loop through incoming items and map them to your table structure
          parsedPayload.data.items.forEach(item => {
            ids.push(item.objectId);
            
          });
          ondrop(ids.join(','));
        } 
      },

    });
  });
});
const showBottomNotification = (message) => {
  // Check if a notification already exists, remove it
  const existingToast = document.getElementById('bottom-toast');
  if (existingToast) existingToast.remove();

  // Create toast element
  const toast = document.createElement('div');
  toast.id = 'bottom-toast';
  toast.innerText = message;
  
  // Style it to look like a popup at the bottom center
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    backgroundColor: '#edf6eb',
    color: '#334155',
    padding: '10px 20px',
    borderRadius: '4px',
    zIndex: '9999',
    fontSize: '14px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
    transition: 'opacity 0.3s ease'
  });

  document.body.appendChild(toast);

  // Automatically remove after 3 seconds
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
};

widget.addEvent("onRefresh", async() => {
  try {
          url.value = await getServiceURL();
          console.log("its ready..")
          console.log("MKK Service URL initialized:", url.value);
          const data = await sendSimpleRequest("/CustomService/custom/getMyRecycleBin?type=VPMReference");
          console.log("MKK Project Data:", data);
          tableData.value=data;
          console.log("tabledata is here:",tableData.value);
        } catch (error) {
          console.error("Failed to initialize Service URL on mount:", error);
        }
});
onMounted(async () => {
        try {
          url.value = await getServiceURL();
          console.log("its ready..")
          console.log("MKK Service URL initialized:", url.value);
          const data = await sendSimpleRequest("/CustomService/custom/getMyRecycleBin?type=VPMReference");
          console.log("MKK Project Data:", data);
          tableData.value=data;
          console.log("tabledata is here:",tableData.value);
        } catch (error) {
          console.error("Failed to initialize Service URL on mount:", error);
        }
});
const ondrop = async (physicalid) => {
  try {
      
    console.log(`Launching authenticated WAFData request for`);
    
        const includeChildren = await showDeleteConfirmationToast();
        console.log("Delete children selected:", includeChildren);
        // 2. Await the promise returned by your utility function
        await sendSimpleRequest(`/CustomService/custom/delete?ids=${physicalid}&deletechild=${includeChildren}`,'DELETE'); 
        // 3. Update your local state with the returned data
        console.log("MKK WAFData request send ");
        const data = await sendSimpleRequest("/CustomService/custom/getMyRecycleBin?type=VPMReference");
          console.log("MKK Project Data:", data);
          tableData.value=data;
          console.log("tabledata is here:",tableData.value);
  } catch (error) {
    console.error("Authenticated network request failed:", error);
  }
};
function showDeleteConfirmationToast() {
  return new Promise((resolve) => {
    const existingToast = document.getElementById('bottom-toast');
    if (existingToast) existingToast.remove();

    const toast = document.createElement('div');
    toast.id = 'bottom-toast';

    toast.innerHTML = `
      <div style="margin-bottom: 12px; text-align: center;">Do you also want to delete its Structure</div>
      <div style="display: flex; justify-content: center; gap: 12px;">
        <button id="toast-yes-btn" style="
          background-color: #2e7d32; 
          color: white; 
          border: none; 
          padding: 6px 14px; 
          border-radius: 4px; 
          cursor: pointer; 
          display: flex; 
          align-items: center; 
          gap: 6px;
          font-size: 13px;
        ">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          Yes
        </button>
        
        <button id="toast-no-btn" style="
          background-color: #c62828; 
          color: white; 
          border: none; 
          padding: 6px 14px; 
          border-radius: 4px; 
          cursor: pointer; 
          display: flex; 
          align-items: center; 
          gap: 6px;
          font-size: 13px;
        ">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
          No
        </button>
      </div>
    `;

    Object.assign(toast.style, {
      position: 'fixed',
      bottom: '20px',
      left: '50%',
      transform: 'translateX(-50%)',
      backgroundColor: '#edf6eb',
      color: '#424141',
      padding: '16px 20px',
      borderRadius: '6px',
      zIndex: '9999',
      fontSize: '14px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
      transition: 'opacity 0.3s ease',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    });

    document.body.appendChild(toast);

    document.getElementById('toast-yes-btn').addEventListener('click', () => {
      toast.remove();
      resolve(true);
    });

    document.getElementById('toast-no-btn').addEventListener('click', () => {
      toast.remove();
      resolve(false);
    });
  });
};
const handleDelete = async () => {
   try {
    console.log(`deleting it permanently`);
    console.log(selectedRows.value);
    // 2. Await the promise returned by your utility function
     await sendSimpleRequest(`/CustomService/custom/permanentlydelete?ids=${selectedRows.value}`,'DELETE'); 
    // 3. Update your local state with the returned data
    console.log("its permanently deleted");
    showBottomNotification("Item(s) deleted");
    const data = await sendSimpleRequest("/CustomService/custom/getMyRecycleBin?type=VPMReference");
    console.log("MKK Project Data:", data);
    tableData.value=data;
  } catch (error) {
    console.error("Authenticated network request failed:", error);
  }
};
const toggleSelectAll = (e) => {
  if (e.target.checked) {
    selectedRows.value = tableData.value.map(row => row.physicalid)
  } else {
    selectedRows.value = []
  }
}

const toggleExpand = async (row) => {
    if (row.expanded) {
    row.expanded = false;
    return;
  }
    try {
      row.loading = true;
      console.log("Fetching children for ID:", row.physicalid);
      const response = await sendSimpleRequest(`/CustomService/custom/getChildren?id=${row.physicalid}`)  
      
      row.children =  response;
      
    } catch (error) {
      console.error("Failed to load child items:", error);
      return;
    } finally {
      row.loading = false;
    }
  

  // Trigger expansion
  row.expanded = true;
  console.log("row is expanded");
}

const handleRestore = async () => {
   try {
    console.log(selectedRows.value);
    // 2. Await the promise returned by your utility function
     await sendSimpleRequest(`/CustomService/custom/recycle?ids=${selectedRows.value}`); 
    // 3. Update your local state with the returned data
    const data = await sendSimpleRequest("/CustomService/custom/getMyRecycleBin?type=VPMReference");
    console.log("MKK Project Data:", data);
    showBottomNotification("Item(s) restored");
    tableData.value=data;
  } catch (error) {
    console.error("Authenticated network request failed:", error);
  }
}

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

/* Main Container Styling */
.recycle-bin-wrapper {
  max-width: 1100px;
  margin: 4px auto;
  padding: 0 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #334155;
  background-color: #f8fafc;
  min-height: 100vh;
}
.empty-state-cell {
  height: 250px; 
  text-align: center;
  background-color: #e59393;
}

.empty-state-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #555555;
  font-size: 20px;
  font-weight: 600;
}
.toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  font-size: 12px;
  font-weight: bold;
  line-height: 1;
  background-color: #ffffff;
  border: 1px solid #cccccc; /* Default box border */
  border-radius: 2px;
  cursor: pointer;
  margin-right: 6px;
  user-select: none;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

/* Black border on hover for the expand/collapse box */
.toggle-btn:hover {
  border-color: #000000 !important;
  background-color: #f9f9f9;
}

.toggle-btn:focus {
  outline: none;
  border-color: #000000;
}

/* Indentation and Tree alignment for child rows */
.child-row-cell {
  position: relative;
}

.child-indent {
  display: inline-flex;
  align-items: center;
  margin-left: 20px; /* Indentation offset for hierarchy */
  position: relative;
}

/* Optional vertical tree connector line */
.child-indent::before {
  content: '';
  position: absolute;
  left: -12px;
  top: -16px;
  bottom: 50%;
  width: 1px;
  background-color: #cbd5e1;
}

.child-indent::after {
  content: '';
  position: absolute;
  left: -12px;
  top: 50%;
  width: 10px;
  height: 1px;
  background-color: #cbd5e1;
}
 /* .height{
  height: 100%;
}  */
/* Drag and Drop Zone */
.drop-zone {
  height: 100vh;
  border: 2px dashed #cbd5e1;
  background-color: #ffffff;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.2s ease-in-out;
  margin-bottom: 24px;
  cursor: pointer;
}

.drop-zone:hover {
  border-color: #6366f1;
  background-color: #fafaff;
}

.drop-zone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.drop-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #e0e7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.drop-zone:hover .drop-icon-wrapper {
  transform: scale(1.08);
}

.drop-svg {
  width: 24px;
  height: 24px;
  color: #4f46e5;
}

.drop-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.drop-subtitle {
  font-size: 12px;
  color: #64748b;
  margin: 2px 0 0 0;
}

/* Table Card Layout */
.table-card {
  background: #ffffff;
  border-radius: 0px;
  box-shadow: none;
  border: 1px solid #cbd5e1;
  overflow: hidden;
}

/* Windows Container Header Header Section */
.windows-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
  background-color: #ffffff;
}

.dashboard-title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.025em;
  margin: 0;
}

/* Action Bar Buttons */
.action-bar {
  display: flex;
  gap: 8px;
  margin-left: 15px;
}


.win-btn.delete {
  background-color: #fff1f2;
  margin: 3px;
}


.restore {
  background-color: #ecfdf5;
  margin: 3px;
}

/* Table Container & Custom Styling */
.table-container {
  width: 100%;
  overflow-x: auto;
  height: 100vh;
  overflow-x: scroll;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.custom-table th {
  background-color: #eef2f6;
  border-bottom: 1px solid #cbd5e1;
  border-right: 1px solid #cbd5e1;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 500;
  color: #1e293b;
  text-transform: none;
  letter-spacing: normal;
}

.custom-table td {
  padding: 16px 20px;
  font-size: 14px;
  color: #334155;
  border-bottom: 1px solid #f1f5f9;
}

.custom-table tbody tr {
  transition: background-color 0.15s ease;
}

.custom-table tbody tr:hover {
  background-color: #f8fafc;
}

.custom-table tr.selected-row {
  background-color: #eef2ff !important;
}

/* Checkbox Column Settings */
.checkbox-col {
  width: 36px;
  text-align: center;
  background-color: #ededed; /* Matched to the solid light-grey sidebar column color from the reference */
  border-bottom: 1px solid #cbd5e1;
  border-right: 1px solid #cbd5e1;
}

/* Target table cells in the checkbox column to match the same sidebar color */
.custom-table td.checkbox-col,
.custom-table td:first-child {
  background-color: #eef2f6;
  border-right: 1px solid #cbd5e1;
}

.custom-checkbox {
  width: 14px;
  height: 14px;
  accent-color: #4f46e5;
  cursor: pointer;
  border-radius: 2px;
}

/* Empty State Handling */
.empty-state {
  text-align: center;
  padding: 120px 20px;
  color: #64748b;
  font-style: normal;
  font-weight: 600;
  font-size: 24px;
  background-color: #e59393;
}
.tree-cell-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  padding-left: 20px; /* Adjust spacing for the tree branch */
}

/* Vertical and horizontal branch connector lines */
.tree-cell-wrapper::before {
  content: "";
  position: absolute;
  left: 8px;
  top: -20px; /* Connects upward to parent row */
  bottom: 50%; /* Stops halfway to form the L-shape */
  width: 1px;
  border-left: 1px solid #b0b0b0;
}

.tree-cell-wrapper::after {
  content: "";
  position: absolute;
  left: 8px;
  top: 50%;
  width: 12px;
  border-bottom: 1px solid #b0b0b0;
}

/* Optional spacing class if needed */
.child-indent {
  margin-right: 6px;
}
/* --- Toggle Button Styling & Black Hover Border --- */
.toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  font-size: 12px;
  font-weight: bold;
  line-height: 1;
  background-color: #ffffff;
  border: 1px solid #cccccc;
  border-radius: 2px;
  cursor: pointer;
  margin-right: 6px;
  user-select: none;
  transition: border-color 0.2s ease, background-color 0.2s ease;
  vertical-align: middle;
}

/* Black border on hover for the expand sign box */
.toggle-btn:hover {
  border-color: #000000 !important;
  background-color: #f9f9f9;
}

.toggle-btn:focus {
  outline: none;
  border-color: #000000;
}

/* --- Tree Hierarchy Styling --- */
.tree-cell-wrapper {
  display: inline-flex;
  align-items: center;
  position: relative;
}

.child-indent {
  display: inline-block;
  width: 16px;
}

.tree-line {
  position: relative;
  display: inline-block;
  width: 10px;
  height: 12px;
  margin-right: 4px;
  border-left: 1px solid #b0b0b0;
  border-bottom: 1px solid #b0b0b0;
  vertical-align: middle;
}
</style>