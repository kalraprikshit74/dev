<template>
  <v-app>
    <v-main>
      <!-- <div class="btn-container">
        <button class="api-btn" @click="fetchUsers">Fetch Users</button>
        <div v-if="showPopup" class="api-popup">
          <span class="close-icon" @click="showPopup = false">&times;</span>
          <pre class="popup-json">{{ popupData }}</pre>
        </div>
      </div> -->
      <h1>Drag and Drop between these two tables using the handle column:</h1>
      <table class="v-data-table-custom-borders" style="margin: 30px auto;width: 100%; table-layout: fixed;">
        <thead>
          <tr>
            <th :style="{ width: widths.t1[0] + 'px' }"></th>
            <th v-for="(header, idx) in headers" :key="header.value"
                :style="{ width: widths.t1[idx+1] + 'px', position: 'relative' }"
                @mouseenter="highlightColumn('t1', idx+1)"
                @mouseleave="clearHighlight('t1', idx+1)">
              {{ header.title }}
              <div class="resizer" @mousedown.prevent="startResize($event, 't1', idx+1)"></div>
            </th>
          </tr>
        </thead>
        <draggable
          v-model="items"
          group="shared-table-group"
          item-key="name"
          tag="tbody"
          :handle="'.drag-handle'"
        >
          <template #item="{ element }">
            <tr>
              <td class="drag-handle" style="cursor: grab; text-align: center; width: 40px">⠿</td>
              <td v-for="(header, idx) in headers" :key="header.value"
                  :class="{'col-hover': isColHighlighted('t1', idx+1)}"
                  :style="{ width: widths.t1[idx+1] + 'px' }">
                {{ element[header.value] }}
              </td>
            </tr>
          </template>
        </draggable>
      </table>
      <table class="v-data-table-custom-borders" style="margin: 30px auto; width: 100%; table-layout: fixed;">
        <thead>
          <tr>
            <th :style="{ width: widths.t2[0] + 'px' }"></th>
            <th v-for="(header, idx) in headers" :key="header.value"
                :style="{ width: widths.t2[idx+1] + 'px', position: 'relative' }"
                @mouseenter="highlightColumn('t2', idx+1)"
                @mouseleave="clearHighlight('t2', idx+1)">
              {{ header.title }}
              <div class="resizer" @mousedown.prevent="startResize($event, 't2', idx+1)"></div>
            </th>
          </tr>
        </thead>
        <draggable
          v-model="items1"
          group="shared-table-group"
          item-key="name"
          tag="tbody"
          :handle="'.drag-handle'"
        >
          <template #item="{ element }">
            <tr>
              <td class="drag-handle" style="cursor: grab; text-align: center; width: 40px">⠿</td>
              <td v-for="(header, idx) in headers" :key="header.value"
                  :style="{ width: widths.t2[idx+1] + 'px' }">
                {{ element[header.value] }}
              </td>
            </tr>
          </template>
        </draggable>
      </table>
      </v-main>
  </v-app>
</template>

<script>
import draggable from 'vuedraggable/src/vuedraggable';

export default {
  components: { draggable },
  data() {
    return {
      // ⭐️ 1. Define Headers
      headers: [
        { title: 'Name', value: 'name' }, // matches item-value="name"
        { title: 'Location', value: 'location' },
        { title: 'height', value: 'height' },
        { title: 'base', value: 'base' },
      ],
      
      // Data array (items)
      items: [
        {
      name: '🍎 Apple',
      location: 'Washington',
      height: '0.1',
      base: '0.07',
      volume: '0.0001',
    },
    {
      name: '🍌 Banana',
      location: 'Ecuador',
      height: '0.2',
      base: '0.05',
      volume: '0.0002',
    },
    {
      name: '🍇 Grapes',
      location: 'Italy',
      height: '0.02',
      base: '0.02',
      volume: '0.00001',
    },
    {
      name: '🍉 Watermelon',
      location: 'China',
      height: '0.4',
      base: '0.3',
      volume: '0.03',
    },
    {
      name: '🍍 Pineapple',
      location: 'Thailand',
      height: '0.3',
      base: '0.2',
      volume: '0.005',
    },
    ],
    items1: [
    {
      name: '🍒 Cherries',
      location: 'Turkey',
      height: '0.02',
      base: '0.02',
      volume: '0.00001',
    },
    {
      name: '🥭 Mango',
      location: 'India',
      height: '0.15',
      base: '0.1',
      volume: '0.0005',
    },
    {
      name: '🍓 Strawberry',
      location: 'USA',
      height: '0.03',
      base: '0.03',
      volume: '0.00002',
    },
    {
      name: '🍑 Peach',
      location: 'China',
      height: '0.09',
      base: '0.08',
      volume: '0.0004',
    },
    {
      name: '🥝 Kiwi',
      location: 'New Zealand',
      height: '0.05',
      base: '0.05',
      volume: '0.0001',
    },
      ],
  selected: [], 
  showPopup: false,
  popupData: '',
      // Column widths per table: first column is handle
      widths: {
        t1: [30, 200, 200, 120, 120],
        t2: [30, 200, 200, 120, 120],
      },
      resizing: null,
      highlighted: { t1: null, t2: null },
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const res = await fetch('https://fake-json-api.mock.beeceptor.com/users');
        const data = await res.json();
        this.popupData = JSON.stringify(data, null, 2);
        this.showPopup = true;
        console.log('API response:', data);
      } catch (err) {
        this.popupData = 'API error: ' + err;
        this.showPopup = true;
        console.error('API error:', err);
      }
    },
    startResize(e, tableKey, colIndex) {
      this.resizing = {
        tableKey,
        colIndex,
        startX: e.clientX,
        startWidth: this.widths[tableKey][colIndex],
      };
    },
    onMouseMove(e) {
      if (!this.resizing) return;
      const delta = e.clientX - this.resizing.startX;
      const newWidth = Math.max(10, this.resizing.startWidth + delta);
      // Vue 3: direct array assignment is reactive
      this.widths[this.resizing.tableKey][this.resizing.colIndex] = newWidth;
    },
    stopResize() {
      this.resizing = null;
    },
    highlightColumn(tableKey, colIndex) {
      this.highlighted[tableKey] = colIndex;
    },
    clearHighlight(tableKey, colIndex) {
      if (this.highlighted[tableKey] === colIndex) this.highlighted[tableKey] = null;
    },
    isColHighlighted(tableKey, colIndex) {
      return this.highlighted[tableKey] === colIndex;
    },
  },
  mounted() {
    window.addEventListener('mousemove', this.onMouseMove);
    window.addEventListener('mouseup', this.stopResize);
  },
  beforeUnmount() {
    window.removeEventListener('mousemove', this.onMouseMove);
    window.removeEventListener('mouseup', this.stopResize);
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.v-data-table-custom-borders {
  border: 1px solid #bdbdbd;
  border-radius: 6px;
  border-collapse: collapse;
  width: auto;
  margin-bottom: 32px;
}
.v-data-table-custom-borders th {
  background: #e0e0e0;
  color: #333;
  font-weight: 600;
  border-right: 1px solid #bdbdbd;
  border-bottom: 1px solid #bdbdbd;
}
.v-data-table-custom-borders th:last-child {
  border-right: none;
}
.v-data-table-custom-borders td {
  border-right: 1px solid #bdbdbd;
  border-bottom: 1px solid #bdbdbd;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.v-data-table-custom-borders td:last-child {
  border-right: none;
}
.v-data-table-custom-borders tr:nth-child(odd) {
  background: #fff;
}
.v-data-table-custom-borders tr:nth-child(even) {
  background: #f5f5f5;
}

/* Highlight entire row on hover */
.v-data-table-custom-borders tbody tr:hover {
  cursor: pointer;
  background: #e6f7ff !important; /* light blue */
}


/* Resizer style */
.v-data-table-custom-borders th { position: relative; }
.v-data-table-custom-borders .resizer {
  position: absolute;
  right: 0;
  top: 0;
  width: 8px;
  height: 100%;
  cursor: ew-resize; /* left-right resize cursor */
  z-index: 5;
}

.drag-handle { user-select: none; }
/* API button styling */
.api-btn {
  background: #e0e0e0;
  color: #333;
  border: none;
  padding: 8px 20px;
  border-radius: 4px;
  margin-bottom: 18px;
  margin-left: 0;
  text-align: left;
  font-size: 16px;
  cursor: pointer;
  display: block;
}
/* API popup styles */
.btn-container {
  position: relative;
  display: block;
  text-align: left;
  margin-left: 0;
  width: fit-content;
}

.api-popup {
  position: absolute;
  top: 100%;
  left: 0;
  width: 600px;
  background: #fff;
  border: 1px solid #bdbdbd;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  z-index: 1000;
  padding: 16px 16px 8px 16px;
  font-size: 13px;
  color: #222;
  margin-top: 6px;
}
.close-icon {
  position: absolute;
  right: 10px;
  top: 8px;
  font-size: 18px;
  color: #888;
  cursor: pointer;
}
.popup-json {
  margin: 0;
  max-height: 120px;
  overflow: auto;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>