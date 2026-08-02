<template>
  <div class="widget-container">
    <h2 class="dashboard-title">Created vs Resolved CAs</h2>  
    
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
      <div class="chart-card">
        <div class="chart-container">
       <div class="chart-scroll">
      <svg
        :width="svgWidth"
        :height="svgHeight"
        :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
      >
        <!-- Grid -->
        <g>
          <template v-for="tick in yTicks" :key="tick">
            <line
              :x1="leftPadding"
              :x2="svgWidth - rightPadding"
              :y1="getY(tick)"
              :y2="getY(tick)"
              class="grid-line"
            />

            <text
              :x="leftPadding - 10"
              :y="getY(tick) + 5"
              class="y-label"
            >
              {{ tick }}
            </text>
          </template>
        </g>

        <!-- X Labels -->
        <g>
          <template
            v-for="(item,index) in createdData"
            :key="'label'+index"
          >
            <text
              :transform="`translate(${getX(index)},${bottomPadding+25}) rotate(-45)`"
              class="x-label"
            >
              {{ formatDate(item.date) }}
            </text>
          </template>
        </g>

        <!-- Created Line -->
        <path
          :d="createdPath"
          class="created-line"
        />

        <!-- Resolved Line -->
        <path
          :d="resolvedPath"
          class="resolved-line"
        />

        <!-- Created Points -->
        <template
          v-for="(item,index) in createdData"
          :key="'created'+index"
        >
          <g
            :transform="`translate(${getX(index)},${getY(item.value)})`"
          >
            <circle
              r="5"
              fill="#10b981"
            />

            <rect
              x="-12"
              y="-28"
              width="24"
              height="18"
              rx="4"
              fill="#10b981"
            />

            <text
              text-anchor="middle"
              y="-15"
              class="point-text"
            >
              {{ item.value }}
            </text>
          </g>
        </template>

        <!-- Resolved Points -->
        <template
          v-for="(item,index) in resolvedData"
          :key="'resolved'+index"
        >
          <g
            :transform="`translate(${getX(index)},${getY(item.value)})`"
          >
            <circle
              r="5"
              fill="#ef4444"
            />

            <rect
              x="-12"
              y="-28"
              width="24"
              height="18"
              rx="4"
              fill="#ef4444"
            />

            <text
              text-anchor="middle"
              y="-15"
              class="point-text"
            >
              {{ item.value }}
            </text>
          </g>
        </template>
      </svg>

        </div>
        </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
const startDate = ref('');
const new_startDate = ref('');
const new_endDate = ref('');

const endDate = ref('');
const renderKey = ref(0);
const url = ref('');

const clearDates = () => {
  startDate.value = '';
  endDate.value = '';
  renderKey.value += 1;
};
const apiData = ref([]);

const createdData = computed(() =>
    apiData.value.filter(item => item.type === "created").sort((a, b) => new Date(a.date) - new Date(b.date))
);

const resolvedData = computed(() =>
    apiData.value.filter(item => item.type === "resolved").sort((a, b) => new Date(a.date) - new Date(b.date))
);

const leftPadding = 70;
const rightPadding = 40;
const topPadding = 30;
const bottomPadding = 400;

const svgHeight = 460;

/*
    Space between two points.
*/
const pointGap = 200;

/*
    Dynamic width
*/
const svgWidth = computed(() => {
    return Math.max(
        window.innerWidth,
        leftPadding +
        rightPadding +
        (createdData.value.length - 1) * pointGap
    );
});

function getX(index){

    return leftPadding + index * pointGap;

}

/*
    Highest value
*/
const maxValue = computed(() => {

    return Math.ceil(

        Math.max(

            ...apiData.value.map(item => item.value)

        ) / 5

    ) * 5;

});

/*
    Convert value to svg coordinate
*/
function getY(value){

    const chartHeight=bottomPadding-topPadding;

    return bottomPadding -

        (value/maxValue.value)*chartHeight;

}

/*
    Left labels
*/
const yTicks=computed(()=>{

    const divisions=5;

    const step=maxValue.value/divisions;

    return Array.from(

        {length:divisions+1},

        (_,i)=>Math.round(i*step)

    );

});

/*
    Format backend date
*/
function formatDate(date){

    return new Date(date)

    .toLocaleDateString(

        "en-US",

        {

            month:"short",

            year:"2-digit"

        }

    );

}

/*
    Created Line
*/
const createdPath=computed(()=>{

    let path="";

    createdData.value.forEach((item,index)=>{

        if(item.value==null)
            return;

        const x=getX(index);

        const y=getY(item.value);

        path+=

        index===0

        ?`M ${x} ${y}`

        :` L ${x} ${y}`;

    });

    return path;

});

/*
    Resolved Line
*/
const resolvedPath=computed(()=>{

    let path="";

    resolvedData.value.forEach((item,index)=>{

        if(item.value==null)
            return;

        const x=getX(index);

        const y=getY(item.value);

        path+=

        index===0

        ?`M ${x} ${y}`

        :` L ${x} ${y}`;

    });

    return path;

});
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
    console.log("INside submitAction");
    let stDate = startDate.value;
    let edDate = endDate.value
    const [year, month, day] = stDate.split('-');
    stDate = `${month}-${day}-${year}`;
    const [endYear, endMonth, endDay] = edDate.split('-');
    edDate = `${endMonth}-${endDay}-${endYear}`;
    url.value = await getServiceURL();
    console.log("MKK Service URL initialized:", url.value);
    apiData.value = await sendSimpleRequest(`/CustomService/ca/getCATimeSeries?startDate=${stDate}&endDate=${edDate}`);
  } catch (error) {
    console.error("Failed to initialize Service URL on mount:", error);
  }
};
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



.grid-line{

    stroke:#E5E7EB;

    stroke-width:1;

}

.x-label{

    font-size:12px;

    fill:#6B7280;

    text-anchor:middle;

}

.y-label{

    font-size:12px;

    fill:#6B7280;

    text-anchor:end;

}

.created-line{

    stroke:#10B981;

    stroke-width:4;

    fill:none;

    stroke-linejoin:round;

    stroke-linecap:round;

}

.resolved-line{

    stroke:#EF4444;

    stroke-width:4;

    fill:none;

    stroke-linejoin:round;

    stroke-linecap:round;

}

.point-text{

    font-size:10px;

    fill:white;

    font-weight:bold;

    dominant-baseline:middle;

}

@media(max-width:768px){

    .x-label{

        font-size:10px;

    }

    .y-label{

        font-size:10px;

    }

}

.chart-container{

    width:100%;

    overflow-x:auto;

    overflow-y:hidden;

    padding-bottom:20px;

}

.chart-scroll{

    min-width:100%;

}

svg{

    display:block;

}

.label-shadow {
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
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
  cursor: pointer;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
} 
</style>