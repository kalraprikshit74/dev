<template>
  <div class="app-container">
     <div class="table-card">      
      <div class="plm-toolbar">
      <div class="plm-toolbar-actions">
        <button
          class="plm-icon-btn plm-delete-btn"
          title="Delete selected products"
          aria-label="Delete selected products"
          :disabled="selectedRows.length === 0"
          @click="deleteSelected"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 7h16" />
          <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2l1-12" />
          <path d="M9 7V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v3" />
          <path d="M10 11v6" />
          <path d="M14 11v6" />
        </svg>
        </button>

        <button
          class="plm-icon-btn plm-restore-btn"
          title="Restore selected products"
          aria-label="Restore selected products"
          :disabled="selectedRows.length === 0"
          @click="restoreSelected"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 14L4 9l5-5" />
          <path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5v0a5.5 5.5 0 0 1-5.5 5.5H11" />
        </svg>
        </button>
        </div>
      </div>
    <div class="table-container" id="drop">
        <table class="custom-table">
          <colgroup>
          <col :style="{ width: `${columnWidths[0]}px` }" />

          <col
            v-for="(header, index) in headers"
            :key="header.key"
            :style="{ width: `${columnWidths[index + 1]}px` }"
          />
        </colgroup>
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

                <th
                  v-for="(header, index) in headers"
                  :key="header.key"
                  :style="{
                    width: `${columnWidths[index + 1]}px`,
                    position: 'relative'
                  }"
                >
                  {{ header.label }}

                  <span
                    class="column-resizer"
                    @pointerdown.stop="startResize($event, index + 1)"
                  ></span>
                </th>
              </tr>
            </thead>
        <tbody>
          <TableRow
            v-for="row in tableData"
            :key="row.physicalid"
            :row="row"
            :headers="headers"
            :depth="0"
            v-model:selected-rows="selectedRows"
            :toggle-expand="toggleExpand"
          />
          </tbody>
      </table>
      </div>
    </div>

  </div>
    
</template>

<script setup>
import { ref, computed, nextTick, onMounted,onBeforeUnmount } from 'vue';
import TableRow from './TableRow.vue'
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
const columnWidths = ref([26, 275, 155, 155, 155, 155])
import './table.css'

let resizeState = null

const startResize = (event, index) => {
  if (event.button !== 0) return

  event.preventDefault()

  resizeState = {
    index,
    startX: event.clientX,
    startWidth: columnWidths.value[index]
  }

  window.addEventListener('pointermove', onResize)
  window.addEventListener('pointerup', stopResize)
}

const onResize = (event) => {
  if (!resizeState) return

  const delta = event.clientX - resizeState.startX
  const newWidth = Math.max(
    60,
    resizeState.startWidth + delta
  )

  columnWidths.value[resizeState.index] = newWidth
}

const stopResize = () => {
  resizeState = null
  window.removeEventListener('pointermove', onResize)
  window.removeEventListener('pointerup', stopResize)
}

onBeforeUnmount(stopResize)

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
      
      row.children =  [...response];
      console.log(row.children);
      
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
